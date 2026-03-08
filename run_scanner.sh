#!/bin/bash
# Market Scanner - Runs every 10 minutes for 60 minutes
# Finds coins up 20%+ in 24h

TRENDING_FILE="/home/eldes/polymarket_panic_bot/trending.json"
SCAN_SCRIPT="/home/eldes/polymarket_panic_bot/scan_once.py"

# Create the scan script if it doesn't exist
cat > $SCAN_SCRIPT << 'EOF'
import json
import urllib.request
import ssl
import sys
from datetime import datetime

def scan():
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=30, context=ctx)
        data = json.loads(response.read().decode())
        
        trending = []
        for coin in data:
            change = coin.get('price_change_percentage_24h') or 0
            if change >= 20:
                trending.append({
                    'symbol': coin.get('symbol'),
                    'name': coin.get('name'),
                    'price_change_percentage_24h': change,
                })
        
        return trending
        
    except Exception as e:
        print(f"Error: {e}")
        return []

coins = scan()
print(json.dumps({"last_scan": datetime.now().isoformat(), "coins": coins}))
EOF

echo "🚀 Starting Market Scanner"
echo "⏱️  Scanning every 10 minutes for 60 minutes"
echo "📁 Output: $TRENDING_FILE"
echo "---"

for i in 1 2 3 4 5 6; do
    echo "🔍 Scan #$i at $(date +%H:%M:%S)"
    
    # Run the scan and save to file
    python3 $SCAN_SCRIPT > $TRENDING_FILE
    
    # Check for 20%+ gainers and print
    coins=$(python3 -c "import json; d=json.load(open('$TRENDING_FILE')); print(len(d['coins']))")
    
    if [ "$coins" -gt 0 ]; then
        python3 -c "import json; d=json.load(open('$TRENDING_FILE')); [print(f\"🚨 TRENDING: {c['name']} ({c['symbol'].upper()}) +{c['price_change_percentage_24h']:.2f}%\") for c in d['coins']]"
    else
        echo "📊 No coins up 20%+ in 24h found"
    fi
    
    if [ $i -lt 6 ]; then
        echo "⏳ Waiting 10 minutes..."
        sleep 600
    fi
done

echo "✅ Completed 6 scans (60 minutes)"
