#!/usr/bin/env python3
"""
💎 ACTIVE POSITION MANAGER
- Scans for new gems periodically
- Pre-set buy/sell levels
- Alerts when action needed
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

# Configuration
WATCHLIST_FILE = "watchlist.json"
POSITIONS_FILE = "positions.json"
ALERTS_FILE = "alerts.json"
SCAN_INTERVAL = 300  # 5 minutes

# Default buy/sell levels (can be customized per token)
DEFAULT_STRATEGY = {
    "buy_trigger": -15,  # Buy when 15%+ drop
    "take_profit_1": 15,  # Sell 25% at +15%
    "take_profit_2": 30,  # Sell 25% at +30%
    "take_profit_3": 50,  # Sell remaining at +50%
    "stop_loss": -10,  # Stop out at -10%
}

# Watchlist - gems to monitor
DEFAULT_WATCHLIST = [
    {"id": "popcat", "symbol": "POPCAT", "name": "Popcat", "strategy": DEFAULT_STRATEGY},
    {"id": "bonk", "symbol": "BONK", "name": "Bonk", "strategy": DEFAULT_STRATEGY},
    {"id": "wif", "symbol": "WIF", "name": "WIF", "strategy": DEFAULT_STRATEGY},
    {"id": "goatse", "symbol": "GOAT", "name": "Goat", "strategy": DEFAULT_STRATEGY},
    {"id": "chill", "symbol": "CHILL", "name": "Chill", "strategy": DEFAULT_STRATEGY},
    {"id": "meow", "symbol": "MEOW", "name": "Meow", "strategy": DEFAULT_STRATEGY},
    {"id": "boden", "symbol": "BODEN", "name": "Jeo Boden", "strategy": DEFAULT_STRATEGY},
    {"id": "drift", "symbol": "DRIFT", "name": "Drift", "strategy": DEFAULT_STRATEGY},
]

def load_json(filepath, default):
    """Load JSON file or return default"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json(filepath, data):
    """Save to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_prices(token_ids):
    """Get live prices"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(token_ids),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true"
        }
        r = requests.get(url, params=params, timeout=15)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def analyze_position(token, data, strategy):
    """Analyze a position and generate alerts"""
    if token["id"] not in data:
        return None
    
    current = data[token["id"]]
    price = current.get("usd", 0)
    change = current.get("usd_24h_change", 0) or 0
    mcap = current.get("usd_market_cap", 0)
    
    alerts = []
    
    # Check buy trigger
    if change <= strategy["buy_trigger"]:
        alerts.append({
            "type": "BUY",
            "message": f"🚀 BUY SIGNAL! {token['symbol']} down {change:.1f}%",
            "price": price,
            "change": change,
            "action": f"Buy {token['symbol']} now! Entry: ${price:.6f}"
        })
    
    # Check take profit levels
    # Check stop loss
    
    return {
        "token": token["symbol"],
        "name": token["name"],
        "price": price,
        "change_24h": change,
        "mcap": mcap,
        "alerts": alerts
    }

def scan_watchlist():
    """Main scanning function"""
    print(f"\n{'='*60}")
    print(f"🔍 POSITION SCANNER - {datetime.now().strftime('%H:%M:%S UTC')}")
    print("="*60)
    
    # Load watchlist
    watchlist = load_json(WATCHLIST_FILE, DEFAULT_WATCHLIST)
    
    # Get prices
    token_ids = [t["id"] for t in watchlist]
    prices = get_prices(token_ids)
    
    if not prices:
        print("⚠️ Could not fetch prices")
        return
    
    all_alerts = []
    signals = []
    
    for token in watchlist:
        analysis = analyze_position(token, prices, token.get("strategy", DEFAULT_STRATEGY))
        
        if analysis:
            change = analysis["change_24h"]
            symbol = token["symbol"]
            
            # Determine signal
            if change <= -15:
                signal = "BUY"
                emoji = "🔥"
            elif change <= -10:
                signal = "WATCH_BUY"
                emoji = "🟢"
            elif change >= 50:
                signal = "TAKE_PROFIT"
                emoji = "🎯"
            else:
                signal = "HOLD"
                emoji = "🟡"
            
            print(f"{emoji} {symbol}: ${analysis['price']:.6f} ({change:+.1f}%) → {signal}")
            
            if analysis["alerts"]:
                all_alerts.extend(analysis["alerts"])
                signals.append(analysis)
    
    print("-"*60)
    
    # Save current state
    state = {
        "timestamp": datetime.now().isoformat(),
        "watchlist": [{"symbol": t["symbol"], "price": prices.get(t["id"], {}).get("usd", 0), 
                      "change": prices.get(t["id"], {}).get("usd_24h_change", 0)} 
                     for t in watchlist]
    }
    save_json("scanner_state.json", state)
    
    # Save alerts
    if all_alerts:
        print(f"\n🚨 {len(all_alerts)} ALERTS:")
        for alert in all_alerts:
            print(f"   {alert['message']}")
        save_json(ALERTS_FILE, {"alerts": all_alerts, "timestamp": datetime.now().isoformat()})
    else:
        print("✅ No action needed")
    
    return all_alerts

def add_to_watchlist(token_id, symbol):
    """Add a new token to watchlist"""
    watchlist = load_json(WATCHLIST_FILE, DEFAULT_WATCHLIST)
    
    # Check if already exists
    if any(t["id"] == token_id for t in watchlist):
        return f"{symbol} already in watchlist"
    
    watchlist.append({
        "id": token_id,
        "symbol": symbol.upper(),
        "name": symbol.title(),
        "strategy": DEFAULT_STRATEGY
    })
    
    save_json(WATCHLIST_FILE, watchlist)
    return f"Added {symbol} to watchlist"

if __name__ == "__main__":
    print("💎 ACTIVE POSITION MANAGER")
    print(f"Scanning every {SCAN_INTERVAL/60:.0f} minutes\n")
    
    # Initial save of watchlist
    save_json(WATCHLIST_FILE, DEFAULT_WATCHLIST)
    
    while True:
        scan_watchlist()
        time.sleep(SCAN_INTERVAL)
