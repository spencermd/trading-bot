#!/usr/bin/env python3
"""
Gem Finder - Scan for low-cap tokens that are down significantly
Focus on Solana ecosystem
Run every 15 minutes for 45 minutes (3 scans)
"""

import yfinance as yf
import json
import os
from datetime import datetime
import time

OUTPUT_FILE = "/home/eldes/polymarket_panic_bot/new_gems.json"

# Extended list of tokens to scan - focused on Solana ecosystem + other low cap
SOLANA_TOKENS = [
    # Solana main
    'BONK-USD', 'WIF-USD', 'POPCAT-USD', 'MEW-USD', 'BOOK-USD', 
    'GRASS-USD', 'ZEREBRO-USD', 'MOODENG-USD', 'FWOG-USD', 'MOG-USD',
    'CHILLGUY-USD', 'BOME-USD', 'SLERF-USD', 'WEN-USD', 'SILLY-USD',
    'SC-USD', 'AUC-USD', 'ALEPH-USD', 'Canto-USD', 'GMT-USD',
    'GALA-USD', 'RNDR-USD', 'BLZ-USD', 'HNT-USD', 'MINA-USD', 
    'AUDIO-USD', 'STEP-USD', 'SAMO-USD', 'RAY-USD', 'COPE-USD', 
    'SNY-USD', 'MAPS-USD', 'PORTAL-USD', 'CAT-USD',
    
    # Other chains
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'AVAX-USD', 'MATIC-USD',
    'DOT-USD', 'LINK-USD', 'UNI-USD', 'ATOM-USD', 'LTC-USD',
    'ALGO-USD', 'VET-USD', 'FIL-USD', 'XLM-USD', 'ETC-USD',
    'AAVE-USD', 'EOS-USD', 'XMR-USD', 'CAKE-USD', 'GRT-USD',
    'NEO-USD', 'EGLD-USD', 'MKR-USD', 'SNX-USD', 'CRV-USD',
    'RUNE-USD', 'ZEC-USD', 'DASH-USD', 'MANA-USD', 'SAND-USD',
    'AXS-USD', 'FTM-USD', 'ZIL-USD', 'SUSHI-USD', 'YFI-USD',
    'BAL-USD', '1INCH-USD', 'CHZ-USD', 'REN-USD', 'SKL-USD',
    'ANKR-USD', 'ICX-USD', 'STORJ-USD', 'KAVA-USD', 'SXP-USD',
    'CEL-USD', 'QTUM-USD', 'ONT-USD', 'HOOK-USD', 'MAGIC-USD',
    'GMX-USD', 'LQTY-USD', 'RDNT-USD', 'VELO-USD', 'GMEE-USD',
    'DODO-USD', 'ALICE-USD', 'BETA-USD', 'KDA-USD', 'NEXO-USD',
    'STMX-USD', 'KEY-USD', 'NKN-USD', 'WAVES-USD', 'ZRX-USD',
    'CELO-USD', 'C98-USD', 'COTI-USD', 'FLUX-USD', 'REQ-USD',
    'RARE-USD', 'BAND-USD', 'ENJ-USD', 'GFT-USD', 'STPT-USD', 
    'LSK-USD', 'STEEM-USD', 'DEP-USD', 'HBAR-USD', 'SYS-USD', 
    'SUN-USD', 'OGN-USD', 'MBL-USD', 'WAN-USD', 'CTSI-USD'
]

def scan_for_gems():
    """Scan for gem tokens matching criteria"""
    gems = []
    scanned = 0
    
    for t in SOLANA_TOKENS:
        try:
            ticker = yf.Ticker(t)
            info = ticker.info
            mcap = info.get('marketCap')
            change = info.get('regularMarketChangePercent')
            
            scanned += 1
            
            if mcap and mcap > 0 and change is not None:
                mcap = float(mcap)
                change = float(change)
                price = info.get('currentPrice', 0)
                
                # Filter: market cap $100K - $10M AND down 15%+ in 24h (strict)
                # Also capture slightly relaxed for display
                if 100000 <= mcap <= 10000000 and change <= -15:
                    gem = {
                        'name': t.replace('-USD', ''),
                        'symbol': t.replace('-USD', ''),
                        'mcap': mcap,
                        'change24h': round(change, 2),
                        'price': price,
                        'timestamp': datetime.now().isoformat()
                    }
                    gems.append(gem)
                    print(f"💎 GEM: {gem['name']} ${gem['mcap']:,.0f} ({gem['change24h']}% down) - BUY?")
                    
        except Exception as e:
            pass
    
    return gems, scanned

def run_scans(num_scans=3, interval_minutes=15):
    """Run multiple scans with interval"""
    all_gems = []
    
    for i in range(num_scans):
        print(f"\n{'='*50}")
        print(f"SCAN {i+1}/{num_scans} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*50}")
        
        gems, scanned = scan_for_gems()
        
        for g in gems:
            # Avoid duplicates
            if not any(existing['name'] == g['name'] for existing in all_gems):
                all_gems.append(g)
        
        print(f"\n📊 Scan {i+1} complete: {len(gems)} gems found (total unique: {len(all_gems)})")
        
        if i < num_scans - 1:
            print(f"⏳ Waiting {interval_minutes} minutes for next scan...")
            time.sleep(interval_minutes * 60)
    
    return all_gems

def main():
    print("🔍 GEM FINDER - Scanning for low-cap tokens")
    print(f"Criteria: Market cap $100K - $10M AND down 15%+ in 24h")
    print(f"Starting at {datetime.now().strftime('%H:%M:%S')}")
    
    all_gems = run_scans(num_scans=3, interval_minutes=15)
    
    # Save to JSON
    result = {
        'scan_time': datetime.now().isoformat(),
        'gems_found': len(all_gems),
        'scans': 3,
        'gems': all_gems
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"FINAL RESULTS")
    print(f"{'='*50}")
    print(f"Total gems found: {len(all_gems)}")
    print(f"Results saved to: {OUTPUT_FILE}")
    
    for g in all_gems:
        print(f"💎 GEM: {g['name']} ${g['mcap']:,.0f} ({g['change24h']}% down) - BUY?")
    
    return result

if __name__ == "__main__":
    main()
