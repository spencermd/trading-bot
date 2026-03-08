#!/usr/bin/env python3
"""Comprehensive signal aggregator for gem scanner"""
import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/eldes/polymarket_panic_bot")

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return None

def aggregate_signals():
    """Aggregate all signal sources into unified alerts"""
    alerts = []
    
    # 1. Check algo_signals.json for BUY signals
    algo = load_json(BASE_DIR / "algo_signals.json")
    if algo and "signals" in algo:
        for sig in algo["signals"]:
            if sig.get("action") == "BUY":
                alerts.append({
                    "type": "ALGO_BUY",
                    "symbol": sig.get("symbol"),
                    "price": sig.get("price"),
                    "rsi": sig.get("rsi"),
                    "action": "BUY",
                    "timestamp": datetime.now().isoformat()
                })
    
    # 2. Check elite.json for opportunities
    elite = load_json(BASE_DIR / "elite.json")
    if elite and "top_opportunities" in elite:
        for opp in elite["top_opportunities"][:10]:
            if opp.get("action") in ["VOLUME_ALERT", "HOT_GAINER"]:
                alerts.append({
                    "type": "ELITE_SIGNAL",
                    "symbol": opp.get("symbol"),
                    "price": opp.get("price"),
                    "action": opp.get("action"),
                    "score": opp.get("score"),
                    "timestamp": datetime.now().isoformat()
                })
    
    # 3. Check ultra.json
    ultra = load_json(BASE_DIR / "ultra.json")
    if ultra and "signals" in ultra:
        for sig in ultra["signals"]:
            if sig.get("action") in ["BUY", "HOT_GAINER"]:
                alerts.append({
                    "type": "ULTRA_SIGNAL",
                    "symbol": sig.get("symbol"),
                    "price": sig.get("price"),
                    "action": sig.get("action"),
                    "timestamp": datetime.now().isoformat()
                })
    
    # 4. Check momentum.json
    momentum = load_json(BASE_DIR / "momentum.json")
    if momentum and "signals" in momentum:
        for sig in momentum["signals"]:
            if sig.get("action") == "BUY":
                alerts.append({
                    "type": "MOMENTUM_BUY",
                    "symbol": sig.get("symbol"),
                    "price": sig.get("price"),
                    "action": "BUY",
                    "timestamp": datetime.now().isoformat()
                })
    
    # 5. Check x.json (social signals)
    x_signals = load_json(BASE_DIR / "x.json")
    if x_signals and "signals" in x_signals:
        for sig in x_signals["signals"][:5]:
            alerts.append({
                "type": "SOCIAL_BUZZ",
                "symbol": sig.get("symbol"),
                "mentions": sig.get("mentions"),
                "sentiment": sig.get("sentiment"),
                "timestamp": datetime.now().isoformat()
            })
    
    return alerts

def run_scan():
    """Run full gem scan and aggregate signals"""
    print(f"\n{'='*60}")
    print(f"🔍 GEM SCAN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Aggregate all signals
    alerts = aggregate_signals()
    
    # Save to alerts.json
    with open(BASE_DIR / "alerts.json", 'w') as f:
        json.dump(alerts, f, indent=2)
    
    # Print signals
    print(f"\n📊 SIGNALS FOUND: {len(alerts)}")
    print("-" * 40)
    
    if alerts:
        for a in alerts:
            symbol = a.get("symbol", "?")
            atype = a.get("type", "SIGNAL")
            action = a.get("action", "")
            price = a.get("price", 0)
            
            if action:
                print(f"  ✅ {atype}: {symbol} @ ${price:.4f} ({action})")
            else:
                print(f"  📌 {atype}: {symbol}")
    else:
        print("  (No buy signals detected)")
    
    print(f"\n💾 Saved to: {BASE_DIR / 'alerts.json'}")
    
    return alerts

if __name__ == "__main__":
    run_scan()
