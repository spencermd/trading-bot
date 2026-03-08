#!/usr/bin/env python3
"""
🧠 MEMETIC TRADING ENGINE
Applies memetic principles to crypto trading
"""

import requests
import json
import time
from datetime import datetime

# Memetic principles applied to trading:
# 1. VIRAL COEFFICIENT - Ideas that spread faster = coins with more social buzz
# 2. ATTENTION ECONOMY - Highest attention = biggest moves
# 3. COOPERATIVE EMERGENCE - Community-driven pumps (e.g., doge, pepe)
# 4. MEMETIC HAZARDS - FOMO spreads like virus - be aware!

def get_social_buzz():
    """Get trending coins (viral potential)"""
    try:
        # Get trending from CoinGecko
        r = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=15)
        data = r.json()
        
        buzz_tokens = []
        for coin in data.get("coins", [])[:10]:
            item = coin.get("item", {})
            buzz_tokens.append({
                "name": item.get("name"),
                "symbol": item.get("symbol"),
                "price_btc": item.get("price_btc"),
                "market_cap_rank": item.get("market_cap_rank"),
                "score": item.get("score", 0)
            })
        return buzz_tokens
    except:
        return []

def get_momentum():
    """Get biggest gainers (attention = momentum)"""
    try:
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=false", timeout=15)
        coins = r.json()
        
        # Sort by 24h change
        gainers = sorted(coins, key=lambda x: x.get("price_change_percentage_24h", 0), reverse=True)[:5]
        
        return [{
            "name": c.get("name"),
            "symbol": c.get("symbol"),
            "change": c.get("price_change_percentage_24h"),
            "volume": c.get("total_volume")
        } for c in gainers]
    except:
        return []

def analyze_memetic_opportunities():
    """Find memetic trading opportunities"""
    print(f"\n{'='*60}")
    print(f"🧠 MEMETIC SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    # 1. Get social buzz (viral potential)
    print("\n📣 SOCIAL BUZZ (Viral Potential):")
    buzz = get_social_buzz()
    for b in buzz[:5]:
        print(f"   🔥 {b['symbol'].upper()}: #{b.get('market_cap_rank', '?')} - Score: {b.get('score', 0)}")
    
    # 2. Get momentum (attention = moves)
    print("\n🚀 MOMENTUM (Attention = Moves):")
    momentum = get_momentum()
    for m in momentum:
        emoji = "📈" if m["change"] > 0 else "📉"
        print(f"   {emoji} {m['symbol'].upper()}: {m['change']:+.1f}%")
    
    # 3. Combine for signals
    print("\n🎯 MEMETIC SIGNALS:")
    
    signals = []
    
    # High buzz + high momentum = explosive potential
    buzz_symbols = {b["symbol"].upper() for b in buzz[:5]}
    momentum_symbols = {m["symbol"].upper() for m in momentum[:3]}
    
    explosive = buzz_symbols & momentum_symbols
    if explosive:
        for s in explosive:
            signals.append(f"🔥 EXPLOSIVE: {s} (High buzz + momentum!)")
    
    # High buzz, low momentum = accumulation potential
    for b in buzz[:5]:
        sym = b["symbol"].upper()
        if sym not in momentum_symbols:
            signals.append(f"📌 WATCH: {sym} (High buzz, waiting for momentum)")
    
    for s in signals:
        print(f"   {s}")
    
    # Save
    result = {
        "timestamp": datetime.now().isoformat(),
        "buzz": buzz,
        "momentum": momentum,
        "signals": signals
    }
    
    with open("memetic_signals.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Saved to memetic_signals.json")
    return result

if __name__ == "__main__":
    print("🧠 MEMETIC TRADING ENGINE")
    print("Applying memetics to crypto...\n")
    
    while True:
        analyze_memetic_opportunities()
        time.sleep(300)  # Scan every 5 minutes
