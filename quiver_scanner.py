#!/usr/bin/env python3
"""
📊 QUIVER QUANTITATIVE SCANNER
Congress Trading + Insider + Alternative Data
"""

import requests
import json
from datetime import datetime

# Quiver Quantitative data endpoints
QUIVER_SECTIONS = [
    {"name": "Congress Trading", "path": "congresstrading", "url": "https://www.quiverquant.com/congresstrading/"},
    {"name": "Insider Trading", "path": "insiders", "url": "https://www.quiverquant.com/insiders/"},
    {"name": "Trending", "path": "trending", "url": "https://www.quiverquant.com/"},
    {"name": "News", "path": "news", "url": "https://www.quiverquant.com/news/"},
]

# Known high-value politicians to track
HIGH_VALUE_POLITICIANS = [
    "Nancy Pelosi",
    "Marjorie Taylor Greene", 
    "J. D. Vance",
    "Bernie Sanders",
    "Elizabeth Warren",
    "Elon Musk",  # Not a politician but influential
]

def fetch_quiver_news():
    """Fetch latest from Quiver Quantitative"""
    url = "https://www.quiverquant.com/news/"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        
        # Parse for news items
        news_items = []
        
        # Extract ticker symbols (usually $XXXX format)
        import re
        tickers = re.findall(r'\$([A-Z]{2,5})', r.text)
        unique_tickers = list(set(tickers))[:20]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "tickers_mentioned": unique_tickers,
            "source": "quiverquant.com"
        }
    except Exception as e:
        return {"error": str(e)}

def analyze_quiver_data():
    """Main analysis"""
    print(f"\n{'='*60}")
    print(f"📊 QUIVER QUANTITATIVE SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    data = fetch_quiver_news()
    
    if "error" in data:
        print(f"Error: {data['error']}")
        return
    
    print(f"\n🎯 TICKERS FROM QUIVER:")
    for ticker in data.get("tickers_mentioned", [])[:15]:
        print(f"   • {ticker}")
    
    print(f"\n📊 DATA SOURCES AVAILABLE:")
    for section in QUIVER_SECTIONS:
        print(f"   • {section['name']}")
    
    # Save
    with open("quiver_signals.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Saved to quiver_signals.json")
    
    return data

if __name__ == "__main__":
    print("📊 QUIVER QUANTITATIVE SCANNER")
    print("Congress Trading + Insider + Alternative Data\n")
    
    analyze_quiver_data()
