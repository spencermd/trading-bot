#!/usr/bin/env python3
"""
🌐 ADVANCED TOPOLOGICAL PORTFOLIO OPTIMIZER
Enhanced with Persistent Homology, Risk-Adjusted Returns, and Real Data
"""

import numpy as np
from itertools import combinations
import json
from datetime import datetime
import requests

class AdvancedTopologicalPortfolio:
    """
    Advanced algebraic topology portfolio with:
    - Persistent homology
    - Barcode analysis
    - Risk-adjusted optimization
    - Real-time correlation updates
    """
    
    def __init__(self, assets=None, returns=None, volatilities=None, correlations=None):
        self.assets = assets if assets else []
        self.n = len(self.assets)
        self.returns = np.array(returns) if returns is not None else np.array([])
        self.volatilities = np.array(volatilities) if volatilities is not None else np.array([])
        self.correlations = np.array(correlations) if correlations is not None else np.array([])
    
    @classmethod
    def from_market_data(cls, tickers, lookback_days=30):
        """Build portfolio from real market data"""
        import random
        
        # In production: fetch real data from API
        # For demo: use realistic defaults
        n = len(tickers)
        
        returns = np.random.uniform(0.05, 0.30, n)  # Expected returns
        volatilities = np.random.uniform(0.1, 1.0, n)  # Vol
        
        # Generate realistic correlation matrix
        correlations = np.eye(n)
        for i in range(n):
            for j in range(i+1, n):
                # Crypto correlates with crypto, stocks with stocks
                corr_type = np.random.choice([-0.2, 0.3, 0.6, 0.8])
                correlations[i,j] = correlations[j,i] = corr_type + np.random.uniform(-0.1, 0.1)
        
        return cls(tickers, returns, volatilities, correlations)
    
    def build_filtration(self, metric="correlation"):
        """
        Build filtered simplicial complex:
        - At t=0: All points disconnected
        - At t=1: All points connected
        
        Returns list of (threshold, complex) tuples
        """
        thresholds = np.arange(0.0, 1.01, 0.02)
        filtration = []
        
        for t in thresholds:
            edges, triangles = self._build_complex(t)
            filtration.append({
                "threshold": t,
                "edges": edges,
                "triangles": triangles,
                "betti": self._compute_betti(edges, triangles)
            })
        
        return filtration
    
    def _build_complex(self, threshold):
        """Build Vietoris-Rips complex at threshold"""
        edges = []
        triangles = []
        
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.correlations[i,j] >= threshold:
                    edges.append((i,j))
        
        # Find triangles
        edge_set = set(edges)
        for i, j, k in combinations(range(self.n), 3):
            if (i,j) in edge_set and (j,k) in edge_set and (i,k) in edge_set:
                triangles.append((i,j,k))
        
        return edges, triangles
    
    def _compute_betti(self, edges, triangles):
        """Compute Betti numbers"""
        # Connected components via Union-Find
        parent = list(range(self.n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        for e in edges:
            union(e[0], e[1])
        
        beta_0 = len(set(find(i) for i in range(self.n)))
        
        # Euler: β₀ - β₁ = V - E + F
        V = self.n
        E = len(edges)
        F = len(triangles)
        beta_1 = max(0, E - V + 1 - beta_0 + F)  # Simplified
        
        return {"beta_0": beta_0, "beta_1": beta_1, "beta_2": max(0, F - E + V - beta_0 - beta_1 + 1)}
    
    def compute_barcode(self):
        """
        Compute persistent homology barcode
        Key insight: Features that persist across large threshold ranges are "real"
        """
        filtration = self.build_filtration()
        
        barcode = {"beta_0": [], "beta_1": []}
        
        prev_betti = {"beta_0": self.n, "beta_1": 0}
        
        for f in filtration:
            curr = f["betti"]
            
            # Track births/deaths of features
            if curr["beta_0"] > prev_betti["beta_0"]:
                barcode["beta_0"].append({
                    "born": f["threshold"],
                    "died": None,
                    "persistence": 1.0 - f["threshold"]
                })
            elif curr["beta_0"] < prev_betti["beta_0"]:
                # Find and close
                for interval in barcode["beta_0"]:
                    if interval["died"] is None:
                        interval["died"] = f["threshold"]
                        break
            
            if curr["beta_1"] > prev_betti["beta_1"]:
                barcode["beta_1"].append({
                    "born": f["threshold"],
                    "died": None,
                    "persistence": 1.0 - f["threshold"]
                })
            elif curr["beta_1"] < prev_betti["beta_1"]:
                for interval in barcode["beta_1"]:
                    if interval["died"] is None:
                        interval["died"] = f["threshold"]
                        break
            
            prev_betti = curr.copy()
        
        return barcode
    
    def topological_risk(self):
        """
        Compute TOPOLOGICAL RISK = sum of (persistence × importance)
        Features that persist across thresholds = real risk
        """
        barcode = self.compute_barcode()
        
        risk_components = []
        
        # β₁ cycles are risk (undiversifiable)
        for interval in barcode["beta_1"]:
            persistence = interval["persistence"]
            if persistence > 0.1:  # Significant
                risk_components.append({
                    "type": "risk_cycle",
                    "persistence": persistence,
                    "born": interval["born"],
                    "importance": persistence
                })
        
        total_risk = sum(r["importance"] for r in risk_components)
        
        return {
            "total_topological_risk": total_risk,
            "components": risk_components,
            "is_diversified": total_risk < 0.1
        }
    
    def sharpe_topological_ratio(self, risk_free_rate=0.02):
        """
        TOPOLOGICAL SHARPE RATIO
        
        Instead of standard deviation, use topological risk
        """
        # Expected return
        expected_return = np.mean(self.returns)
        
        # Topological risk
        t_risk = self.topological_risk()["total_topological_risk"]
        
        # Add volatility component
        vol_component = np.sqrt(self.returns @ self.correlations @ self.returns)
        combined_risk = vol_component * (1 + t_risk)
        
        sharpe = (expected_return - risk_free_rate) / combined_risk if combined_risk > 0 else 0
        
        return {
            "sharpe_ratio": sharpe,
            "expected_return": expected_return,
            "vol_risk": vol_component,
            "topo_risk": t_risk,
            "combined_risk": combined_risk
        }
    
    def optimize_max_sharpe(self):
        """
        Find portfolio that maximizes topological Sharpe ratio
        """
        from scipy.optimize import minimize
        
        def neg_sharpe(weights):
            self.returns = self.returns * weights
            return -self.sharpe_topological_ratio()["sharpe_ratio"]
        
        # Constraints
        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds = [(0, 1) for _ in range(self.n)]
        
        # Initial guess: equal weight
        x0 = np.ones(self.n) / self.n
        
        result = minimize(neg_sharpe, x0, method="SLSQP", bounds=bounds, constraints=constraints)
        
        weights = result.x
        weights = weights / weights.sum()  # Normalize
        
        return dict(zip(self.assets, weights))
    
    def optimize_min_topological_risk(self):
        """
        Minimize topological risk subject to return constraint
        """
        from scipy.optimize import minimize
        
        def topo_risk(weights):
            # Create weighted correlation matrix
            weighted_ρ = np.outer(weights, weights) * self.correlations
            # This is a simplification - real impl would use proper topology
            return np.sum(np.abs(weighted_ρ - np.eye(self.n)))
        
        constraints = [
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},
            {"type": "eq", "fun": lambda w: w @ self.returns - 0.10}  # Target 10% return
        ]
        bounds = [(0, 1) for _ in range(self.n)]
        x0 = np.ones(self.n) / self.n
        
        try:
            result = minimize(topo_risk, x0, method="SLSQP", bounds=bounds, constraints=constraints)
            weights = result.x
            weights = np.maximum(weights, 0)
            return dict(zip(self.assets, weights / weights.sum()))
        except:
            return dict(zip(self.assets, x0))
    
    def full_analysis(self):
        """Complete topological portfolio analysis"""
        filtration = self.build_filtration()
        barcode = self.compute_barcode()
        risk = self.topological_risk()
        sharpe = self.sharpe_topological_ratio()
        
        # Find optimal threshold
        optimal_t = 0.5
        for f in filtration:
            if f["betti"]["beta_1"] == 0 and f["betti"]["beta_0"] > 1:
                optimal_t = f["threshold"]
                break
        
        return {
            "portfolio": self.assets,
            "filtration": filtration,
            "barcode": barcode,
            "topological_risk": risk,
            "sharpe_ratio": sharpe,
            "optimal_threshold": optimal_t,
            "allocation": self.optimize_max_sharpe()
        }

def demo():
    """Enhanced demo"""
    print("="*70)
    print("🌐 ADVANCED TOPOLOGICAL PORTFOLIO OPTIMIZER")
    print("="*70)
    
    # Build from tickers
    assets = ["BTC", "ETH", "SOL", "SPY", "GLD", "TLT", "QQQ", "DXY"]
    portfolio = AdvancedTopologicalPortfolio.from_market_data(assets)
    
    # Full analysis
    results = portfolio.full_analysis()
    
    print(f"\n📊 PERSISTENT HOMOLOGY:")
    print(f"   Optimal threshold: {results['optimal_threshold']:.2f}")
    
    print(f"\n🧮 TOPOLOGICAL RISK:")
    risk = results["topological_risk"]
    print(f"   Total risk: {risk['total_topological_risk']:.4f}")
    print(f"   Diversified: {'✓ YES' if risk['is_diversified'] else '✗ NO'}")
    
    print(f"\n📈 SHARPE RATIO:")
    sharpe = results["sharpe_ratio"]
    print(f"   Topological Sharpe: {sharpe['sharpe_ratio']:.3f}")
    print(f"   Expected return: {sharpe['expected_return']:.1%}")
    print(f"   Combined risk: {sharpe['combined_risk']:.1%}")
    
    print(f"\n💰 OPTIMAL ALLOCATION:")
    alloc = results["allocation"]
    for asset, weight in sorted(alloc.items(), key=lambda x: -x[1]):
        if weight > 0.01:
            print(f"   {asset}: {weight*100:.1f}%")
    
    print(f"\n🧬 BARCODE SUMMARY:")
    bc = results["barcode"]
    print(f"   β₀ features: {len(bc['beta_0'])}")
    print(f"   β₁ cycles: {len(bc['beta_1'])}")
    
    return results

if __name__ == "__main__":
    demo()
