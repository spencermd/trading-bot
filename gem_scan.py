#!/usr/bin/env python3
"""
Gem Finder - Find low-cap gems down 8%+
Save to gems.json
Uses CoinGecko markets API for bulk fetch
"""

import requests
import json
from datetime import datetime

OUTPUT_FILE = "/home/eldes/polymarket_panic_bot/gems.json"

def get_top_coins():
    """Get top coins from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 200,
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def scan_gems():
    """Scan for gems down 8%+"""
    coins = get_top_coins()
    gems = []
    
    for coin in coins:
        try:
            mcap = coin.get('market_cap', 0)
            change_24h = coin.get('price_change_percentage_24h', 0)
            current_price = coin.get('current_price', 0)
            symbol = coin.get('symbol', '').upper()
            name = coin.get('name', '')
            
            # Filter: market cap < $1B AND down 8%+
            if mcap and change_24h is not None:
                if mcap < 1000000000 and change_24h <= -8:
                    gem = {
                        'name': symbol,
                        'id': coin.get('id'),
                        'mcap': mcap,
                        'change24h': round(change_24h, 2),
                        'price': current_price,
                        'timestamp': datetime.now().isoformat()
                    }
                    gems.append(gem)
                    print(f"💎 GEM: {gem['name']} ${gem['mcap']:,.0f} ({gem['change24h']}% down)")
                    
        except Exception as e:
            pass
    
    return gems

def main():
    print(f"🔍 GEM FINDER - {datetime.now().strftime('%H:%M:%S')}")
    print("Criteria: Market cap < $1B AND down 8%+ in 24h")
    
    gems = scan_gems()
    
    result = {
        'scan_time': datetime.now().isoformat(),
        'gems_found': len(gems),
        'gems': gems
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📊 Found {len(gems)} gems")
    print(f"💾 Saved to: {OUTPUT_FILE}")
    
    return result

if __name__ == "__main__":
    main()
