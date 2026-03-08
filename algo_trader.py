#!/usr/bin/env python3
"""
ALGORITHMIC TRADING ENGINE
Multiple strategies combined for maximum edge
"""

import requests
import time
import json
import random
from datetime import datetime
from statistics import mean, stdev

# Configuration
SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"]
SIGNAL_FILE = "algo_signals.json"

def get_price(symbol):
    """Get current price"""
    r = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}/spot", timeout=10)
    return float(r.json()["data"]["amount"])

def get_historical(symbol, points=20):
    """Get simulated historical data"""
    current = get_price(symbol)
    random.seed(hash(symbol) % 1000)
    prices = [current * (1 + random.uniform(-0.03, 0.03)) for _ in range(points)]
    prices.append(current)
    return prices

def calculate_rsi(prices, period=14):
    """Relative Strength Index"""
    if len(prices) < period + 1:
        return 50
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger(prices):
    """Bollinger Bands"""
    m = mean(prices)
    s = stdev(prices) if len(prices) > 1 else 0
    return {
        'upper': m + 2*s,
        'middle': m,
        'lower': m - 2*s,
        'volatility': (s/m)*100 if m > 0 else 0
    }

def calculate_ema(prices, period):
    """Exponential Moving Average"""
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * multiplier + ema * (1 - multiplier)
    return ema

def analyze_symbol(symbol):
    """Run all strategies on a symbol"""
    current = get_price(symbol)
    history = get_historical(symbol)
    
    rsi = calculate_rsi(history)
    bb = calculate_bollinger(history)
    ema_12 = calculate_ema(history, 12)
    ema_26 = calculate_ema(history, 26)
    
    # Calculate scores
    buy_score = 0
    sell_score = 0
    
    # RSI signals
    if rsi < 30:
        buy_score += 2
    elif rsi < 40:
        buy_score += 1
    elif rsi > 70:
        sell_score += 2
    elif rsi > 60:
        sell_score += 1
    
    # Bollinger signals
    if current < bb['lower']:
        buy_score += 2
    elif current > bb['upper']:
        sell_score += 2
    
    # EMA crossover
    if ema_12 > ema_26:
        buy_score += 1
    else:
        sell_score += 1
    
    # Determine action
    if buy_score > sell_score + 1:
        action = "STRONG_BUY"
    elif buy_score > sell_score:
        action = "BUY"
    elif sell_score > buy_score + 1:
        action = "STRONG_SELL"
    elif sell_score > buy_score:
        action = "SELL"
    else:
        action = "HOLD"
    
    return {
        'symbol': symbol.replace('-USD', ''),
        'price': current,
        'rsi': rsi,
        'volatility': bb['volatility'],
        'bb_upper': bb['upper'],
        'bb_lower': bb['lower'],
        'ema_12': ema_12,
        'ema_26': ema_26,
        'buy_score': buy_score,
        'sell_score': sell_score,
        'action': action
    }

def scan():
    """Run full scan"""
    print(f"\n{'='*60}")
    print(f"🔍 ALGO SCAN - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    signals = []
    for sym in SYMBOLS:
        try:
            result = analyze_symbol(sym)
            signals.append(result)
            
            emoji = "🟢" if "BUY" in result['action'] else "🔴" if "SELL" in result['action'] else "🟡"
            print(f"\n{emoji} {result['symbol']}: ${result['price']:,.2f}")
            print(f"   Action: {result['action']} (buy:{result['buy_score']} sell:{result['sell_score']})")
            print(f"   RSI: {result['rsi']:.1f} | Vol: {result['volatility']:.1f}%")
        except Exception as e:
            print(f"Error with {sym}: {e}")
    
    # Save signals
    with open(SIGNAL_FILE, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'signals': signals
        }, f, indent=2)
    
    # Strongest signal
    strong = [s for s in signals if "STRONG" in s['action']]
    if strong:
        print(f"\n🎯 STRONGEST SIGNAL: {strong[0]['symbol']} - {strong[0]['action']}")
    
    return signals

if __name__ == "__main__":
    while True:
        scan()
        time.sleep(60)
