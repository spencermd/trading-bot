#!/usr/bin/env python3
"""Single gem hunt scan - checks for buy signals and -10%+ drops"""
import json
import requests
from datetime import datetime

ALERTS_FILE = "/home/eldes/polymarket_panic_bot/alerts.json"
BASELINE_FILE = "/home/eldes/polymarket_panic_bot/alerts_baseline.json"

# Known tokens to monitor
SOLANA_TOKENS = ["popcat", "goat", "bonk", "wif", "meow", "chill", "boden", "drift", 
                 "jup", "hump", "moochy", "act", "slerf", "benny", "pengu", "frog", 
                 "pepe", "brett", "moodeng", "fwog", "chill", "navi", "pnut", "spx"]

def get_token_prices():
    """Fetch current prices from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ",".join(SOLANA_TOKENS),
            "order": "market_cap_desc",
            "sparkline": False
        }
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return {c["id"]: c for c in r.json()}
    except Exception as e:
        print(f"Error fetching prices: {e}")
    return {}

def get_low_cap_alts():
    """Get low cap alts for gem hunting"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_asc",
            "per_page": 50,
            "page": 1,
            "sparkline": False
        }
        r = requests.get(url, params=params, timeout=30)
        if r.status_code == 200:
            return [c for c in r.json() if c.get("market_cap", 0) < 50_000_000]
    except:
        pass
    return []

def load_baseline():
    try:
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_alerts(alerts):
    with open(ALERTS_FILE, 'w') as f:
        json.dump(alerts, f, indent=2)

def run_scan():
    print(f"\n{'='*60}")
    print(f"💎 GEM HUNT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    alerts = []
    baseline = load_baseline()
    prices = get_token_prices()
    lowcap = get_low_cap_alts()
    
    # Check tracked tokens for -10%+ drops
    print("\n📉 TRACKED TOKENS - Price Changes:")
    for token_id, data in prices.items():
        symbol = data.get("symbol", "").upper()
        current = data.get("current_price", 0)
        change = data.get("price_change_percentage_24h", 0)
        
        # Check against baseline
        if symbol in baseline:
            baseline_price = baseline[symbol]
            if baseline_price > 0:
                drop_pct = ((current - baseline_price) / baseline_price) * 100
                if drop_pct <= -10:
                    alerts.append({
                        "type": "PANIC_DROP",
                        "symbol": symbol,
                        "current_price": current,
                        "baseline_price": baseline_price,
                        "drop_pct": round(drop_pct, 2),
                        "change_24h": change if change is not None else 0,
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"  🚨 {symbol}: ${current:.6f} ({drop_pct:+.1f}% from baseline)")
        
        # Also show regular 24h change
        if change is not None and change <= -10:
            print(f"  ⚠️ {symbol}: {change:+.1f}% (24h)")
    
    # Look for gem buys (low cap + oversold)
    print("\n💎 GEM SIGNALS (Low Cap + Oversold):")
    for coin in lowcap[:30]:
        mcap = coin.get("market_cap", 0)
        change = coin.get("price_change_percentage_24h") or 0
        symbol = coin.get("symbol", "").upper()
        
        # Buy signal: low cap + oversold
        if mcap < 10_000_000 and change < -10:
            alerts.append({
                "type": "GEM_BUY",
                "symbol": symbol,
                "name": coin.get("name"),
                "price": coin.get("current_price"),
                "mcap": mcap,
                "change_24h": change,
                "timestamp": datetime.now().isoformat()
            })
            print(f"  🟢 {symbol} ({coin.get('name')}): ${coin.get('current_price', 0):.6f}")
            print(f"     MCap: ${mcap:,} | 24h: {change:+.1f}%")
    
    # General buy signals (any -10%+ drop)
    print("\n🎯 ALL OVERSOLD (>-10% 24h):")
    for coin in lowcap[:20]:
        change = coin.get("price_change_percentage_24h") or 0
        if change < -10:
            symbol = coin.get("symbol", "").upper()
            print(f"  📉 {symbol}: {change:+.1f}%")
            alerts.append({
                "type": "OVERSOLD",
                "symbol": symbol,
                "name": coin.get("name"),
                "price": coin.get("current_price"),
                "change_24h": change,
                "timestamp": datetime.now().isoformat()
            })
    
    # Save alerts
    save_alerts(alerts)
    
    print(f"\n📊 Total alerts: {len(alerts)}")
    print(f"💾 Saved to {ALERTS_FILE}")
    
    return alerts

if __name__ == "__main__":
    run_scan()
