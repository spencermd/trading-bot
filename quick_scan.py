#!/usr/bin/env python3
"""Quick scanner using Coinbase"""
import requests, time
from datetime import datetime

COINS = [("BTC","BTC-USD"), ("ETH","ETH-USD"), ("SOL","SOL-USD"), ("XRP","XRP-USD"), ("DOGE","DOGE-USD"), ("ADA","ADA-USD")]

def get_price(symbol):
    r = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}/spot", timeout=10)
    return float(r.json()["data"]["amount"])

print(f"🚀 QUICK SCAN @ {datetime.now().strftime('%H:%M:%S')}")
print("="*40)
for name, symbol in COINS:
    try:
        price = get_price(symbol)
        print(f"  {name}: ${price:,.2f}")
    except:
        print(f"  {name}: ERROR")
print("="*40)
