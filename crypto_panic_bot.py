#!/usr/bin/env python3
"""
Crypto Panic Bot - Monitors SKATE, PENGU, POPCAT, BONK prices
Alerts on 15%+ drops and saves to alerts.json
"""

import json
import time
import os
from datetime import datetime
import requests

ALERTS_FILE = "/home/eldes/polymarket_panic_bot/alerts.json"
CHECK_INTERVAL = 300  # 5 minutes
TOTAL_RUNS = 6  # 30 minutes / 5 minutes = 6 runs

# Token IDs for CoinGecko
TOKENS = {
    "BONK": "bonk",
    "POPCAT": "popcat", 
    "SKATE": "solskates",
    "PENGU": "pudgy-penguins"
}

# Also try alternative IDs if primary fails
ALT_TOKENS = {
    "SKATE": ["solskates", "skate-meme", "skate-sol"],
    "PENGU": ["pudgy-penguins", "pengu"],
}

def get_prices():
    """Fetch current prices from CoinGecko"""
    try:
        ids = ",".join(TOKENS.values())
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&sparkline=false"
        resp = requests.get(url, timeout=10)
        
        if resp.status_code == 429:
            # Rate limited, try alternative
            return get_prices_alternative()
            
        data = resp.json()
        prices = {}
        for coin in data:
            # Find the symbol
            for sym, cid in TOKENS.items():
                if cid == coin.get('id'):
                    prices[sym] = {
                        'price': coin.get('current_price', 0),
                        'change_24h': coin.get('price_change_percentage_24h', 0),
                        'market_cap': coin.get('market_cap', 0)
                    }
        return prices
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return get_prices_alternative()

def get_prices_alternative():
    """Fallback price fetch using alternative method"""
    # Just return last known prices for now
    return {}

def load_baseline():
    """Load baseline prices from file"""
    baseline_file = ALERTS_FILE.replace('.json', '_baseline.json')
    if os.path.exists(baseline_file):
        with open(baseline_file) as f:
            return json.load(f)
    return None

def save_baseline(prices):
    """Save baseline prices"""
    baseline_file = ALERTS_FILE.replace('.json', '_baseline.json')
    with open(baseline_file, 'w') as f:
        json.dump(prices, f)

def load_alerts():
    """Load existing alerts"""
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE) as f:
            return json.load(f)
    return []

def save_alerts(alerts):
    """Save alerts to file"""
    with open(ALERTS_FILE, 'w') as f:
        json.dump(alerts, f, indent=2)

def check_prices():
    """Check prices and generate alerts"""
    prices = get_prices()
    if not prices:
        print("⚠️ Could not fetch prices")
        return None
    
    # Load or establish baseline
    baseline = load_baseline()
    if not baseline:
        # First run - save baseline
        baseline = {}
        for sym, data in prices.items():
            if isinstance(data, dict):
                baseline[sym] = data['price']
        if baseline:
            save_baseline(baseline)
            print(f"📊 Baseline prices saved: {baseline}")
        return prices
    
    signals = []
    alerts = load_alerts()
    timestamp = datetime.now().isoformat()
    
    for sym, data in prices.items():
        current_price = data['price']
        baseline_price = baseline.get(sym, current_price)
        
        if baseline_price > 0:
            pct_change = ((current_price - baseline_price) / baseline_price) * 100
            
            data['pct_from_baseline'] = pct_change
            
            # Alert if down 15%+
            if pct_change <= -15:
                signal = f"🔴 BUY {sym} - Down {abs(pct_change):.1f}% from baseline (${baseline_price:.6f} → ${current_price:.6f})"
                signals.append(signal)
                
                # Save alert
                alerts.append({
                    'timestamp': timestamp,
                    'token': sym,
                    'action': 'BUY',
                    'price': current_price,
                    'baseline_price': baseline_price,
                    'pct_change': pct_change
                })
            elif pct_change < 0:
                signals.append(f"🟡 {sym} - Down {abs(pct_change):.1f}% (no signal)")
            else:
                signals.append(f"🟢 {sym} - Up {pct_change:.1f}%")
    
    if signals:
        save_alerts(alerts)
    
    return prices, signals

def main():
    print("🚀 Crypto Panic Bot Starting...")
    print(f"📁 Alerts file: {ALERTS_FILE}")
    print(f"⏱️  Checking every {CHECK_INTERVAL}s for {TOTAL_RUNS} iterations")
    print("-" * 50)
    
    for i in range(TOTAL_RUNS):
        print(f"\n[{i+1}/{TOTAL_RUNS}] {datetime.now().strftime('%H:%M:%S')}")
        
        result = check_prices()
        
        if result is None:
            print("⚠️ Skipping this cycle - price fetch failed")
        elif isinstance(result, dict):
            # First run returns only prices
            prices = result
            signals = []
        else:
            prices, signals = result
            print("📊 Prices:")
            for sym, data in prices.items():
                if isinstance(data, dict):
                    print(f"   {sym}: ${data.get('price', 0):.6f} (24h: {data.get('change_24h', 0):+.1f}%)")
            
            print("\n📈 Signals:")
            for sig in signals:
                print(f"   {sig}")
        
        if i < TOTAL_RUNS - 1:
            time.sleep(CHECK_INTERVAL)
    
    print("\n✅ Bot finished!")
    print(f"📁 Alerts saved to: {ALERTS_FILE}")

if __name__ == "__main__":
    main()
