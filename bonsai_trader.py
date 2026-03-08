#!/usr/bin/env python3
"""
🌳 BONSAI TRADER
The Art of Pruning + Generative Growth
"""

import random
from datetime import datetime

class BonsaiPosition:
    """A branch (position) on our trading tree"""
    def __init__(self, token, entry_price, size):
        self.token = token
        self.entry_price = entry_price
        self.size = size
        self.current_price = entry_price
        self.pnl_percent = 0
        self.created_at = datetime.now()
    
    def update(self, price):
        self.current_price = price
        self.pnl_percent = ((price - self.entry_price) / self.entry_price) * 100

class BonsaiTrader:
    """
    Pruning-based trading system
    Like a bonsai tree:
    - Plant new branches (positions)
    - Prune losing branches (cut losses)
    - Harvest winners (take profits)
    - Let the tree grow
    """
    
    def __init__(self, config=None):
        # Configuration
        self.max_branches = config.get("max_positions", 10) if config else 10
        self.prune_threshold = config.get("prune_threshold", -5) if config else -5  # % loss to prune
        self.harvest_threshold = config.get("harvest_threshold", 30) if config else 30  # % gain to harvest
        self.trailing_stop = config.get("trailing_stop", 15) if config else 15  # % trailing stop
        
        # State
        self.positions = []  # Active branches
        self.pruned = []  # Cut branches
        self.harvested = []  # Taken profits
        self.pruned_count = 0
        self.harvested_count = 0
        self.total_pnl = 0
    
    def plant(self, token, entry_price, size):
        """Add a new branch (position)"""
        if len(self.positions) >= self.max_branches:
            return False, "Tree full - prune first"
        
        position = BonsaiPosition(token, entry_price, size)
        self.positions.append(position)
        return True, f"Planted {token} branch"
    
    def update_prices(self, prices):
        """Update all branch prices"""
        for pos in self.positions:
            if pos.token in prices:
                pos.update(prices[pos.token])
    
    def prune(self):
        """Cut branches that are losing too much"""
        pruned_tokens = []
        
        # Find branches to prune
        to_remove = []
        for i, pos in enumerate(self.positions):
            if pos.pnl_percent <= self.prune_threshold:
                to_remove.append(i)
                pruned_tokens.append(pos.token)
                self.pruned.append(pos)
                self.pruned_count += 1
                self.total_pnl += pos.pnl_percent
        
        # Remove from active
        for i in reversed(to_remove):
            self.positions.pop(i)
        
        return pruned_tokens
    
    def harvest(self):
        """Harvest branches that reached profit target"""
        harvested_tokens = []
        
        to_remove = []
        for i, pos in enumerate(self.positions):
            if pos.pnl_percent >= self.harvest_threshold:
                to_remove.append(i)
                harvested_tokens.append(pos.token)
                self.harvested.append(pos)
                self.harvested_count += 1
                self.total_pnl += pos.pnl_percent
        
        for i in reversed(to_remove):
            self.positions.pop(i)
        
        return harvested_tokens
    
    def check_trailing_stop(self):
        """Check trailing stop for all positions"""
        harvested = []
        for pos in self.positions:
            # Calculate current drawdown from peak
            if hasattr(pos, 'peak_pnl'):
                current_drawdown = pos.peak_pnl - pos.pnl_percent
                if current_drawdown >= self.trailing_stop:
                    harvested.append(pos.token)
                    self.harvested.append(pos)
                    self.harvested_count += 1
            else:
                pos.peak_pnl = pos.pnl_percent
        
        # Remove harvested
        self.positions = [p for p in self.positions if p.token not in harvested]
        
        return harvested
    
    def status(self):
        """Get tree status"""
        active_pnl = sum(p.pnl_percent for p in self.positions)
        
        return {
            "branches_growing": len(self.positions),
            "branches_pruned": self.pruned_count,
            "branches_harvested": self.harvested_count,
            "active_pnl": active_pnl,
            "total_pnl": self.total_pnl,
            "positions": [
                {
                    "token": p.token,
                    "pnl": f"{p.pnl_percent:.2f}%"
                }
                for p in self.positions
            ]
        }
    
    def grow(self):
        """Let the tree grow - returns positions to keep"""
        return self.positions

# Demo
def demo():
    """Demonstrate the Bonsai Trader"""
    print("="*60)
    print("🌳 BONSAI TRADER - Demo")
    print("="*60)
    
    # Create trader
    trader = BonsaiTrader({
        "max_positions": 5,
        "prune_threshold": -10,  # Prune at -10%
        "harvest_threshold": 30,  # Harvest at +30%
        "trailing_stop": 10  # Trail at 10%
    })
    
    # Simulate some trades
    print("\n🌱 Planting branches...")
    trader.plant("PENGU", 0.004, 1000)
    trader.plant("SKATE", 0.003, 2000)
    trader.plant("PEPE", 0.000001, 500000)
    
    # Simulate price movements
    print("\n📈 Growing...")
    prices = {
        "PENGU": 0.0044,  # +10%
        "SKATE": 0.0027,  # -10%
        "PEPE": 0.0000011  # +10%
    }
    trader.update_prices(prices)
    
    # Check status
    status = trader.status()
    print(f"\n🌳 Tree Status:")
    print(f"   Growing: {status['branches_growing']} branches")
    print(f"   Active P&L: {status['active_pnl']:.2f}%")
    
    for pos in status["positions"]:
        print(f"   - {pos['token']}: {pos['pnl']}")
    
    # Prune
    pruned = trader.prune()
    if pruned:
        print(f"\n✂️ Pruned: {pruned}")
    
    # Harvest
    harvested = trader.harvest()
    if harvested:
        print(f"\n🌾 Harvested: {harvested}")
    
    print(f"\n💰 Total P&L: {trader.total_pnl:.2f}%")
    
    return trader

if __name__ == "__main__":
    demo()
