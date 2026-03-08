#!/usr/bin/env python3
"""X Scanner - Aggregate social signals for crypto opportunities"""

import json
import os
from datetime import datetime, timezone
import requests

def get_news_signals():
    """Get trending topics from crypto news"""
    signals = []
    topics = []
    try:
        r = requests.get("https://blockworks.co/category/markets", timeout=10)
        if r.status_code == 200:
            # Extract topics from headlines in the HTML
            import re
            headlines = re.findall(r'<a[^>]*>([^<]+)</a>', r.text)
            for h in headlines[:20]:
                h = h.strip()
                if len(h) > 10 and len(h) < 100:
                    signals.append({"source": "blockworks", "topic": h[:80]})
    except Exception as e:
        print(f"News error: {e}")
    return signals

def get_market_opportunities():
    """Load opportunities from existing bot data"""
    opp = {}
    try:
        with open("ultra.json") as f:
            data = json.load(f)
            opp = data.get("opportunities", {})
    except:
        pass
    return opp

def scan():
    """Main scan function"""
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    # Get news/social signals
    news_signals = get_news_signals()
    
    # Get market opportunities from existing bot data
    opportunities = get_market_opportunities()
    
    # Build X-style signal report
    result = {
        "timestamp": timestamp,
        "scan_type": "X_SCANNER",
        "scan_number": 1,
        "social_signals": news_signals[:15],
        "opportunities": {
            "top_gems": opportunities.get("top_gems", []),
            "hot_gainers": opportunities.get("hot_gainers", []),
            "bullish_breakouts": opportunities.get("bullish_breakouts", []),
            "algo_signals": opportunities.get("algo_signals", {}),
            "whale_alerts": opportunities.get("whale_alerts", [])
        },
        "actionable_signals": []
    }
    
    # Generate actionable signals
    if opportunities.get("algo_signals", {}).get("BUY"):
        for coin in opportunities["algo_signals"]["BUY"]:
            result["actionable_signals"].append({
                "type": "ALGO_BUY",
                "coin": coin,
                "source": "technical_analysis"
            })
    
    if opportunities.get("whale_alerts"):
        for whale in opportunities["whale_alerts"][:3]:
            result["actionable_signals"].append({
                "type": "WHALE_ALERT",
                "coin": whale.get("symbol"),
                "spike_ratio": whale.get("spike_ratio"),
                "volume_24h": whale.get("volume_24h")
            })
    
    return result

if __name__ == "__main__":
    result = scan()
    print(json.dumps(result, indent=2))
