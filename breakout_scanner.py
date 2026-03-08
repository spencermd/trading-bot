#!/usr/bin/env python3
"""
💥 BREAKOUT SCANNER - Ultra sensitive
"""

import requests
import json
import time
import os
from datetime import datetime

BASE_DIR = "/home/eldes/polymarket_panic_bot"
BREAKOUTS_FILE = os.path.join(BASE_DIR, "breakouts.json")

CRYPTO_IDS = ["bitcoin", "ethereum", "solana", "dogecoin", "ripple", "cardano", "avalanche-2", "polkadot", "chainlink", "polygon", "litecoin", "uniswap", "cosmos", "stellar", "monero"]

def get_prices():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": ",".join(CRYPTO_IDS), "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=10
        )
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return {}

def load_history():
    try:
        with open(os.path.join(BASE_DIR, "price_history.json"), 'r') as f:
            return json.load(f)
    except:
        return {}

def save_history(history, new_data):
    for cid, price in new_data.items():
        if cid not in history:
            history[cid] = []
        history[cid].append(price)
        history[cid] = history[cid][-30:]
    
    with open(os.path.join(BASE_DIR, "price_history.json"), 'w') as f:
        json.dump(history, f)

def detect_breakout(current, prices, change_24h):
    """Very sensitive breakout detection"""
    if len(prices) < 3:
        return None
    
    # Recent levels
    recent = prices[-8:] if len(prices) >= 8 else prices
    resistance = max(recent)
    support = min(recent)
    
    # Any breakout above recent high
    if current > resistance:
        strength = (current - resistance) / resistance
        return ("BULLISH_BREAKOUT", strength)
    
    # Any breakdown below recent low
    if current < support:
        strength = (support - current) / support
        return ("BEARISH_BREAKDOWN", strength)
    
    # Any momentum
    if len(prices) >= 3:
        mom = (current - prices[-3]) / prices[-3]
        if abs(mom) > 0.005:  # 0.5% in short period
            if mom > 0:
                return ("MOMENTUM_UP", mom)
            else:
                return ("MOMENTUM_DOWN", mom)
    
    # Any significant daily move
    if len(prices) >= 2:
        daily = (current - prices[0]) / prices[0]
        if abs(daily) > 0.008:  # 0.8%+ daily move
            if daily > 0:
                return ("DAILY_GAIN", daily)
            else:
                return ("DAILY_LOSS", daily)
    
    return None

def scan():
    print(f"\n💥 SCAN - {datetime.now().strftime('%H:%M:%S')}")
    
    prices = get_prices()
    if not prices:
        print("  ⚠️ No data")
        return []
    
    history = load_history()
    breakouts = []
    current_prices = {}
    
    for cid in CRYPTO_IDS:
        if cid not in prices:
            continue
        
        current = prices[cid].get("usd", 0)
        change = prices[cid].get("usd_24h_change", 0)
        
        if current == 0:
            continue
        
        current_prices[cid] = current
        hist = history.get(cid, [])
        
        result = detect_breakout(current, hist, change)
        if result:
            btype, strength = result
            breakout = {
                "symbol": cid.upper(),
                "price": current,
                "change_24h": change,
                "breakout_type": btype,
                "strength": strength,
                "timestamp": datetime.now().isoformat()
            }
            breakouts.append(breakout)
            print(f"  💥 {cid.upper()}: ${current:,.2f} {btype} ({strength*100:+.2f}%)")
    
    save_history(history, current_prices)
    
    with open(BREAKOUTS_FILE, 'w') as f:
        json.dump({
            "scan_time": datetime.now().isoformat(),
            "breakout_count": len(breakouts),
            "breakouts": breakouts
        }, f, indent=2)
    
    print(f"  💾 {len(breakouts)} breakouts")
    return breakouts

def main():
    print("💥 BREAKOUT SCANNER - 30 min session")
    print("="*50)
    
    for i in range(3):
        print(f"\n📍 Scan {i+1}/3")
        breakouts = scan()
        
        if breakouts:
            for b in breakouts:
                print(f"\n💥 BREAKOUT: {b['symbol']}!")
                print(f"   Price: ${b['price']:,.2f} | {b['breakout_type']} ({b['strength']*100:+.2f}%)")
        
        if i < 2:
            print("\n⏳ Waiting 10 min...")
            time.sleep(600)
    
    print("\n✅ Done")

if __name__ == "__main__":
    main()
