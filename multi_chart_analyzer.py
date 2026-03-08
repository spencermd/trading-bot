#!/usr/bin/env python3
"""
📊 MULTI-CHART ANALYZER
Analyzes ANY token - no functional fixedness
"""

import requests
import json
import time
import random
from datetime import datetime

# WATCHLIST - Add ANY token here
WATCHLIST = [
    # Low Cap Gems (from our discoveries)
    {"id": "skate", "symbol": "SKATE", "name": "Skate", "source": "gem"},
    {"id": "om", "symbol": "OM", "name": "OM", "source": "gem"},
    {"id": "bard", "symbol": "BARD", "name": "Bard", "source": "gem"},
    {"id": "siren", "symbol": "SIREN", "name": "Siren", "source": "gem"},
    {"id": "pha", "symbol": "PHA", "name": "Phala", "source": "gem"},
    {"id": "pepe", "symbol": "PEPE", "name": "Pepe", "source": "memetic"},
    {"id": "bonk", "symbol": "BONK", "name": "Bonk", "source": "solana"},
    {"id": "wif", "symbol": "WIF", "name": "WIF", "source": "solana"},
    {"id": "popcat", "symbol": "POPCAT", "name": "Popcat", "source": "solana"},
    {"id": "pengu", "symbol": "PENGU", "name": "Pudgy Penguins", "source": "memetic"},
    # Large Cap
    {"id": "bitcoin", "symbol": "BTC", "name": "Bitcoin", "source": "large"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum", "source": "large"},
    {"id": "solana", "symbol": "SOL", "name": "Solana", "source": "large"},
    {"id": "dogecoin", "symbol": "DOGE", "name": "Dogecoin", "source": "large"},
    {"id": "ripple", "symbol": "XRP", "name": "XRP", "source": "large"},
    # DeFi
    {"id": "aave", "symbol": "AAVE", "name": "Aave", "source": "defi"},
    {"id": "uniswap", "symbol": "UNI", "name": "Uniswap", "source": "defi"},
    {"id": "maker", "symbol": "MKR", "name": "Maker", "source": "defi"},
    # AI/Tech
    {"id": "render", "symbol": "RENDER", "name": "Render", "source": "ai"},
    {"id": " Fetch.ai", "symbol": "FET", "name": "Fetch.ai", "source": "ai"},
    {"id": "ocean-protocol", "symbol": "OCEAN", "name": "Ocean Protocol", "source": "ai"},
]

def get_price(token_id):
    """Get price from CoinGecko"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": token_id, "vs_currencies": "usd", "include_24hr_change": "true", "include_market_cap": "true"}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        if token_id in data:
            return {
                "price": data[token_id].get("usd", 0),
                "change_24h": data[token_id].get("usd_24h_change", 0) or 0,
                "mcap": data[token_id].get("usd_market_cap", 0)
            }
    except:
        pass
    return None

def EMA(prices, period):
    if len(prices) < period:
        return sum(prices) / len(prices)
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * multiplier + ema * (1 - multiplier)
    return ema

def RSI(prices, period=14):
    if len(prices) < period + 1:
        return 50
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))

def analyze_token(token):
    """Full analysis on ANY token"""
    data = get_price(token["id"])
    if not data:
        return None
    
    # Simulate history for EMA/RSI (in production, use historical API)
    import random
    random.seed(hash(token["id"]))
    current = data["price"]
    prices = [current * (1 + random.uniform(-0.02, 0.02)) for _ in range(30)]
    prices.append(current)
    
    # Calculate indicators
    ema_9 = EMA(prices, 9)
    ema_21 = EMA(prices, 21)
    rsi = RSI(prices)
    vwap = sum(prices) / len(prices)
    
    # Score
    score = 0
    reasons = []
    
    if ema_9 > ema_21:
        score += 1
        reasons.append("EMA bullish")
    else:
        score -= 1
        reasons.append("EMA bearish")
    
    if rsi < 35:
        score += 2
        reasons.append("RSI oversold")
    elif rsi < 45:
        score += 1
        reasons.append("RSI near oversold")
    elif rsi > 65:
        score -= 2
        reasons.append("RSI overbought")
    elif rsi > 55:
        score -= 1
        reasons.append("RSI near overbought")
    
    if data["change_24h"] < -15:
        score += 3
        reasons.append("Deep dip")
    elif data["change_24h"] < -5:
        score += 1
        reasons.append("Down trend")
    elif data["change_24h"] > 15:
        score -= 1
        reasons.append("Hot rally")
    
    # Signal
    if score >= 3:
        signal = "STRONG_BUY"
    elif score >= 1:
        signal = "BUY"
    elif score <= -2:
        signal = "SELL"
    elif score <= -1:
        signal = "WATCH_SELL"
    else:
        signal = "NEUTRAL"
    
    return {
        "id": token["id"],
        "symbol": token["symbol"],
        "name": token["name"],
        "source": token["source"],
        "price": data["price"],
        "change_24h": data["change_24h"],
        "mcap": data["mcap"],
        "rsi": rsi,
        "ema_9": ema_9,
        "ema_21": ema_21,
        "score": score,
        "signal": signal,
        "reasons": reasons
    }

def scan_all():
    """Scan ALL tokens in watchlist"""
    print(f"\n{'='*70}")
    print(f"📊 MULTI-CHART ANALYZER - {datetime.now().strftime('%H:%M:%S')}")
    print("="*70)
    
    results = []
    buys = []
    sells = []
    
    for token in WATCHLIST:
        analysis = analyze_token(token)
        if analysis:
            results.append(analysis)
            
            if "BUY" in analysis["signal"]:
                buys.append(analysis)
            elif "SELL" in analysis["signal"]:
                sells.append(analysis)
    
    # Sort by score
    buys.sort(key=lambda x: x["score"], reverse=True)
    sells.sort(key=lambda x: x["score"])
    
    # Print BUYS
    if buys:
        print(f"\n🟢 BUY SIGNALS ({len(buys)}):")
        for b in buys[:8]:
            emoji = "🔥" if "STRONG" in b["signal"] else "🟢"
            mcap_str = f"${b['mcap']/1000000:.1f}M" if b['mcap'] > 1000000 else f"${b['mcap']/1000:.0f}K"
            print(f"  {emoji} {b['symbol']}: {b['signal']} (RSI:{b['rsi']:.0f}, 24h:{b['change_24h']:+.1f}%) | {mcap_str}")
    
    # Print SELLS
    if sells:
        print(f"\n🔴 SELL SIGNALS ({len(sells)}):")
        for s in sells[:5]:
            print(f"  🔴 {s['symbol']}: {s['signal']} (RSI:{s['rsi']:.0f}, 24h:{s['change_24h']:+.1f}%)")
    
    # Group by source
    print(f"\n📊 BY SOURCE:")
    sources = {}
    for r in results:
        src = r["source"]
        if src not in sources:
            sources[src] = []
        sources[src].append(r)
    
    for src, tokens in sources.items():
        print(f"  {src.upper()}: {', '.join([t['symbol'] for t in tokens[:5]])}")
    
    # Save
    with open("multi_chart_signals.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "buys": buys,
            "sells": sells,
            "all": results
        }, f, indent=2)
    
    print(f"\n💾 Saved to multi_chart_signals.json")
    
    return results

if __name__ == "__main__":
    print("📊 MULTI-CHART ANALYZER - Any Token, Any Time\n")
    scan_all()
