#!/usr/bin/env python3
"""
Market Scanner - Runs 6 scans (every 10 minutes for 60 minutes)
Finds coins up 20%+ in 24h and saves to trending.json
"""

import json
import time
import urllib.request
import ssl
import sys
from datetime import datetime

TRENDING_FILE = "/home/eldes/polymarket_panic_bot/trending.json"
SCAN_INTERVAL = 600  # 10 minutes
TOTAL_SCANS = 6

def log(msg):
    print(msg)
    sys.stdout.flush()

def save_trending(coins):
    data = {
        "last_scan": datetime.now().isoformat(),
        "coins": coins
    }
    with open(TRENDING_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def scan_coingecko():
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=30, context=ctx)
        data = json.loads(response.read().decode())
        
        trending = []
        for coin in data:
            change = coin.get('price_change_percentage_24h') or 0
            if change >= 20:
                trending.append({
                    'id': coin.get('id'),
                    'symbol': coin.get('symbol'),
                    'name': coin.get('name'),
                    'price_change_percentage_24h': change,
                    'current_price': coin.get('current_price'),
                    'market_cap': coin.get('market_cap'),
                    'image': coin.get('image')
                })
        
        return trending
        
    except Exception as e:
        log(f"❌ Error scanning: {e}")
        return []

# Run scanner
log("🚀 Starting Market Scanner (20%+ momentum detector)")
log(f"⏱️  Running {TOTAL_SCANS} scans, every {SCAN_INTERVAL//60} minutes")
log(f"📁 Output: {TRENDING_FILE}")
log("-" * 50)

for scan_num in range(1, TOTAL_SCANS + 1):
    timestamp = datetime.now().strftime('%H:%M:%S')
    log(f"\n🔍 Scan #{scan_num} at {timestamp}")
    
    coins = scan_coingecko()
    
    if coins:
        for coin in coins:
            log(f"🚨 TRENDING: {coin['name']} ({coin['symbol'].upper()}) +{coin['price_change_percentage_24h']:.2f}%")
    else:
        log("📊 No coins up 20%+ in 24h found this scan")
    
    save_trending(coins)
    
    if scan_num < TOTAL_SCANS:
        log(f"⏳ Waiting {SCAN_INTERVAL//60} minutes until next scan...")
        time.sleep(SCAN_INTERVAL)

log(f"\n✅ Completed {TOTAL_SCANS} scans (60 minutes)")
log("Scanner finished.")
