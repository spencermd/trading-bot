#!/usr/bin/env python3
"""X Scanner - Aggregate social signals for crypto opportunities"""

import json
import os
from datetime import datetime
import requests

def get_reddit_signals():
    """Get trending coins from Reddit"""
    signals = []
    try:
        # CryptoMoonShots
        r = requests.get("https://www.reddit.com/r/CryptoMoonShots/new.json?limit=10", 
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for post in data.get("data", {}).get("children", [])[:5]:
                title = post.get("data", {}).get("title", "")
                # Extract potential coin names (capitalized words, ticker-like)
                words = title.split()
                for word in words:
                    if word.isupper() and len(word) <= 5 and word not in ["AMA", "CEO", "API", "ICO", "DYOR"]:
                        signals.append({"source": "Reddit", "coin": word, "title": title[:50]})
    except Exception as e:
        print(f"Reddit error: {e}")
    return signals

def get_alerts_data():
    """Load existing alerts from bot"""
    try:
        with open("alerts.json") as f:
            return json.load(f)
    except:
        return []

def get_ultra_data():
    """Load existing ultra scan data"""
    try:
        with open("ultra.json") as f:
            return json.load(f)
    except:
        return {}

def scan():
    """Main scan function"""
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Get social signals
    reddit_signals = get_reddit_signals()
    
    # Get existing bot data
    alerts = get_alerts_data()
    ultra = get_ultra_data()
    
    # Combine signals
    opportunities = {
        "timestamp": timestamp,
        "social_signals": reddit_signals,
        "oversold_alerts": alerts,
        "market_data": ultra.get("opportunities", {}),
        "recommendations": ultra.get("recommendations", [])
    }
    
    return opportunities

if __name__ == "__main__":
    result = scan()
    print(json.dumps(result, indent=2))
