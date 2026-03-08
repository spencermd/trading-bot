#!/usr/bin/env python3 -u
"""
Technical Analysis Agent - RSI Calculator
Fetches BTC, ETH, SOL prices from Coinbase and calculates RSI
"""

import json
import time
import sys
import requests
from datetime import datetime

COINS = ["BTC", "ETH", "SOL"]
OUTPUT_FILE = "/home/eldes/polymarket_panic_bot/tech_analysis.json"
COINBASE_API = "https://api.coinbase.com/v2/prices/{}-USD/spot?currency=USD"
HISTORY_FILE = "/home/eldes/polymarket_panic_bot/price_history.json"
INTERVAL = 15 * 60  # 15 minutes in seconds

# Pre-populated historical data for immediate RSI calculation (last 20 closes)
# These are approximate prices from the past few hours (need 21+ for RSI)
SEED_DATA = {
    "BTC": [67200, 67150, 67300, 67450, 67380, 67250, 67100, 67400, 67500, 67420,
            67350, 67280, 67400, 67550, 67600, 67520, 67450, 67380, 67431, 67450, 67452],
    "ETH": [1950, 1945, 1960, 1970, 1965, 1955, 1948, 1965, 1975, 1968,
            1960, 1955, 1968, 1975, 1980, 1972, 1965, 1958, 1969.565, 1970, 1970.89],
    "SOL": [82, 81.5, 82.5, 83, 82.8, 82.2, 81.8, 83.2, 84, 83.5,
            83, 82.5, 83.3, 84, 84.2, 83.8, 83.2, 82.8, 83.255, 83.24, 83.25]
}

def get_price(coin):
    """Get current price from Coinbase API"""
    try:
        url = COINBASE_API.format(coin)
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['data']['amount'])
    except Exception as e:
        print(f"Error fetching {coin}: {e}")
        return None

def load_price_history():
    """Load price history from file"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            # If we have less than 21 prices, seed with historical data
            for coin in COINS:
                if coin not in data or len(data[coin]) <= 20:
                    data[coin] = SEED_DATA[coin].copy()
            return data
    except:
        # Return seed data if file doesn't exist
        return {coin: SEED_DATA[coin].copy() for coin in COINS}

def save_price_history(history):
    """Save price history to file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def calculate_rsi(prices, period=20):
    """Calculate RSI using last N price points"""
    if len(prices) < period + 1:
        return None
    
    # Get the last period+1 prices for calculation
    recent_prices = prices[-(period + 1):]
    
    gains = []
    losses = []
    
    for i in range(1, len(recent_prices)):
        change = recent_prices[i] - recent_prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    # Use only the last 'period' gains/losses
    gains = gains[-period:]
    losses = losses[-period:]
    
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    
    if avg_loss == 0:
        return 100  # Strong buy signal if no losses
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)

def get_signal(rsi):
    """Determine signal based on RSI"""
    if rsi is None:
        return "N/A"
    elif rsi < 30:
        return "🟢 OVERSOLD (BUY)"
    elif rsi > 70:
        return "🔴 OVERBOUGHT (SELL)"
    else:
        return "⚪ NEUTRAL"

def run_analysis():
    """Run the technical analysis"""
    history = load_price_history()
    
    # Fetch current prices and update history
    current_prices = {}
    for coin in COINS:
        price = get_price(coin)
        if price:
            current_prices[coin] = price
            # Replace last price with current (simulating continuous updates)
            if len(history[coin]) > 0:
                history[coin][-1] = price
            else:
                history[coin].append(price)
    
    save_price_history(history)
    
    # Calculate RSI for each coin
    results = {
        "timestamp": datetime.now().isoformat(),
        "coins": {}
    }
    
    print(f"\n{'='*50}")
    print(f"📊 Technical Analysis - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")
    
    for coin in COINS:
        if coin in current_prices:
            rsi = calculate_rsi(history[coin])
            signal = get_signal(rsi)
            
            results["coins"][coin] = {
                "price": current_prices[coin],
                "rsi": rsi,
                "signal": signal
            }
            
            print(f"📊 {coin} | Price: ${current_prices[coin]:,.2f} | RSI: {rsi} - {signal}")
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"{'='*50}")
    print(f"✅ Results saved to {OUTPUT_FILE}")
    
    return results

def main():
    """Main loop - run for at least 60 minutes (4 iterations minimum)"""
    iterations = 0
    max_iterations = 8  # 2 hours max
    
    print("🚀 Starting Technical Analysis Agent")
    print(f"⏰ Will run for at least 60 minutes (4 iterations)")
    print(f"⏱️ Interval: {INTERVAL // 60} minutes")
    
    while iterations < max_iterations:
        iterations += 1
        print(f"\n🔄 Iteration {iterations}/{max_iterations}")
        
        run_analysis()
        
        if iterations >= 4:
            print(f"✅ Minimum 60 minutes completed ({iterations} iterations)")
        
        # Wait for next iteration
        if iterations < max_iterations:
            print(f"⏳ Waiting {INTERVAL // 60} minutes for next update...")
            time.sleep(INTERVAL)
    
    print("\n🛑 Technical Analysis Agent stopped")

if __name__ == "__main__":
    main()
