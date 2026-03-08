#!/bin/bash
cd /home/eldes/polymarket_panic_bot

for i in 1 2 3; do
  echo "=== Check $i at $(date) ==="
  
  # Get BTC data
  BTC_DATA=$(curl -s "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=1")
  BTC_HIGH=$(echo "$BTC_DATA" | grep -o '"high":[0-9.]*' | tail -1 | cut -d':' -f2)
  BTC_LOW=$(echo "$BTC_DATA" | grep -o '"low":[0-9.]*' | tail -1 | cut -d':' -f2)
  BTC_CLOSE=$(echo "$BTC_DATA" | grep -o '"close":[0-9.]*' | tail -1 | cut -d':' -f2)
  
  # Get ETH data
  ETH_DATA=$(curl -s "https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=USD&limit=1")
  ETH_HIGH=$(echo "$ETH_DATA" | grep -o '"high":[0-9.]*' | tail -1 | cut -d':' -f2)
  ETH_LOW=$(echo "$ETH_DATA" | grep -o '"low":[0-9.]*' | tail -1 | cut -d':' -f2)
  ETH_CLOSE=$(echo "$ETH_DATA" | grep -o '"close":[0-9.]*' | tail -1 | cut -d':' -f2)
  
  # Calculate volatility
  BTC_VOL=$(echo "scale=2; ($BTC_HIGH - $BTC_LOW) / $BTC_CLOSE * 100" | bc)
  ETH_VOL=$(echo "scale=2; ($ETH_HIGH - $ETH_LOW) / $ETH_CLOSE * 100" | bc)
  
  echo "BTC: high=$BTC_HIGH, low=$BTC_LOW, close=$BTC_CLOSE, vol=$BTC_VOL%"
  echo "ETH: high=$ETH_HIGH, low=$ETH_LOW, close=$ETH_CLOSE, vol=$ETH_VOL%"
  
  # Check alerts
  if (( $(echo "$BTC_VOL > 5" | bc -l) )); then
    echo "⚡ VOLATILITY: BTC at ${BTC_VOL}%"
  fi
  if (( $(echo "$ETH_VOL > 5" | bc -l) )); then
    echo "⚡ VOLATILITY: ETH at ${ETH_VOL}%"
  fi
  
  # Save to JSON
  cat > volatility.json << JSON
{
  "last_update": "$(date -Iseconds)",
  "btc": {
    "price": $BTC_CLOSE,
    "volatility": $BTC_VOL,
    "high": $BTC_HIGH,
    "low": $BTC_LOW
  },
  "eth": {
    "price": $ETH_CLOSE,
    "volatility": $ETH_VOL,
    "high": $ETH_HIGH,
    "low": $ETH_LOW
  }
}
JSON
  
  if [ $i -lt 3 ]; then
    echo "Sleeping 12 minutes..."
    sleep 720
  fi
done

echo "=== Monitoring complete ==="
