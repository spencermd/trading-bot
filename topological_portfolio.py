#!/usr/bin/env python3
"""
🌐 TOPOLOGICAL PORTFOLIO OPTIMIZER
Algebraic Topology approach to portfolio construction
"""

import numpy as np
from itertools import combinations
import json
from datetime import datetime

class TopologicalPortfolio:
    """
    Build portfolio using algebraic topology:
    - Assets as 0-simplices (vertices)
    - Correlations as 1-simplices (edges)
    - Diversification = killing cycles (β₁ → 0)
    """
    
    def __init__(self, assets, returns, volatilities, correlations):
        """
        assets: list of asset names
        returns: list of expected returns
        volatilities: list of volatilities
        correlations: n×n correlation matrix
        """
        self.assets = assets
        self.n = len(assets)
        self.returns = np.array(returns)
        self.volatilities = np.array(volatilities)
        self.correlations = np.array(correlations)
    
    def build_vietoris_rips(self, threshold):
        """Build Vietoris-Rips complex at given threshold"""
        edges = []  # 1-simplices
        triangles = []  # 2-simplices
        
        # Edges: correlation above threshold
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.correlations[i,j] >= threshold:
                    edges.append((i,j))
        
        # Triangles: complete subgraph of 3
        for i, j, k in combinations(range(self.n), 3):
            if (i,j) in edges and (j,k) in edges and (i,k) in edges:
                triangles.append((i,j,k))
        
        return edges, triangles
    
    def compute_betti_numbers(self, threshold):
        """
        Compute Betti numbers:
        β₀ = number of connected components
        β₁ = number of independent cycles (undiversified risk)
        """
        edges, triangles = self.build_vietoris_rips(threshold)
        
        # Build adjacency for connected components
        adj = {i: set() for i in range(self.n)}
        for e in edges:
            adj[e[0]].add(e[1])
            adj[e[1]].add(e[0])
        
        # BFS for connected components (β₀)
        visited = set()
        components = 0
        for start in range(self.n):
            if start not in visited:
                components += 1
                stack = [start]
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        visited.add(node)
                        stack.extend(adj[node] - visited)
        
        # Euler characteristic: χ = V - E + F
        # For 2D: β₀ - β₁ = V - E + F
        V = self.n
        E = len(edges)
        F = len(triangles)
        
        # Simplified β₁ calculation
        beta_1 = max(0, E - V + 1 - components)  # Cycles
        
        return {
            "beta_0": components,  # Clusters
            "beta_1": beta_1,       # Risk cycles
            "vertices": V,
            "edges": E,
            "triangles": F
        }
    
    def compute_persistent_homology(self):
        """Find optimal threshold using persistent homology"""
        thresholds = np.arange(0.0, 1.01, 0.05)
        persistence = []
        
        for t in thresholds:
            betti = self.compute_betti_numbers(t)
            persistence.append({
                "threshold": t,
                "beta_0": betti["beta_0"],
                "beta_1": betti["beta_1"]
            })
        
        return persistence
    
    def find_optimal_threshold(self):
        """Find threshold where β₁ = 0 (fully diversified)"""
        persistence = self.compute_persistent_homology()
        
        # Find first threshold where beta_1 = 0
        for p in persistence:
            if p["beta_1"] == 0 and p["beta_0"] > 1:
                return p["threshold"]
        
        # Default to lowest beta_1
        best = min(persistence, key=lambda x: x["beta_1"])
        return best["threshold"]
    
    def optimize(self):
        """
        Find topologically optimal portfolio
        Goal: Minimize β₁ (risk cycles) while maintaining β₀ > 1 (diversity)
        """
        t = self.find_optimal_threshold()
        
        # Get edges at optimal threshold
        edges, _ = self.build_vietoris_rips(t)
        
        # Find minimum spanning tree edges (diversification backbone)
        connected = set()
        mst_edges = []
        
        for e in sorted(edges, key=lambda x: self.correlations[x[0], x[1]]):
            # Add edge if it connects new components
            c0, c1 = e[0] in connected, e[1] in connected
            if not (c0 and c1):  # At least one is new
                mst_edges.append(e)
                connected.add(e[0])
                connected.add(e[1])
        
        # Equal weight to all connected assets
        weights = np.zeros(self.n)
        if connected:
            for i in connected:
                weights[i] = 1.0 / len(connected)
        
        # Add small weight to disconnected for exploration
        if len(connected) < self.n:
            for i in range(self.n):
                if weights[i] == 0:
                    weights[i] = 0.01
        
        # Normalize
        weights = weights / weights.sum()
        
        return {
            "weights": dict(zip(self.assets, weights)),
            "threshold": t,
            "betti": self.compute_betti_numbers(t)
        }
    
    def analyze(self):
        """Full topological analysis"""
        persistence = self.compute_persistent_homology()
        optimal_t = self.find_optimal_threshold()
        
        return {
            "assets": self.assets,
            "persistence": persistence,
            "optimal_threshold": optimal_t,
            "optimal_allocation": self.optimize()
        }

