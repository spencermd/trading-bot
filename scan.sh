#!/bin/bash
ALERTS_FILE="/home/eldes/polymarket_panic_bot/alerts.json"

scan() {
    echo "=== SCAN $(date '+%Y-%m-%d %H:%M:%S') ==="
    
    # Fetch prices
    RESPONSE=$(curl -s --max-time 10 "https://api.coingecko.com/api/v3/simple/price?ids=pudgy-penguin,popcat,bonk,skate,kaspa&vs_currencies=usd&include_24hr_change=true")
    echo "Response received"
    
    # Check for rate limit
    if echo "$RESPONSE" | grep -q "rate"; then
        echo "Rate limited, skipping scan..."
        return
    fi
    
    echo "$RESPONSE" > /tmp/crypto_scan.json
    
    python3 << PYEOF
import json
import datetime

with open('/tmp/crypto_scan.json', 'r') as f:
    data = json.load(f)

alerts = []
signals = []

coin_map = {
    'pudgy-penguin': 'PENGU',
    'popcat': 'POPCAT', 
    'bonk': 'BONK',
    'skate': 'SKATE',
    'kaspa': 'KCT'
}

for coin, info in data.items():
    price = info.get('usd', 0)
    change = info.get('usd_24h_change', 0)
    
    coin_name = coin_map.get(coin, coin.upper())
    
    print(f"{coin_name}: \${price:.6f} ({change:+.2f}%)")
    
    # Buy signal: down 15%+
    if change <= -15:
        signal = f"🚨 BUY SIGNAL: {coin_name} down {abs(change):.1f}%!"
        signals.append(signal)
        alerts.append({'type': 'BUY', 'coin': coin_name, 'change': round(change, 2), 'price': price, 'time': datetime.datetime.now().isoformat()})
        print(f"  {signal}")
    
    # Take profit: up 50%+
    if change >= 50:
        signal = f"🎯 TAKE PROFIT: {coin_name} up {change:.1f}%!"
        signals.append(signal)
        alerts.append({'type': 'TAKE_PROFIT', 'coin': coin_name, 'change': round(change, 2), 'price': price, 'time': datetime.datetime.now().isoformat()})
        print(f"  {signal}")

# Save alerts
if alerts:
    try:
        with open('$ALERTS_FILE', 'r') as f:
            existing = json.load(f)
    except:
        existing = []
    existing.extend(alerts)
    with open('$ALERTS_FILE', 'w') as f:
        json.dump(existing, f, indent=2)
    print(f"Saved {len(alerts)} alert(s)")
PYEOF
    
    echo ""
}

# Run 7 scans (35 minutes total)
for i in 1 2 3 4 5 6 7; do
    scan
    if [ $i -lt 7 ]; then
        echo "Sleeping 5 minutes until next scan..."
        sleep 300
    fi
done

echo "=== SCANNING COMPLETE ==="
