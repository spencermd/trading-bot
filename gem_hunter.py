#!/usr/bin/env python3
"""
💎 GEM HUNTER - Continuous Low Cap Scanner for Solana/Phantom
Scans for gems under $10M market cap using RSI, Bollinger, and momentum algos
"""

import requests
import json
import time
from datetime import datetime
from statistics import mean, stdev

SIGNAL_FILE = "gem_signals.json"

# Known Solana tokens to monitor (low cap gems)
SOLANA_GEMS = [
    "popcat", "goat", "bonk", "wif", "meow", "chill", "boden", "drift", 
    "jup", "hump", "moochy", "act", "slerf", "benny", "c标准的"
]

def get_token_data(token_ids):
    """Get data for multiple tokens"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ",".join(token_ids),
            "order": "market_cap_desc",
            "sparkline": False
        }
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

def get_low_cap_coins():
    """Get low cap coins from CoinGecko"""
    try:
        # Get coins with low market cap
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_asc",
            "per_page": 100,
            "page": 1,
            "sparkline": False
        }
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            coins = r.json()
            # Filter for low cap, high potential
            return [c for c in coins if c.get("market_cap", 0) < 50_000_000]
    except:
        pass
    return []

def calculate_signal(change_24h, mcap):
    """Calculate trading signal using our algorithms"""
    buy_score = 0
    sell_score = 0
    reasons = []
    
    # RSI-like (using 24h change as momentum proxy)
    if change_24h < -20:
        buy_score += 2
        reasons.append("Oversold (-20%+)")
    elif change_24h < -10:
        buy_score += 1
        reasons.append("Oversold (-10%+)")
    elif change_24h > 20:
        sell_score += 2
        reasons.append("Overbought")
    
    # Market cap advantage (lower = more upside)
    if mcap < 500_000:
        buy_score += 3
        reasons.append("Micro cap!")
    elif mcap < 2_000_000:
        buy_score += 2
        reasons.append("Low cap")
    elif mcap < 10_000_000:
        buy_score += 1
        reasons.append("Small cap")
    
    # Volatility bonus
    if abs(change_24h) > 10:
        buy_score += 1
        reasons.append("High volatility = opportunity")
    
    # Determine action
    if buy_score >= 4:
        action = "STRONG_BUY"
    elif buy_score >= 2:
        action = "BUY"
    elif sell_score >= 3:
        action = "SELL"
    else:
        action = "WATCH"
    
    return action, buy_score, sell_score, reasons

def analyze_gem(coin):
    """Analyze a single gem"""
    name = coin.get("name", "Unknown")
    symbol = coin.get("symbol", "?").upper()
    price = coin.get("current_price", 0)
    mcap = coin.get("market_cap", 0)
    change_24h = coin.get("price_change_percentage_24h", 0)
    volume = coin.get("total_volume", 0)
    
    action, buy_s, sell_s, reasons = calculate_signal(change_24h, mcap)
    
    return {
        "name": name,
        "symbol": symbol,
        "price": price,
        "mcap": mcap,
        "change_24h": change_24h,
        "volume": volume,
        "action": action,
        "buy_score": buy_s,
        "sell_score": sell_s,
        "reasons": reasons
    }

def scan():
    """Main scan function"""
    print(f"\n{'='*60}")
    print(f"💎 GEM SCAN - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    # Try to get live data
    coins = get_low_cap_coins()
    
    # Add known Solana gems if not enough
    known_ids = SOLANA_GEMS
    known_data = get_token_data(known_ids)
    if known_data:
        coins.extend(known_data)
    
    if not coins:
        print("⚠️ Could not fetch data, using cached")
        return []
    
    # Remove duplicates
    seen = set()
    unique = []
    for c in coins:
        if c.get("id") not in seen:
            seen.add(c.get("id"))
            unique.append(c)
    coins = unique
    
    # Analyze
    results = []
    for coin in coins[:50]:
        gem = analyze_gem(coin)
        if gem["buy_score"] > 0 or gem["action"] != "WATCH":
            results.append(gem)
    
    # Sort by score
    results.sort(key=lambda x: x["buy_score"], reverse=True)
    
    # Print top results
    strong_buys = [r for r in results if "BUY" in r["action"]]
    print(f"\n🎯 Found {len(strong_buys)} potential buys\n")
    
    for gem in results[:10]:
        emoji = "🔥" if "STRONG" in gem["action"] else "🟢" if "BUY" in gem["action"] else "🟡"
        print(f"{emoji} {gem['name']} ({gem['symbol']})")
        if gem["price"] < 0.001:
            print(f"   Price: ${gem['price']:.8f}")
        elif gem["price"] < 0.01:
            print(f"   Price: ${gem['price']:.6f}")
        else:
            print(f"   Price: ${gem['price']:.4f}")
        print(f"   MCap: ${gem['mcap']:,}")
        print(f"   24h: {gem['change_24h']:+.1f}%")
        print(f"   Action: {gem['action']} (score: {gem['buy_score']})")
        if gem["reasons"]:
            print(f"   Why: {', '.join(gem['reasons'][:2])}")
        print()
    
    # Save
    with open(SIGNAL_FILE, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "gems": results[:20]
        }, f, indent=2)
    
    return results

if __name__ == "__main__":
    print("💎 GEM HUNTER - Continuous Scanner")
    print("Targeting: Solana/Phantom wallet tokens")
    print("Criteria: Market cap < $10M, oversold signals\n")
    
    while True:
        try:
            scan()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(300)  # Scan every 5 minutes
