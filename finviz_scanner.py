#!/usr/bin/env python3
"""
📊 FINVIZ SCANNER
Market Overview + Stock Screener from finviz.com
"""

import requests
import re
import json
from datetime import datetime

def fetch_finviz():
    """Fetch from finviz.com"""
    url = "https://finviz.com/"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        
        # Market stats
        stats = {}
        
        # Extract tickers from different sections
        gainers = re.findall(r'>([A-Z]{1,5})</a>.*?(\d+\.\d+)%', r.text)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "market_summary": "Fetched from finviz.com",
            "source": "finviz.com"
        }
    except Exception as e:
        return {"error": str(e)}

def get_finviz_screener():
    """Get various screeners"""
    screeners = [
        {"name": "Top Gainers", "url": "https://finviz.com/screener.ashx?v=340&s=ta_topgainers"},
        {"name": "Top Losers", "url": "https://finviz.com/screener.ashx?v=340&s=ta_toplosers"},
        {"name": "New High", "url": "https://finviz.com/screener.ashx?v=340&s=ta_newhigh"},
        {"name": "New Low", "url": "https://finviz.com/screener.ashx?v=340&s=ta_newlow"},
        {"name": "Overbought", "url": "https://finviz.com/screener.ashx?v=210&s=ta_overbought"},
        {"name": "Oversold", "url": "https://finviz.com/screener.ashx?v=210&s=ta_oversold"},
        {"name": "Unusual Volume", "url": "https://finviz.com/screener.ashx?v=320&s=ta_unusualvolume"},
        {"name": "Insider Buying", "url": "https://finviz.com/screener.ashx?v=340&s=it_latestbuys"},
    ]
    
    return screeners

def analyze_finviz():
    """Main analysis"""
    print(f"\n{'='*60}")
    print(f"📊 FINVIZ SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    screeners = get_finviz_screener()
    
    print(f"\n🎯 FINVIZ SCREENS AVAILABLE:")
    for s in screeners:
        print(f"   • {s['name']}")
    
    data = fetch_finviz()
    
    # Save
    with open("finviz_signals.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "screeners": screeners
        }, f, indent=2)
    
    print(f"\n💾 Saved to finviz_signals.json")
    
    return data

if __name__ == "__main__":
    print("📊 FINVIZ SCANNER\n")
    analyze_finviz()
