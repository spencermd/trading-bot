#!/usr/bin/env python3
"""Crypto market scanner - monitors BTC, ETH, SOL, XRP, DOGE, ADA, AVAX"""

import json
import time
import os
from datetime import datetime
import requests

# Configuration
COINS = ["bitcoin", "ethereum", "solana", "ripple", "dogecoin", "cardano", "avalanche-2"]
SYMBOLS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "AVAX"]
SIGNALS_FILE = "/home/eldes/polymarket_panic_bot/signals.json"
SCAN_INTERVAL = 60  # seconds
MIN_RUNTIME = 300  # seconds

def load_signals():
    """Load existing signals from file"""
    if os.path.exists(SIGNALS_FILE):
        try:
            with open(SIGNALS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_signals(signals):
    """Save signals to file"""
    with open(SIGNALS_FILE, 'w') as f:
        json.dump(signals, f, indent=2)

def fetch_prices():
    """Fetch current prices from CoinGecko"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error fetching prices: {e}")
        return None

def check_signals(price_data):
    """Check for >5% gain or >10% drop in 24h"""
    signals = []
    
    for coin, symbol in zip(COINS, SYMBOLS):
        if coin in price_data:
            price = price_data[coin]["usd"]
            change_24h = price_data[coin].get("usd_24h_change", 0)
            
            if change_24h > 5:
                signals.append({
                    "symbol": symbol,
                    "type": "GAIN",
                    "change_24h": round(change_24h, 2),
                    "price": price,
                    "timestamp": datetime.now().isoformat()
                })
            elif change_24h < -10:
                signals.append({
                    "symbol": symbol,
                    "type": "DROP",
                    "change_24h": round(change_24h, 2),
                    "price": price,
                    "timestamp": datetime.now().isoformat()
                })
    
    return signals

def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Crypto scanner started")
    print(f"Monitoring: {', '.join(SYMBOLS)}")
    print(f"Signals: >5% gain or >10% drop in 24h")
    print("-" * 50)
    
    start_time = time.time()
    all_signals = load_signals()
    new_signals_count = 0
    
    while True:
        elapsed = time.time() - start_time
        
        price_data = fetch_prices()
        
        if price_data:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Prices (24h change):")
            
            for coin, symbol in zip(COINS, SYMBOLS):
                if coin in price_data:
                    price = price_data[coin]["usd"]
                    change = price_data[coin].get("usd_24h_change", 0)
                    change_str = f"{change:+.2f}%"
                    print(f"  {symbol}: ${price:,.2f} ({change_str})")
            
            # Check for signals
            signals = check_signals(price_data)
            
            if signals:
                print("\n*** SIGNALS DETECTED ***")
                for sig in signals:
                    print(f"  {sig['symbol']}: {sig['type']} - {sig['change_24h']}% ({sig['price']})")
                    all_signals.append(sig)
                    new_signals_count += 1
                
                save_signals(all_signals)
        
        # Check if we've run long enough
        if elapsed >= MIN_RUNTIME:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Minimum runtime ({MIN_RUNTIME}s) reached. Scanner stopping.")
            print(f"Total signals saved: {new_signals_count}")
            break
        
        # Wait for next scan
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
