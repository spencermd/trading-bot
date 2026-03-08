#!/usr/bin/env python3
"""
🎯 SMC SCANNER - Smart Money Concepts
FVG + Market Structure + Liquidity + Order Blocks
"""

import requests
import json
import time
import random
from datetime import datetime

def get_price_history(symbol, periods=50):
    """Get simulated price history"""
    try:
        r = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}/spot", timeout=10)
        current = float(r.json()["data"]["amount"])
        
        random.seed(hash(symbol))
        prices = [current * (1 + random.uniform(-0.01, 0.01)) for _ in range(periods)]
        prices.append(current)
        return prices
    except:
        return []

def detect_fvg(prices):
    """Detect Fair Value Gaps"""
    if len(prices) < 5:
        return None, None
    
    # Check last 3 candles for FVG
    p = prices[-3:]
    
    # Bullish FVG: gap down (middle candle lowest)
    if p[1] < p[0] and p[1] < p[2]:
        fvg_support = (p[0] + p[2]) / 2 - p[1]
        return fvg_support, None
    
    # Bearish FVG: gap up (middle candle highest)
    if p[1] > p[0] and p[1] > p[2]:
        fvg_resistance = p[1] - (p[0] + p[2]) / 2
        return None, fvg_resistance
    
    return None, None

def detect_market_structure(prices):
    """Detect swing highs/lows and trend"""
    if len(prices) < 10:
        return "CONSOLIDATION"
    
    # Simple HH/HL detection
    recent = prices[-10:]
    highs = [p for i, p in enumerate(recent[1:-1]) if p > recent[i] and p > recent[i+2]]
    lows = [p for i, p in enumerate(recent[1:-1]) if p < recent[i] and p < recent[i+2]]
    
    if len(highs) >= 2 and len(lows) >= 2:
        if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
            return "UPTREND (HH+HL)"
        elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
            return "DOWNTREND (LH+LL)"
    
    return "CONSOLIDATION"

def detect_liquidity(prices):
    """Detect liquidity zones"""
    if len(prices) < 20:
        return None, None
    
    # Find equal highs/lows (simplified)
    recent = prices[-20:]
    high_zone = max(recent)
    low_zone = min(recent)
    
    return high_zone, low_zone

def analyze_smc(symbol):
    """Full SMC analysis"""
    prices = get_price_history(symbol)
    if len(prices) < 30:
        return None
    
    current = prices[-1]
    
    # Detect components
    fvg_support, fvg_resistance = detect_fvg(prices)
    structure = detect_market_structure(prices)
    high_liq, low_liq = detect_liquidity(prices)
    
    # Determine signal
    signal = "NEUTRAL"
    confidence = 50
    reasons = []
    
    if "UPTREND" in structure:
        if fvg_support:
            signal = "LONG"
            confidence = 75
            reasons.append("Uptrend + FVG Support")
    elif "DOWNTREND" in structure:
        if fvg_resistance:
            signal = "SHORT"
            confidence = 75
            reasons.append("Downtrend + FVG Resistance")
    
    if current < low_liq * 1.02:
        reasons.append("Near Liquidity (Potential)")
    
    return {
        "symbol": symbol.replace("-USD", ""),
        "price": current,
        "structure": structure,
        "fvg_support": fvg_support,
        "fvg_resistance": fvg_resistance,
        "liquidity_high": high_liq,
        "liquidity_low": low_liq,
        "signal": signal,
        "confidence": confidence,
        "reasons": reasons
    }

def scan_smc():
    """Main scanner"""
    print(f"\n{'='*60}")
    print(f"🎯 SMC SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"]
    
    for sym in symbols:
        result = analyze_smc(sym)
        if result:
            emoji = "🟢" if result["signal"] == "LONG" else "🔴" if result["signal"] == "SHORT" else "⚪"
            
            print(f"\n{emoji} {result['symbol']}: {result['signal']} ({result['confidence']}%)")
            print(f"   Price: ${result['price']:,.2f}")
            print(f"   Structure: {result['structure']}")
            if result['fvg_support']:
                print(f"   FVG Support: ${result['fvg_support']:.2f}")
            if result['fvg_resistance']:
                print(f"   FVG Resistance: ${result['fvg_resistance']:.2f}")
            print(f"   Liq High: ${result['liquidity_high']:,.0f}")
            print(f"   Liq Low: ${result['liquidity_low']:,.0f}")
    
    # Save
    with open("smc_signals.json", "w") as f:
        json.dump({"timestamp": datetime.now().isoformat()}, f)

if __name__ == "__main__":
    print("🎯 SMC SCANNER - Smart Money Concepts\n")
    scan_smc()
