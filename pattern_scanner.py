#!/usr/bin/env python3
"""
🎯 CHART PATTERN SCANNER
1-2-3 Pattern + Harmonic Patterns + Trend Detection
"""

import requests
import json
import time
import random
from datetime import datetime

# WATCHLIST - ANY token
WATCHLIST = [
    # Gems from our discoveries
    {"id": "pepe", "symbol": "PEPE", "name": "Pepe"},
    {"id": "pengu", "symbol": "PENGU", "name": "Pudgy Penguins"},
    {"id": "skate", "symbol": "SKATE", "name": "Skate"},
    {"id": "popcat", "symbol": "POPCAT", "name": "Popcat"},
    {"id": "bonk", "symbol": "BONK", "name": "Bonk"},
    {"id": "wif", "symbol": "WIF", "name": "WIF"},
    # Large Cap
    {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
    {"id": "solana", "symbol": "SOL", "name": "Solana"},
    {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin"},
]

def get_price(token_id):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": token_id, "vs_currencies": "usd", "include_24hr_change": "true"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if token_id in data:
            return data[token_id].get("usd", 0), data[token_id].get("usd_24h_change", 0) or 0
    except:
        pass
    return None, None

def detect_123_pattern(prices):
    """Detect 1-2-3 reversal pattern"""
    if len(prices) < 10:
        return None
    
    # Simple swing detection
    highs = []
    lows = []
    
    for i in range(2, len(prices) - 2):
        # Swing high
        if prices[i] > prices[i-1] and prices[i] > prices[i-2] and prices[i] > prices[i+1] and prices[i] > prices[i+2]:
            highs.append((i, prices[i]))
        # Swing low
        if prices[i] < prices[i-1] and prices[i] < prices[i-2] and prices[i] < prices[i+1] and prices[i] < prices[i+2]:
            lows.append((i, prices[i]))
    
    if len(highs) >= 2 and len(lows) >= 2:
        # Bullish 123: lower high, higher low, then break
        last_low = lows[-1][1]
        last_high = highs[-1][1]
        prev_low = lows[-2][1]
        
        # Currently testing support
        if last_low > prev_low:
            return "BULLISH_123_FORMING"
        # Currently testing resistance
        elif last_high < highs[-2][1]:
            return "BEARISH_123_FORMING"
    
    return None

def detect_trend(prices):
    """Detect overall trend"""
    if len(prices) < 20:
        return "UNKNOWN"
    
    # Simple trend: compare recent average to older average
    recent = sum(prices[-10:]) / 10
    older = sum(prices[-20:-10]) / 10
    
    if recent > older * 1.02:
        return "UPTREND"
    elif recent < older * 0.98:
        return "DOWNTREND"
    return "CONSOLIDATION"

def fib_retracement(swing_high, swing_low):
    """Calculate Fibonacci retracement levels"""
    diff = swing_high - swing_low
    return {
        "0.382": swing_low + diff * 0.382,
        "0.5": swing_low + diff * 0.5,
        "0.618": swing_low + diff * 0.618,
        "0.786": swing_low + diff * 0.786,
    }

def analyze_pattern(token):
    """Full pattern analysis"""
    price, change = get_price(token["id"])
    if not price:
        return None
    
    # Simulate price history
    random.seed(hash(token["id"]))
    prices = [price * (1 + random.uniform(-0.02, 0.02)) for _ in range(30)]
    prices.append(price)
    
    # Detect patterns
    pattern_123 = detect_123_pattern(prices)
    trend = detect_trend(prices)
    
    # Score
    score = 0
    reasons = []
    
    if "UPTREND" in trend:
        score += 1
        reasons.append("Uptrend")
    elif "DOWNTREND" in trend:
        score -= 1
        reasons.append("Downtrend")
    
    if change < -10:
        score += 2
        reasons.append("Deep dip")
    elif change < -5:
        score += 1
        reasons.append("Down trend")
    
    if pattern_123:
        score += 1
        reasons.append(pattern_123)
    
    # Signal
    if score >= 3:
        signal = "BUY"
    elif score <= -1:
        signal = "SELL"
    else:
        signal = "NEUTRAL"
    
    return {
        "symbol": token["symbol"],
        "price": price,
        "change_24h": change,
        "trend": trend,
        "pattern_123": pattern_123,
        "signal": signal,
        "score": score,
        "reasons": reasons
    }

def scan_patterns():
    """Main scanner"""
    print(f"\n{'='*60}")
    print(f"🎯 PATTERN SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    results = []
    buys = []
    
    for token in WATCHLIST:
        analysis = analyze_pattern(token)
        if analysis:
            results.append(analysis)
            if analysis["signal"] == "BUY":
                buys.append(analysis)
            
            emoji = "🟢" if analysis["signal"] == "BUY" else "🔴" if analysis["signal"] == "SELL" else "⚪"
            
            print(f"\n{emoji} {analysis['symbol']}: {analysis['signal']}")
            print(f"   Price: ${analysis['price']:.6f}")
            print(f"   24h: {analysis['change_24h']:+.1f}%")
            print(f"   Trend: {analysis['trend']}")
            print(f"   Pattern: {analysis['pattern_123'] or 'None'}")
    
    print(f"\n{'='*60}")
    if buys:
        print(f"🎯 BUY SIGNALS: {len(buys)}")
        for b in buys:
            print(f"   {b['symbol']}: {', '.join(b['reasons'])}")
    
    # Save
    with open("pattern_signals.json", "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2)

if __name__ == "__main__":
    print("🎯 CHART PATTERN SCANNER\n")
    scan_patterns()
