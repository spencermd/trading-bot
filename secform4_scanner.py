#!/usr/bin/env python3
"""
📋 SEC FORM 4 SCANNER
Real-time insider trading from secform4.com
"""

import requests
import re
import json
from datetime import datetime

def fetch_secform4():
    """Fetch latest from secform4.com"""
    # Their main pages
    urls = [
        "https://www.secform4.com/all-buys",
        "https://www.secform4.com/all-sells"
    ]
    
    all_tickers = []
    
    for url in urls:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)
            
            # Extract tickers
            tickers = re.findall(r'>([A-Z]{1,5})</a>', r.text)
            all_tickers.extend(tickers)
        except:
            pass
    
    # Get unique
    unique = list(set(all_tickers))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "tickers": unique[:20],
        "source": "secform4.com"
    }

def analyze_secform4():
    """Main analysis"""
    print(f"\n{'='*60}")
    print(f"📋 SEC FORM 4 SCANNER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    data = fetch_secform4()
    
    print(f"\n🎯 TICKERS WITH INSIDER ACTIVITY:")
    for t in data.get("tickers", [])[:15]:
        print(f"   • {t}")
    
    # Save
    with open("secform4_signals.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Saved to secform4_signals.json")
    
    return data

if __name__ == "__main__":
    print("📋 SEC FORM 4 SCANNER\n")
    analyze_secform4()
