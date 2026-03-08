#!/usr/bin/env python3
"""
Gem Finder - Scan for low-cap tokens that are down significantly
Focus on Solana ecosystem
"""

import yfinance as yf
import json
import os
from datetime import datetime

OUTPUT_FILE = "/home/eldes/polymarket_panic_bot/new_gems.json"

# Extended list of tokens to scan - focused on Solana ecosystem + other low cap
SOLANA_TOKENS = [
    # Solana main
    'BONK-USD', 'WIF-USD', 'POPCAT-USD', 'MEW-USD', 'BOOK-USD', 
    'GRASS-USD', 'ZEREBRO-USD', 'MOODENG-USD', 'FWOG-USD', 'MOG-USD',
    'CHILLGUY-USD', 'BOME-USD', 'SLERF-USD', 'WEN-USD', 'SILLY-USD',
    'SC-USD', 'AUC-USD', 'ALEPH-USD', 'Canto-USD', 'GMT-USD',
    'GALA-USD', 'RNDR-USD', 'IMGM-USD', 'BLZ-USD', 'HNT-USD',
    'MINA-USD', 'AUDIO-USD', 'STEP-USD', 'SAMO-USD', 'RAY-USD',
    'COPE-USD', 'SNY-USD', 'MAPS-USD', 'PORTAL-USD', 'CAT-USD',
    
    # Other chains (for variety)
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
    'RARE-USD', 'BAND-USD', 'ENJ-USD', 'GFT-USD', 'BURGER-USD',
    'STPT-USD', 'LSK-USD', 'STEEM-USD', 'DEP-USD', 'RENBTC-USD',
    'WBTC-USD', 'HBAR-USD', 'SYS-USD', 'SUN-USD'
]

def scan_for_gems():
    """Scan for gem tokens matching criteria"""
    gems = []
    scanned = 0
    errors = 0
    
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
                
                # Filter: market cap $100K - $10M AND down 10%+ in 24h (relaxed for more results)
                if 100000 <= mcap <= 10000000 and change <= -10:
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
            errors += 1
            pass
    
    return gems, scanned, errors

def main():
    print(f"🔍 Scanning for gems... ({datetime.now().strftime('%H:%M:%S')})")
    
    gems, scanned, errors = scan_for_gems()
    
    # Save to JSON
    result = {
        'scan_time': datetime.now().isoformat(),
        'gems_found': len(gems),
        'scanned': scanned,
        'errors': errors,
        'gems': gems
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📊 Scan complete: {len(gems)} gems found out of {scanned} tokens scanned")
    print(f"📁 Results saved to: {OUTPUT_FILE}")
    
    return result

if __name__ == "__main__":
    main()
