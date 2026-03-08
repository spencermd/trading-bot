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
