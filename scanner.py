#!/usr/bin/env python3
"""
CRYPTO DIVERGENCE SCANNER v2
Uses CoinGecko API - Commander's money-making machine 🤑
"""

import time
import requests
import json
from datetime import datetime

# Configuration
COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH", 
    "solana": "SOL",
    "ripple": "XRP",
    "dogecoin": "DOGE",
    "cardano": "ADA",
    "avalanche-2": "AVAX"
}

def get_prices():
    """Get current prices from CoinGecko"""
    try:
        ids = ",".join(COINS.keys())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url, timeout=15)
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return {}

def analyze_market(coin_id, data):
    """Analyze a single market"""
    name = COINS.get(coin_id, coin_id.upper())
    price = data.get("usd", 0)
    change_24h = data.get("usd_24h_change", 0)
    
    # Simple signals based on 24h change
    signal = None
    
    if change_24h < -10:
        signal = "DEEP_DISCOUNT"  # 10%+ drop = potential buy
    elif change_24h < -5:
        signal = "BUY_THE_DIP"
    elif change_24h > 10:
        signal = "TAKE_PROFIT"
    elif change_24h > 5:
        signal = "MOMENTUM_UP"
    
    return {
        "name": name,
        "price": price,
        "change_24h": change_24h,
        "signal": signal
    }

def scan():
    """Main scanner loop"""
    print("\n" + "="*60)
    print(f"📈 CRYPTO SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    data = get_prices()
    if not data:
        print("❌ Failed to fetch data")
        return
    
    signals = []
    
    for coin_id, market_data in data.items():
        analysis = analyze_market(coin_id, market_data)
        
        emoji = "🚀" if analysis["change_24h"] > 0 else "🔻"
        print(f"\n{emoji} {analysis['name']}: ${analysis['price']:,.2f} ({analysis['change_24h']:+.2f}%)")
        
        if analysis["signal"]:
            print(f"   🎯 {analysis['signal']}")
            signals.append(analysis)
    
    print("\n" + "-"*60)
    
    if signals:
        print(f"🎯 ACTIVE SIGNALS ({len(signals)}):")
        for s in signals:
            print(f"   {s['name']}: {s['signal']} ({s['change_24h']:+.2f}%)")
        
        # Save to file
        with open("signals.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "signals": signals
            }, f, indent=2)
        print(f"\n💾 Saved to signals.json")
    else:
        print("😴 No strong signals")
    
    print("="*60)
    return signals

if __name__ == "__main__":
    print("🚀 SCANNER STARTED - Ctrl+C to stop")
    scan()
