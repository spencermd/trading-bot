#!/usr/bin/env python3
"""Enhanced gem hunt using existing data + fresh API calls"""
import json
import requests
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/eldes/polymarket_panic_bot")
ALERTS_FILE = BASE_DIR / "alerts.json"

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return None

def fetch_cgecko(url, params=None):
    """Fetch from CoinGecko with retry"""
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"  API error: {e}")
    return None

def scan_gems():
    print(f"\n{'='*60}")
    print(f"💎 GEM HUNT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    alerts = []
    
    # Try to fetch fresh low-cap data
    print("\n📡 Fetching market data...")
    lowcap = fetch_cgecko(
        "https://api.coingecko.com/api/v3/coins/markets",
        {"vs_currency": "usd", "order": "market_cap_asc", "per_page": 100, "page": 1, "sparkline": False}
    )
    
    # Use cached data if API failed
    if not lowcap:
        print("  ⚠️ Using cached data...")
        for cache_file in ["gems.json", "gem_alts.json", "altcoins.json"]:
            data = load_json(BASE_DIR / cache_file)
            if data:
                lowcap = data.get("gems", []) if "gems" in data else data.get("coins", [])
                break
    
    # Process low-cap coins for buy signals
    print("\n💎 GEM SIGNALS (Low Cap + Oversold):")
    gems_found = 0
    
    if lowcap:
        for coin in lowcap[:50]:
            mcap = coin.get("market_cap", 0) or coin.get("mcap", 0)
            change = coin.get("price_change_percentage_24h") or coin.get("change24h") or coin.get("change_24h") or 0
            symbol = (coin.get("symbol", "") or coin.get("name", "")).upper()
            name = coin.get("name", coin.get("symbol", "?"))
            price = coin.get("current_price", 0) or coin.get("price", 0)
            
            # Buy signal: low cap (<$50M) + oversold (<-10%)
            if mcap and mcap < 50_000_000 and change < -10:
                alerts.append({
                    "type": "GEM_BUY",
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "mcap": mcap,
                    "change_24h": change,
                    "timestamp": datetime.now().isoformat()
                })
                print(f"  🟢 {symbol}: ${price:.6f} | MCap: ${mcap:,.0f} | 24h: {change:+.1f}%")
                gems_found += 1
    
    if gems_found == 0:
        print("  (No gem signals found)")
    
    # Check for panic drops from baseline
    baseline = load_json(BASE_DIR / "alerts_baseline.json") or {}
    print("\n📉 PANIC DROPS (vs baseline):")
    drops_found = 0
    
    if baseline:
        tracked = fetch_cgecko(
            "https://api.coingecko.com/api/v3/coins/markets",
            {"vs_currency": "usd", "ids": "bonk,pengu,popcat,wif,meow,goat", "sparkline": False}
        )
        
        if tracked:
            for coin in tracked:
                symbol = coin.get("symbol", "").upper()
                if symbol in baseline:
                    current = coin.get("current_price", 0)
                    baseline_price = baseline[symbol]
                    if baseline_price > 0:
                        drop = ((current - baseline_price) / baseline_price) * 100
                        if drop <= -10:
                            alerts.append({
                                "type": "PANIC_DROP",
                                "symbol": symbol,
                                "current_price": current,
                                "baseline_price": baseline_price,
                                "drop_pct": round(drop, 2),
                                "timestamp": datetime.now().isoformat()
                            })
                            print(f"  🚨 {symbol}: ${current:.6f} ({drop:+.1f}% from baseline)")
                            drops_found += 1
    
    if drops_found == 0:
        print("  (No panic drops detected)")
    
    # General oversold (any -10%+ 24h change)
    print("\n🎯 ALL OVERSOLD (>=-10% 24h):")
    oversold_found = 0
    
    if lowcap:
        for coin in lowcap[:30]:
            change = coin.get("price_change_percentage_24h") or coin.get("change24h") or 0
            if change and change <= -10:
                symbol = (coin.get("symbol", "") or coin.get("name", "")).upper()
                price = coin.get("current_price", 0) or coin.get("price", 0)
                alerts.append({
                    "type": "OVERSOLD",
                    "symbol": symbol,
                    "name": coin.get("name"),
                    "price": price,
                    "change_24h": change,
                    "timestamp": datetime.now().isoformat()
                })
                print(f"  📉 {symbol}: {change:+.1f}%")
                oversold_found += 1
    
    if oversold_found == 0:
        print("  (No oversold positions)")
    
    # Save alerts
    with open(ALERTS_FILE, 'w') as f:
        json.dump(alerts, f, indent=2)
    
    print(f"\n📊 Summary: {len(alerts)} alerts")
    print(f"💾 Saved to {ALERTS_FILE}")
    
    return alerts

if __name__ == "__main__":
    scan_gems()
