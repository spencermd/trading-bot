#!/usr/bin/env python3
"""
💰 PHANTOM TRADING DASHBOARD
Ready-to-execute trade tickets with algo signals
"""

import requests
import json
import time
from datetime import datetime

# Configuration
TRADE_AMOUNT = 100  # USD per trade
STOP_LOSS_PCT = 10  # 10% stop loss
TAKE_PROFIT_PCT = 30  # 30% take profit

# Solana tokens to trade (add your gems here)
WATCHLIST = [
    {"id": "popcat", "symbol": "POPCAT", "name": "Popcat"},
    {"id": "bonk", "symbol": "BONK", "name": "Bonk"},
    {"id": "wif", "symbol": "WIF", "name": "WIF"},
    {"id": "chill", "symbol": "CHILL", "name": "Chill"},
]

def get_market_data():
    """Get live prices and market data"""
    try:
        ids = ",".join([t["id"] for t in WATCHLIST])
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": ids,
            "order": "market_cap_desc",
            "sparkline": False
        }
        r = requests.get(url, params=params, timeout=30)
        return r.json() if r.status_code == 200 else []
    except:
        return []

def calculate_signal(change_24h, mcap):
    """Calculate algo signal"""
    score = 0
    
    # RSI-like: big drops
    if change_24h < -15:
        score += 2
    elif change_24h < -10:
        score += 1
    
    # Cap advantage
    if mcap < 10_000_000:
        score += 2
    elif mcap < 100_000_000:
        score += 1
    
    if score >= 3:
        return "STRONG_BUY"
    elif score >= 1:
        return "BUY"
    return "WATCH"

def generate_trade_ticket(token_data):
    """Generate a trade ticket"""
    price = token_data.get("current_price", 0)
    mcap = token_data.get("market_cap", 0)
    change = token_data.get("price_change_percentage_24h", 0)
    symbol = token_data.get("symbol", "").upper()
    
    # Calculate position
    tokens = TRADE_AMOUNT / price if price > 0 else 0
    
    # Price levels
    entry = price
    stop = price * (1 - STOP_LOSS_PCT/100)
    target = price * (1 + TAKE_PROFIT_PCT/100)
    
    # Signal
    signal = calculate_signal(change, mcap)
    
    return {
        "token": token_data.get("name", symbol),
        "symbol": symbol,
        "price": price,
        "mcap": mcap,
        "change_24h": change,
        "signal": signal,
        "position_usd": TRADE_AMOUNT,
        "tokens_received": tokens,
        "entry": entry,
        "stop_loss": stop,
        "take_profit": target,
        "risk_reward": f"1:{TAKE_PROFIT_PCT/STOP_LOSS_PCT}"
    }

def print_dashboard():
    """Print trading dashboard"""
    print(f"\n{'='*65}")
    print(f"💰 PHANTOM TRADING DASHBOARD - {datetime.now().strftime('%H:%M:%S UTC')}")
    print("="*65)
    
    coins = get_market_data()
    
    if not coins:
        print("⚠️ Could not fetch live data")
        return []
    
    tickets = []
    buys = []
    
    for coin in coins:
        ticket = generate_trade_ticket(coin)
        tickets.append(ticket)
        
        if "BUY" in ticket["signal"]:
            buys.append(ticket)
            
            emoji = "🔥" if "STRONG" in ticket["signal"] else "🟢"
            print(f"\n{emoji} {ticket['token']} ({ticket['symbol']}) - {ticket['signal']}")
            print(f"   Price: ${ticket['price']:.6f}")
            print(f"   MCap: ${ticket['mcap']:,}")
            print(f"   24h: {ticket['change_24h']:+.1f}%")
            print(f"   ")
            print(f"   💵 BUY: ${ticket['position_usd']} → {ticket['tokens_received']:,.0f} {ticket['symbol']}")
            print(f"   📈 Entry: ${ticket['entry']:.6f}")
            print(f"   🛡️ Stop: ${ticket['stop_loss']:.6f} (-{STOP_LOSS_PCT}%)")
            print(f"   🎯 Target: ${ticket['take_profit']:.6f} (+{TAKE_PROFIT_PCT}%)")
            print(f"   📊 R:R = {ticket['risk_reward']}")
        else:
            print(f"\n🟡 {ticket['token']} ({ticket['symbol']}) - {ticket['signal']}")
            print(f"   ${ticket['price']:.6f} | {ticket['change_24h']:+.1f}% | MCap: ${ticket['mcap']:,}")
    
    # Summary
    print(f"\n{'='*65}")
    if buys:
        print(f"🎯 {len(buys)} BUY SIGNALS READY TO EXECUTE")
        for b in buys:
            print(f"   {b['symbol']}: ${b['position_usd']} → {b['tokens_received']:,.0f} tokens")
    else:
        print("😴 No buy signals - watching for opportunities")
    print("="*65)
    
    # Save
    with open("trade_tickets.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "tickets": tickets,
            "signals": buys
        }, f, indent=2)
    
    return buys

if __name__ == "__main__":
    while True:
        print_dashboard()
        time.sleep(300)  # Check every 5 minutes
