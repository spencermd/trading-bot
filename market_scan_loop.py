#!/usr/bin/env python3
"""Market Scanner - OKX API based trending/gaining coins scanner"""
import json
import os
import time
import sys
from datetime import datetime

import requests

# Force output flushing
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

SCANS = 5
INTERVAL = 8 * 60  # 8 minutes in seconds
OUTPUT_FILE = "/home/eldes/polymarket_panic_bot/trending.json"

def get_gainers():
    """Fetch gainers from OKX API"""
    try:
        r = requests.get("https://www.okx.com/api/v5/market/tickers?instType=SPOT", timeout=15)
        if r.status_code == 200:
            data = r.json()
            if "data" in data:
                results = []
                for t in data["data"]:
                    try:
                        last = float(t["last"])
                        open_24h = float(t.get("open24h", 0))
                        if open_24h > 0:
                            change = ((last - open_24h) / open_24h) * 100
                            results.append({
                                "symbol": t["instId"],
                                "last": last,
                                "open24h": open_24h,
                                "change_24h": change,
                                "vol_24h": t.get("volCcy24h", "0")
                            })
                    except:
                        pass
                return results
    except Exception as e:
        print(f"Error fetching: {e}")
    return []

def scan(scan_num):
    """Perform one scan"""
    print(f"\n{'='*50}")
    print(f"🔍 SCAN {scan_num}/{SCANS} - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")
    sys.stdout.flush()
    
    results = get_gainers()
    
    if not results:
        print("❌ No data fetched")
        return
    
    # Sort by change
    results.sort(key=lambda x: x["change_24h"], reverse=True)
    
    # Find coins up 15%+
    hot_coins = [c for c in results if c["change_24h"] >= 15]
    
    result = {
        "scan_time": datetime.now().isoformat(),
        "scan_number": scan_num,
        "hot_coins_15plus": hot_coins[:10],
        "total_scanned": len(results)
    }
    
    # Save to file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Total coins scanned: {len(results)}")
    print(f"🔥 Hot coins (15%+): {len(hot_coins)}")
    sys.stdout.flush()
    
    if hot_coins:
        for coin in hot_coins[:10]:
            msg = f"🔥 TRENDING: {coin['symbol']} +{coin['change_24h']:.1f}%"
            print(msg)
            sys.stdout.flush()
    else:
        print("📊 No coins up 15%+ this scan")
        sys.stdout.flush()
    
    print(f"✅ Saved to {OUTPUT_FILE}")
    sys.stdout.flush()
    return result

# Run scans
for i in range(SCANS):
    result = scan(i + 1)
    
    if i < SCANS - 1:
        print(f"⏳ Next scan in 8 minutes...")
        sys.stdout.flush()
        time.sleep(INTERVAL)

print(f"\n✅ Scanner complete - {SCANS} scans done!")
