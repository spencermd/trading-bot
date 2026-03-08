#!/usr/bin/env python3
"""
🤖 TRADING DESK COORDINATOR
Polls agent outputs and posts to Discord
"""

import json
import time
import os
from datetime import datetime

# Discord channel
CHANNEL_ID = "1479960846544408646"
GUILD_ID = "1477766404529852598"

BASE_DIR = "/home/eldes/polymarket_panic_bot"

# Track last known state to detect changes
LAST_STATE_FILE = "coordinator_state.json"

# Files to monitor
MONITOR_FILES = {
    "alerts.json": "🚨 ALERT",
    "new_gems.json": "💎 NEW GEMS",
    "tech_analysis.json": "📊 TECH ANALYSIS",
    "trending.json": "🔥 TRENDING",
    "algo_signals.json": "📈 ALGO SIGNALS"
}

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return None

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def get_state():
    return load_json(os.path.join(BASE_DIR, LAST_STATE_FILE)) or {}

def save_state(state):
    save_json(os.path.join(BASE_DIR, LAST_STATE_FILE), state)

def check_for_changes():
    """Check all monitored files for changes"""
    changes = []
    current_state = get_state()
    new_state = {}
    
    for filename, alert_type in MONITOR_FILES.items():
        filepath = os.path.join(BASE_DIR, filename)
        data = load_json(filepath)
        
        if data is None:
            new_state[filename] = None
            continue
        
        # Convert to string for comparison
        data_str = json.dumps(data, sort_keys=True)
        new_state[filename] = data_str
        
        # Check if changed
        last_state = current_state.get(filename)
        if last_state != data_str:
            changes.append({
                "type": alert_type,
                "filename": filename,
                "data": data
            })
    
    save_state(new_state)
    return changes

def format_alert(change):
    """Format alert data for Discord"""
    alert_type = change["type"]
    data = change["data"]
    
    if alert_type == "🚨 ALERT":
        if not data.get("alerts"):
            return None
        return f"🚨 **{alert_type}**\n" + "\n".join([a.get("message", "") for a in data["alerts"]])
    
    elif alert_type == "💎 NEW GEMS":
        gems = data if isinstance(data, list) else data.get("gems", [])
        if not gems:
            return None
        # Get top 3
        top = gems[:3]
        msg = "💎 **NEW GEMS FOUND**\n"
        for g in top:
            name = g.get("symbol", g.get("name", "?"))
            change = g.get("price_change_24h", g.get("change", 0))
            mcap = g.get("market_cap", 0)
            msg += f"• {name}: {change:+.1f}% (${mcap/1000:.0f}K)\n"
        return msg
    
    elif alert_type == "📊 TECH ANALYSIS":
        coins = data.get("coins", {}) if isinstance(data, dict) else {}
        if not coins:
            return None
        msg = "📊 **TECHNICAL ANALYSIS**\n"
        for coin, info in coins.items():
            rsi = info.get("rsi", 0)
            signal = info.get("signal", "")
            price = info.get("price", 0)
            msg += f"• {coin}: ${price:,.0f} RSI:{rsi:.0f} {signal}\n"
        return msg
    
    elif alert_type == "🔥 TRENDING":
        coins = data.get("coins", []) if isinstance(data, dict) else data
        if not coins:
            return None
        msg = "🔥 **TRENDING**\n"
        for c in coins[:3]:
            name = c.get("symbol", c.get("name", "?"))
            change = c.get("price_change_percentage_24h", 0)
            msg += f"• {name}: +{change:.1f}%\n"
        return msg
    
    elif alert_type == "📈 ALGO SIGNALS":
        signals = data.get("signals", []) if isinstance(data, dict) else data
        if not signals:
            return None
        msg = "📈 **ALGO SIGNALS**\n"
        for s in signals[:3]:
            sym = s.get("symbol", "?")
            action = s.get("action", "?")
            msg += f"• {sym}: {action}\n"
        return msg
    
    return None

def post_to_discord(message):
    """Post message to Discord"""
    os.system(f'''
curl -s -X POST "https://discord.com/api/v10/channels/{CHANNEL_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bot $(cat /home/eldes/.openclaw/config.yaml 2>/dev/null | grep -i token | cut -d' ' -f2)" \
  -d '{{"content": "{message}"}}'
''')

def main():
    print("🤖 COORDINATOR STARTED")
    print(f"Monitoring: {', '.join(MONITOR_FILES.keys())}")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            changes = check_for_changes()
            
            if changes:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Changes detected!")
                
                for change in changes:
                    message = format_alert(change)
                    if message:
                        print(f"Posting: {message[:100]}...")
                        # Uncomment to post to Discord:
                        # post_to_discord(message)
            
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            print("\n🤖 Coordinator stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
