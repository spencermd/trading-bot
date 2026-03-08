#!/usr/bin/env python3
"""
Whale Watcher - Track large cap coins for volume spikes
Uses existing bot data - no API calls
Runs every 20 minutes for 40 minutes (2 cycles)
"""

import json
import time
import os
import sys
from datetime import datetime

# Force unbuffered output
sys.stdout = sys.stderr

WHALES_FILE = "/home/eldes/polymarket_panic_bot/whales.json"
BOT_DIR = "/home/eldes/polymarket_panic_bot"
CHECK_INTERVAL = 30  # 30 seconds for demo (use 20*60 for production)
CYCLES = 2  # 40 minutes total

print("DEBUG: Starting script", flush=True)

def get_local_data():
    """Get data from existing bot files"""
    coins = []
    
    # Read altcoins for market cap
    try:
        with open(f"{BOT_DIR}/altcoins.json", "r") as f:
            altcoins = json.load(f)
            for c in altcoins[:50]:  # Top 50
                coins.append({
                    "symbol": c.get("symbol", "").upper(),
                    "name": c.get("name", ""),
                    "market_cap": c.get("market_cap", 0),
                    "volume_24h": 0,
                    "price": 0,
                    "change_24h": 0
                })
    except Exception as e:
        print(f"Altcoins error: {e}", flush=True)
    
    # Read trending for volume
    try:
        with open(f"{BOT_DIR}/trending.json", "r") as f:
            trending = json.load(f)
            for t in trending.get("hot_coins_15plus", []):
                vol_str = t.get("vol_24h", "0")
                if isinstance(vol_str, str):
                    vol = float(vol_str.replace(",", ""))
                else:
                    vol = vol_str
                
                symbol = t.get("symbol", "UNKNOWN").split("-")[0].upper()
                
                found = False
                for c in coins:
                    if c["symbol"] == symbol:
                        c["volume_24h"] = vol
                        c["price"] = t.get("last", 0)
                        c["change_24h"] = t.get("change_24h", 0)
                        found = True
                        break
                if not found:
                    coins.insert(0, {
                        "symbol": symbol,
                        "name": symbol,
                        "market_cap": 0,
                        "volume_24h": vol,
                        "price": t.get("last", 0),
                        "change_24h": t.get("change_24h", 0)
                    })
    except Exception as e:
        print(f"Trending error: {e}", flush=True)
    
    return coins

def detect_volume_spikes(coins_data, threshold=1.5):
    """Detect coins with unusual volume"""
    if not coins_data:
        return []
    
    with_volume = [c for c in coins_data if c.get("volume_24h", 0) > 0]
    
    if not with_volume:
        return []
    
    volumes = [c["volume_24h"] for c in with_volume]
    avg_volume = sum(volumes) / len(volumes)
    
    spikes = []
    for coin in with_volume:
        if coin["volume_24h"] > avg_volume * threshold:
            spikes.append({
                "symbol": coin["symbol"],
                "name": coin["name"],
                "price": coin.get("price", 0),
                "volume_24h": coin["volume_24h"],
                "market_cap": coin.get("market_cap", 0),
                "change_24h": coin.get("change_24h", 0),
                "avg_volume": avg_volume,
                "spike_ratio": coin["volume_24h"] / avg_volume if avg_volume > 0 else 0,
                "timestamp": datetime.now().isoformat()
            })
    
    spikes.sort(key=lambda x: x["spike_ratio"], reverse=True)
    return spikes

def load_whales():
    """Load existing whale alerts"""
    try:
        if os.path.exists(WHALES_FILE):
            with open(WHALES_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"alerts": [], "last_scan": None}

def save_whales(data):
    """Save whale alerts"""
    with open(WHALES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def run_whale_watcher():
    """Main whale watcher loop"""
    print("🐋 Starting Whale Watcher...", flush=True)
    print(f"Running {CYCLES} cycles ({CHECK_INTERVAL//60} min each)", flush=True)
    print("-" * 50, flush=True)
    
    whales_data = load_whales()
    new_alerts = []
    
    for cycle in range(1, CYCLES + 1):
        print(f"\n🔄 Cycle {cycle}/{CYCLES} - {datetime.now().strftime('%H:%M:%S')}", flush=True)
        
        coins_data = get_local_data()
        print(f"DEBUG: Got {len(coins_data)} coins", flush=True)
        
        if coins_data:
            spikes = detect_volume_spikes(coins_data)
            
            print(f"📊 Analyzed {len(coins_data)} coins", flush=True)
            print(f"📈 Found {len(spikes)} volume spikes", flush=True)
            
            for spike in spikes:
                alert_msg = f"🐋 WHALE: {spike['symbol']} volume alert - {spike['spike_ratio']:.1f}x avg"
                if spike.get("volume_24h", 0) > 0:
                    alert_msg += f", ${spike['volume_24h']/1e6:.1f}M 24h"
                print(alert_msg, flush=True)
                new_alerts.append(alert_msg)
                
                exists = any(
                    a.get("symbol") == spike["symbol"] and 
                    a.get("timestamp", "").startswith(spike["timestamp"][:10])
                    for a in whales_data.get("alerts", [])
                )
                
                if not exists:
                    whales_data["alerts"].append(spike)
            
            whales_data["last_scan"] = datetime.now().isoformat()
            save_whales(whales_data)
            
            if spikes:
                print("\n🎯 Top Volume Spikes:", flush=True)
                for i, spike in enumerate(spikes[:5], 1):
                    vol_str = f"${spike['volume_24h']/1e6:.1f}M" if spike.get("volume_24h", 0) > 0 else "N/A"
                    print(f"  {i}. {spike['symbol']}: {spike['spike_ratio']:.1f}x ({vol_str})", flush=True)
        else:
            print("❌ No data available", flush=True)
        
        if cycle < CYCLES:
            print(f"\n⏳ Next check in {CHECK_INTERVAL//60} min...", flush=True)
            time.sleep(CHECK_INTERVAL)
    
    print("\n✅ Whale Watcher completed!", flush=True)
    print(f"📁 Saved to: {WHALES_FILE}", flush=True)
    
    return new_alerts

if __name__ == "__main__":
    run_whale_watcher()
