#!/usr/bin/env python3
"""
📐 ELLIOTT WAVE + RSI TRADER
Combines Elliott Wave theory with RSI for precise entries
"""

import requests
import json
import time
from datetime import datetime
from statistics import mean, stdev

def get_price_history(symbol, hours=24):
    """Get price history for wave analysis"""
    try:
        r = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}/spot", timeout=10)
        current = float(r.json()["data"]["amount"])
        
        # Simulate history (in production, use historical API)
        import random
        random.seed(hash(symbol))
        prices = [current * (1 + random.uniform(-0.02, 0.02)) for _ in range(hours)]
        prices.append(current)
        return prices
    except:
        return []

def calculate_rsi(prices, period=14):
    """RSI = 100 - (100 / (1 + RS))"""
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
    rsi = 100 - (100 / (1 + rs))
    return rsi

def detect_elliott_wave(prices):
    """Detect Elliott Wave pattern"""
    if len(prices) < 20:
        return "INSUFFICIENT_DATA"
    
    # Simple wave detection based on pivots
    # In production: use proper pivot point algorithm
    
    # Calculate momentum
    recent = prices[-10:]
    first_half = mean(recent[:5])
    second_half = mean(recent[5:])
    
    if second_half > first_half * 1.02:
        return "WAVE_3_UP"  # Impulse wave
    elif second_half < first_half * 0.98:
        return "WAVE_C_DOWN"  # Corrective wave
    else:
        return "WAVE_4_CONSOLIDATION"

def calculate_wave_rsi_confluence(prices):
    """Calculate RSI with wave analysis for confluence"""
    rsi = calculate_rsi(prices)
    wave = detect_elliott_wave(prices)
    
    signal = "NEUTRAL"
    confidence = 0
    
    # Bullish confluence
    if rsi < 35 and "UP" in wave:
        signal = "STRONG_BUY"
        confidence = 90
    elif rsi < 45 and "UP" in wave:
        signal = "BUY"
        confidence = 70
    elif rsi < 30:
        signal = "BUY"
        confidence = 60
    
    # Bearish confluence
    elif rsi > 65 and "DOWN" in wave:
        signal = "STRONG_SELL"
        confidence = 90
    elif rsi > 55 and "DOWN" in wave:
        signal = "SELL"
        confidence = 70
    elif rsi > 70:
        signal = "SELL"
        confidence = 60
    
    return {
        "rsi": rsi,
        "wave": wave,
        "signal": signal,
        "confidence": confidence
    }

def scan_elliott_rsi():
    """Main scanner"""
    print(f"\n{'='*60}")
    print(f"📐 ELLIOTT + RSI SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"]
    
    results = []
    
    for sym in symbols:
        prices = get_price_history(sym, 24)
        if not prices:
            continue
        
        analysis = calculate_wave_rsi_confluence(prices)
        
        emoji = "🟢" if "BUY" in analysis["signal"] else "🔴" if "SELL" in analysis["signal"] else "⚪"
        
        print(f"\n{emoji} {sym.replace('-USD', '')}")
        print(f"   RSI: {analysis['rsi']:.1f}")
        print(f"   Wave: {analysis['wave']}")
        print(f"   Signal: {analysis['signal']} ({analysis['confidence']}% confidence)")
        
        results.append({
            "symbol": sym,
            "rsi": analysis["rsi"],
            "wave": analysis["wave"],
            "signal": analysis["signal"],
            "confidence": analysis["confidence"]
        })
    
    # Save
    with open("elliott_rsi_signals.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    return results

if __name__ == "__main__":
    print("📐 ELLIOTT WAVE + RSI TRADER")
    print("Scanning every 15 minutes...\n")
    
    while True:
        scan_elliott_rsi()
        time.sleep(900)