# Demo
def demo():
    """Demonstrate with example assets"""
    
    # Example: 6 assets with different correlations
    assets = ["BTC", "ETH", "SOL", "SPY", "GLD", "TLT"]
    
    # Expected returns
    returns = [0.15, 0.08, 0.25, 0.07, 0.03, 0.02]
    
    # Volatilities
    volatilities = [0.70, 0.55, 0.90, 0.15, 0.12, 0.08]
    
    # Correlation matrix
    correlations = np.array([
        [1.00, 0.75, 0.65, 0.15, 0.05, -0.10],  # BTC
        [0.75, 1.00, 0.70, 0.20, 0.08, -0.05],  # ETH
        [0.65, 0.70, 1.00, 0.18, 0.05, -0.08],  # SOL
        [0.15, 0.20, 0.18, 1.00, 0.30,  0.40],  # SPY
        [0.05, 0.08, 0.05, 0.30, 1.00,  0.50],  # GLD
        [-0.10,-0.05,-0.08, 0.40, 0.50,  1.00],  # TLT
    ])
    
    # Build portfolio
    portfolio = TopologicalPortfolio(assets, returns, volatilities, correlations)
    
    # Analyze
    results = portfolio.analyze()
    
    print("="*60)
    print("🌐 TOPOLOGICAL PORTFOLIO OPTIMIZER")
    print("="*60)
    
    print(f"\n📊 PERSISTENT HOMOLOGY:")
    for p in results["persistence"]:
        if p["threshold"] in [0.0, 0.3, 0.5, 0.7, 1.0]:
            print(f"   t={p['threshold']:.1f}: β₀={p['beta_0']}, β₁={p['beta_1']}")
    
    opt = results["optimal_allocation"]
    print(f"\n🎯 OPTIMAL THRESHOLD: {opt['threshold']:.2f}")
    print(f"\n💰 OPTIMAL ALLOCATION:")
    for asset, weight in sorted(opt["weights"].items(), key=lambda x: -x[1]):
        if weight > 0.01:
            print(f"   {asset}: {weight*100:.1f}%")
    
    b = opt["betti"]
    print(f"\n🧮 BETTI NUMBERS (at optimal):")
    print(f"   β₀ = {b['beta_0']} (asset clusters)")
    print(f"   β₁ = {b['beta_1']} (risk cycles)")
    
    # Interpretation
    print(f"\n💡 INTERPRETATION:")
    if b["beta_1"] == 0:
        print("   ✓ Portfolio is fully diversified!")
        print("   ✓ No undiversifiable risk cycles remain")
    else:
        print(f"   ⚠ {b['beta_1']} risk cycle(s) remain")
    
    return results

if __name__ == "__main__":
    demo()
