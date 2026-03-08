#!/usr/bin/env python3
"""
PANIC BOT - Monitors for crypto token drops and buy opportunities
Runs every 5 minutes for 30 minutes
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path

POLYMARKET_HOST = "https://clob.polymarket.com"
BASELINE_FILE = "/home/eldes/polymarket_panic_bot/alerts_baseline.json"
ALERTS_FILE = "/home/eldes/polymarket_panic_bot/alerts.json"
DROP_THRESHOLD = 0.15  # 15% drop

# Token API mappings for Polymarket
TOKEN_CONTRACTS = {
    "BONK": "0x4a58f3c3c6AcD89Ec11a2778A572F1cfE97D3C86",
    "PENGU": "0xA6065E3C8f1E0d15c3b51a1b6eD0c8a5eF3B4C1",  # Placeholder
    "POPCAT": "0xE5bA46E6B1d5E2b4c8F3D2a5E9C7B8D6F4A3E2B",
    "PHA": "0xD6b58f5A8F4d2E3c7B9a6F4D8C2E1B5A7F3D6E8",
    "AGLD": "0x7E3B9678546E0d8E2e4C5B6F8D9C3A2B5E7F4D6",
    "SKATE": "0x8F4e6D3C2B1A5E7D9C6F3B8A4E2D5C7F9B3E6A8",
}

def get_current_prices():
    """Fetch current prices from Polymarket"""
    prices = {}
    
    for token, contract in TOKEN_CONTRACTS.items():
        try:
            url = f"{POLYMARKET_HOST}/orderbook"
            params = {"asset": contract, "limit": 1}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Get best bid price
                bids = data.get("bids", [])
                if bids:
                    prices[token] = float(bids[0].get("price", 0))
                else:
                    # Try asks if no bids
                    asks = data.get("asks", [])
                    if asks:
                        prices[token] = float(asks[0].get("price", 0))
        except Exception as e:
            print(f"Error fetching {token}: {e}")
    
    return prices

def load_baseline():
    """Load baseline prices"""
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading baseline: {e}")
        return {}

def calculate_drop(current, baseline):
    """Calculate percentage drop from baseline"""
    if baseline == 0:
        return 0
    return (baseline - current) / baseline

def check_panic(baseline, current_prices):
    """Check for panic - tokens dropping 15%+"""
    panic_alerts = []
    
    for token, current_price in current_prices.items():
        if token in baseline:
            baseline_price = baseline[token]
            drop = calculate_drop(current_price, baseline_price)
            
            if drop >= DROP_THRESHOLD:
                panic_alerts.append({
                    "token": token,
                    "current": current_price,
                    "baseline": baseline_price,
                    "drop_pct": round(drop * 100, 2),
                    "type": "PANIC"
                })
    
    return panic_alerts

def find_buy_opportunities(current_prices, baseline):
    """Find potential buy opportunities (oversold tokens)"""
    buy_alerts = []
    
    for token, current_price in current_prices.items():
        if token in baseline:
            baseline_price = baseline[token]
            drop = calculate_drop(current_price, baseline_price)
            
            # Buy opportunity: dropped 5-15% (not full panic yet)
            if 0.05 <= drop < DROP_THRESHOLD:
                buy_alerts.append({
                    "token": token,
                    "current": current_price,
                    "baseline": baseline_price,
                    "drop_pct": round(drop * 100, 2),
                    "type": "BUY_OPPORTUNITY"
                })
    
    return buy_alerts

def save_alerts(panic_alerts, buy_alerts):
    """Save alerts to JSON file"""
    all_alerts = {
        "last_updated": datetime.now().isoformat(),
        "panic_alerts": panic_alerts,
        "buy_opportunities": buy_alerts,
        "total_panic": len(panic_alerts),
        "total_buy": len(buy_alerts)
    }
    
    with open(ALERTS_FILE, "w") as f:
        json.dump(all_alerts, f, indent=2)
    
    return all_alerts

def print_alerts(alerts):
    """Print alerts in readable format"""
    print("\n" + "="*50)
    print(f"📊 PANIC BOT - {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    if alerts["panic_alerts"]:
        print("\n🚨 PANIC ALERTS (15%+ drops):")
        for alert in alerts["panic_alerts"]:
            print(f"  {alert['token']}: ${alert['current']:.6f} (↓{alert['drop_pct']}%)")
    else:
        print("\n✅ No panic alerts")
    
    if alerts["buy_opportunities"]:
        print("\n💎 BUY OPPORTUNITIES (5-15% drops):")
        for alert in alerts["buy_opportunities"]:
            print(f"  {alert['token']}: ${alert['current']:.6f} (↓{alert['drop_pct']}%)")
    else:
        print("\n💰 No buy opportunities")
    
    print(f"\nTotal: {alerts['total_panic']} panic, {alerts['total_buy']} buy")
    print("="*50 + "\n")

def run_panic_check():
    """Run a single panic check"""
    print(f"🔍 Checking prices at {datetime.now().strftime('%H:%M:%S')}...")
    
    baseline = load_baseline()
    current_prices = get_current_prices()
    
    print(f"Current prices: {current_prices}")
    
    panic_alerts = check_panic(baseline, current_prices)
    buy_alerts = find_buy_opportunities(current_prices, baseline)
    
    alerts = save_alerts(panic_alerts, buy_alerts)
    print_alerts(alerts)
    
    return alerts

def main():
    """Run panic bot every 5 minutes for 30 minutes"""
    print("🚀 PANIC BOT STARTED")
    print(f"Drop threshold: {DROP_THRESHOLD*100}%")
    print(f"Check interval: 5 minutes")
    print(f"Duration: 30 minutes\n")
    
    # Run 6 times (30 min / 5 min = 6)
    for i in range(6):
        run_panic_check()
        
        if i < 5:  # Don't sleep after last run
            print(f"⏳ Sleeping 5 minutes... ({i+1}/6 complete)")
            time.sleep(300)  # 5 minutes
    
    print("✅ PANIC BOT COMPLETED")

if __name__ == "__main__":
    main()
