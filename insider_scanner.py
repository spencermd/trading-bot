#!/usr/bin/env python3
"""
📈 INSIDER TRADING SCANNER
Monitors openinsider.com for SEC Form 4 insider trades
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def parse_insider_trades():
    """Fetch and parse insider trades from openinsider.com"""
    url = "http://openinsider.com/screener"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        html = r.text
        
        # Parse the data - looking for recent insider buys (P) and sells (S)
        trades = []
        
        # Look for ticker symbols (they appear as links)
        ticker_pattern = r'>/([A-Z]{1,5})</a>'
        tickers = re.findall(ticker_pattern, html)
        
        # Look for purchase (P) and sale (S) indicators
        purchase_pattern = r'P.*?\$(\d+\.\d+)'
        sale_pattern = r'S.*?\$(\d+\.\d+)'
        
        purchases = re.findall(purchase_pattern, html)
        sales = re.findall(sale_pattern, html)
        
        # Get unique tickers
        unique_tickers = list(set(tickers))[:20]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "tickers": unique_tickers,
            "purchase_count": len(purchases),
            "sale_count": len(sales),
            "data_source": "openinsider.com"
        }
    except Exception as e:
        return {"error": str(e)}

def get_insider_news():
    """Get latest insider trading news"""
    url = "http://openinsider.com/"
    
    try:
        r = requests.get(url, timeout=15)
        return {"status": "fetched", "url": url}
    except Exception as e:
        return {"error": str(e)}

def analyze_insider_sentiment():
    """Analyze insider trading sentiment"""
    data = parse_insider_trades()
    
    print(f"\n{'='*60}")
    print(f"📈 INSIDER TRADING SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    if "error" in data:
        print(f"Error: {data['error']}")
        return
    
    print(f"\n📊 INSIDER ACTIVITY:")
    print(f"   Purchases detected: {data.get('purchase_count', 0)}")
    print(f"   Sales detected: {data.get('sale_count', 0)}")
    
    print(f"\n🎯 TICKERS WITH INSIDER ACTIVITY:")
    for ticker in data.get("tickers", [])[:15]:
        print(f"   • {ticker}")
    
    # Save
    with open("insider_signals.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Saved to insider_signals.json")
    
    return data

if __name__ == "__main__":
    print("📈 INSIDER TRADING SCANNER")
    print("Monitoring SEC Form 4 filings from openinsider.com\n")
    
    analyze_insider_sentiment()
