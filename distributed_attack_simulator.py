"""
Bitcoin ECDLP - Distributed Attack Simulator
Simulate coordinated attacks across multiple GPU clusters
"""

import time
import random
import threading
from datetime import datetime, timedelta
import math

print("="*80)
print("🖥️  BITCOIN ECDLP - DISTRIBUTED ATTACK SIMULATOR")
print("="*80)
print()

# ========================
# CURVE SETUP
# ========================

P = 17
a = 0
b = 7

def mod_inverse(a, m):
    if a < 0:
        a = (a % m + m) % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def point_add(p1, p2, p_mod, a_coeff):
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        if (y1 + y2) % p_mod == 0:
            return (0, 0)
    
    if x1 == x2 and y1 == y2:
        numerator = (3 * x1**2 + a_coeff) % p_mod
        denominator = (2 * y1) % p_mod
    else:
        numerator = (y2 - y1) % p_mod
        denominator = (x2 - x1) % p_mod
    
    lambda_val = (numerator * mod_inverse(denominator, p_mod)) % p_mod
    x3 = (lambda_val**2 - x1 - x2) % p_mod
    y3 = (lambda_val * (x1 - x3) - y1) % p_mod
    
    return (x3, y3)

def point_multiply(k, base_point, p_mod, a_coeff):
    if k == 0:
        return (0, 0)
    result = (0, 0)
    addend = base_point
    
    while k:
        if k & 1:
            result = point_add(result, addend, p_mod, a_coeff)
        addend = point_add(addend, addend, p_mod, a_coeff)
        k >>= 1
    
    return result

def find_curve_points(p, a, b):
    points = [(0, 0)]
    for x in range(p):
        y_squared = (x**3 + a*x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))
    return sorted(set(points))

points = find_curve_points(P, a, b)
G = (2, 5)
N = len(points)

# ========================
# DISTRIBUTED NODE
# ========================

class GPUNode:
    """Simulates a single GPU computing node"""
    
    def __init__(self, node_id, ops_per_sec=1e6, location="Unknown"):
        self.node_id = node_id
        self.ops_per_sec = ops_per_sec  # Operations per second
        self.location = location
        self.is_active = True
        self.keys_tested = 0
        self.start_key = 0
        self.end_key = 0
        self.found_key = None
        self.found = False
        self.processing_time = 0
        self.latency = random.uniform(0.01, 0.1)  # 10-100ms network latency
        self.uptime = random.uniform(0.95, 0.99)  # 95-99% uptime
    
    def assign_range(self, start_key, end_key):
        """Assign a range of keys to search"""
        self.start_key = start_key
        self.end_key = end_key
    
    def search_range(self, target_public, verbose=False):
        """Search assigned range for private key"""
        if not self.is_active:
            return None
        
        start_time = time.time()
        
        for test_key in range(self.start_key, self.end_key + 1):
            # Simulate random downtime
            if random.random() > self.uptime:
                if verbose:
                    print(f"  Node {self.node_id}: Network hiccup!")
                time.sleep(random.uniform(0.1, 0.5))
            
            test_public = point_multiply(test_key, G, P, a)
            self.keys_tested += 1
            
            if test_public == target_public:
                self.found = True
                self.found_key = test_key
                self.processing_time = time.time() - start_time
                return test_key
        
        self.processing_time = time.time() - start_time
        return None
    
    def get_status(self):
        """Return node status"""
        return {
            'node_id': self.node_id,
            'location': self.location,
            'keys_tested': self.keys_tested,
            'found': self.found,
            'processing_time': self.processing_time,
            'latency_ms': self.latency * 1000,
            'uptime_percent': self.uptime * 100
        }

# ========================
# DISTRIBUTED CLUSTER
# ========================

class GPUCluster:
    """Manages multiple GPU nodes"""
    
    def __init__(self, cluster_name, num_nodes, ops_per_sec_per_node):
        self.cluster_name = cluster_name
        self.num_nodes = num_nodes
        self.nodes = []
        self.total_keys_tested = 0
        self.found_key = None
        self.start_time = None
        self.end_time = None
        self.synchronization_time = 0
        
        # Create nodes with realistic locations
        locations = [
            "Virginia, USA", "Oregon, USA", "Frankfurt, Germany",
            "Tokyo, Japan", "Sydney, Australia", "London, UK",
            "Toronto, Canada", "São Paulo, Brazil"
        ]
        
        for i in range(num_nodes):
            location = locations[i % len(locations)]
            node = GPUNode(i, ops_per_sec=ops_per_sec_per_node, location=location)
            self.nodes.append(node)
    
    def distribute_workload(self, search_space, verbose=False):
        """Distribute search space among nodes"""
        keys_per_node = search_space // self.num_nodes
        remainder = search_space % self.num_nodes
        
        if verbose:
            print(f"\n📊 WORKLOAD DISTRIBUTION")
            print("-" * 80)
            print(f"Total search space: {search_space}")
            print(f"Number of nodes: {self.num_nodes}")
            print(f"Keys per node: {keys_per_node}")
            print(f"Remainder: {remainder}")
            print()
        
        for i, node in enumerate(self.nodes):
            start = 1 + i * keys_per_node
            end = start + keys_per_node - 1
            
            # Add remainder to last node
            if i == self.num_nodes - 1:
                end += remainder
            
            node.assign_range(start, end)
            
            if verbose:
                print(f"  Node {node.node_id:2d} ({node.location:20s}): {start:6d} - {end:6d}")
    
    def coordinate_search(self, target_public, verbose=True):
        """Coordinate search across all nodes"""
        if verbose:
            print()
            print("🚀 STARTING DISTRIBUTED SEARCH")
            print("="*80)
            print()
        
        self.start_time = time.time()
        
        # Simulate parallel search
        threads = []
        results = {}
        
        for node in self.nodes:
            def search_worker(n):
                result = n.search_range(target_public, verbose)
                if result:
                    results[n.node_id] = result
            
            thread = threading.Thread(target=search_worker, args=(node,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        self.end_time = time.time()
        
        # Calculate synchronization overhead
        max_time = max(node.processing_time for node in self.nodes)
        self.synchronization_time = max_time + sum(node.latency for node in self.nodes)
        
        # Collect results
        for node in self.nodes:
            self.total_keys_tested += node.keys_tested
            if node.found:
                self.found_key = node.found_key
        
        if verbose:
            self.print_results()
        
        return self.found_key
    
    def print_results(self):
        """Print search results"""
        total_time = self.end_time - self.start_time
        
        print("✅ SEARCH COMPLETED")
        print("="*80)
        print()
        
        print(f"Cluster: {self.cluster_name}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Total keys tested: {self.total_keys_tested:,}")
        print()
        
        if self.found_key:
            print(f"🎉 FOUND! Private key: {self.found_key}")
        else:
            print("❌ Not found in assigned range")
        
        print()
        print("📊 NODE STATISTICS")
        print("-"*80)
        print(f"{'Node':<6} {'Location':<20} {'Keys':<10} {'Time':<10} {'Latency':<10} {'Status':<10}")
        print("-"*80)
        
        for node in self.nodes:
            status = "✅ FOUND" if node.found else "OK"
            print(f"{node.node_id:<6} {node.location:<20} {node.keys_tested:<10} "
                  f"{node.processing_time:<10.3f}s {node.latency*1000:<10.1f}ms {status:<10}")
        
        print()
    
    def get_cluster_stats(self):
        """Get cluster statistics"""
        total_time = self.end_time - self.start_time if self.end_time else 0
        efficiency = (self.num_nodes * max(n.processing_time for n in self.nodes) / total_time 
                     if total_time > 0 else 0)
        
        return {
            'cluster_name': self.cluster_name,
            'num_nodes': self.num_nodes,
            'total_time': total_time,
            'total_keys': self.total_keys_tested,
            'keys_per_second': self.total_keys_tested / total_time if total_time > 0 else 0,
            'efficiency': efficiency * 100,
            'found_key': self.found_key
        }

# ========================
# SCENARIOS
# ========================

def scenario_small_cluster():
    """Scenario 1: Small cluster (10 nodes)"""
    print()
    print("="*80)
    print("SCENARIO 1: Small Cluster (10 GPUs)")
    print("="*80)
    
    cluster = GPUCluster("Small Cluster", num_nodes=10, ops_per_sec_per_node=1e6)
    
    # Setup puzzle
    secret_key = random.randint(1, N-1)
    target_public = point_multiply(secret_key, G, P, a)
    
    print(f"Secret key (hidden): {secret_key}")
    print(f"Target public key: {target_public}")
    
    # Distribute and search
    cluster.distribute_workload(N, verbose=True)
    cluster.coordinate_search(target_public, verbose=True)
    
    return cluster.get_cluster_stats()

def scenario_medium_cluster():
    """Scenario 2: Medium cluster (100 nodes)"""
    print()
    print("="*80)
    print("SCENARIO 2: Medium Cluster (100 GPUs)")
    print("="*80)
    
    cluster = GPUCluster("Medium Cluster", num_nodes=100, ops_per_sec_per_node=1e6)
    
    # Setup puzzle
    secret_key = random.randint(1, N-1)
    target_public = point_multiply(secret_key, G, P, a)
    
    print(f"Secret key (hidden): {secret_key}")
    print(f"Target public key: {target_public}")
    
    # Distribute and search
    cluster.distribute_workload(N, verbose=False)
    print("\n📊 WORKLOAD DISTRIBUTION (condensed)")
    print(f"Total search space: {N}")
    print(f"Number of nodes: 100")
    print(f"Keys per node: {N//100}")
    
    cluster.coordinate_search(target_public, verbose=True)
    
    return cluster.get_cluster_stats()

def scenario_mega_cluster():
    """Scenario 3: Mega cluster (1000 nodes)"""
    print()
    print("="*80)
    print("SCENARIO 3: Mega Cluster (1000 GPUs)")
    print("="*80)
    
    cluster = GPUCluster("Mega Cluster", num_nodes=1000, ops_per_sec_per_node=1e6)
    
    # Setup puzzle
    secret_key = random.randint(1, N-1)
    target_public = point_multiply(secret_key, G, P, a)
    
    print(f"Secret key (hidden): {secret_key}")
    print(f"Target public key: {target_public}")
    
    # Distribute and search
    cluster.distribute_workload(N, verbose=False)
    print("\n📊 WORKLOAD DISTRIBUTION (condensed)")
    print(f"Total search space: {N}")
    print(f"Number of nodes: 1000")
    print(f"Keys per node: {N//1000}")
    
    cluster.coordinate_search(target_public, verbose=True)
    
    return cluster.get_cluster_stats()

def scenario_real_world():
    """Scenario: Real-world Puzzle #71"""
    print()
    print("="*80)
    print("REAL-WORLD SCENARIO: Bitcoin Puzzle #71")
    print("="*80)
    print()
    
    print("📋 PUZZLE #71 PARAMETERS")
    print("-"*80)
    print(f"Target address: 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU")
    print(f"Reward: 7.10154982 BTC (~$300,000+)")
    print(f"Search space: 2^270 to 2^271 (~3.7 × 10^81 keys)")
    print()
    
    scenarios_data = [
        {
            'name': '1 GPU (V100)',
            'gpus': 1,
            'ops_per_sec': 1e9,
            'time_years': 10**30
        },
        {
            'name': '100 GPUs',
            'gpus': 100,
            'ops_per_sec': 1e11,
            'time_years': 10**28
        },
        {
            'name': '1,000 GPUs',
            'gpus': 1000,
            'ops_per_sec': 1e12,
            'time_years': 1.5
        },
        {
            'name': '10,000 GPUs',
            'gpus': 10000,
            'ops_per_sec': 1e13,
            'time_years': 0.15
        },
        {
            'name': '100,000 GPUs',
            'gpus': 100000,
            'ops_per_sec': 1e14,
            'time_years': 0.015
        },
    ]
    
    print("⏱️  TIME ESTIMATES (Average Case)")
    print("-"*80)
    print(f"{'Configuration':<20} {'GPUs':<10} {'Time':<20} {'Cost/Day':<15}")
    print("-"*80)
    
    for scenario in scenarios_data:
        cost_per_day = scenario['gpus'] * 0.30  # $0.30/GPU/hour
        
        if scenario['time_years'] < 1:
            time_str = f"{scenario['time_years']*365:.0f} days"
        elif scenario['time_years'] < 1000:
            time_str = f"{scenario['time_years']:.1f} years"
        else:
            time_str = f"~10^{int(math.log10(scenario['time_years']))}"
        
        print(f"{scenario['name']:<20} {scenario['gpus']:<10,} {time_str:<20} ${cost_per_day:<14,.0f}")
    
    print()
    print("💡 KEY INSIGHTS")
    print("-"*80)
    print("• With current technology, Puzzle #71 is economically infeasible")
    print("• Would require >10,000 GPUs for ~1 year of computation")
    print("• Cost: ~$3-5 million for continuous operation")
    print("• Even then, no guarantee (probabilistic algorithm)")
    print()

# ========================
# COMPARISON
# ========================

def compare_clusters():
    """Compare performance across scenarios"""
    print()
    print("="*80)
    print("📊 CLUSTER PERFORMANCE COMPARISON")
    print("="*80)
    print()
    
    stats = []
    
    print("Running Scenario 1 (10 nodes)...")
    stat1 = scenario_small_cluster()
    stats.append(stat1)
    time.sleep(0.5)
    
    print("\n" + "="*80)
    print("Running Scenario 2 (100 nodes)...")
    stat2 = scenario_medium_cluster()
    stats.append(stat2)
    time.sleep(0.5)
    
    print("\n" + "="*80)
    print("Running Scenario 3 (1000 nodes)...")
    stat3 = scenario_mega_cluster()
    stats.append(stat3)
    
    print("\n" + "="*80)
    print("🏆 PERFORMANCE SUMMARY")
    print("="*80)
    print()
    print(f"{'Configuration':<20} {'Nodes':<10} {'Time':<12} {'Speed':<15} {'Efficiency':<12}")
    print("-"*80)
    
    for stat in stats:
        efficiency = stat['efficiency']
        print(f"{stat['cluster_name']:<20} {stat['num_nodes']:<10} "
              f"{stat['total_time']:<12.3f}s {stat['keys_per_second']:<15,.0f} "
              f"{efficiency:<12.1f}%")
    
    print()
    print("📈 SPEEDUP ANALYSIS")
    print("-"*80)
    
    # Calculate speedups
    if len(stats) >= 2:
        speedup_2_vs_1 = stats[0]['total_time'] / stats[1]['total_time'] if stats[1]['total_time'] > 0 else 0
        speedup_3_vs_1 = stats[0]['total_time'] / stats[2]['total_time'] if stats[2]['total_time'] > 0 else 0
        
        print(f"Scenario 2 vs Scenario 1: {speedup_2_vs_1:.2f}x faster")
        print(f"Scenario 3 vs Scenario 1: {speedup_3_vs_1:.2f}x faster")
        print()
        
        ideal_speedup_2 = 10  # 100 nodes / 10 nodes
        ideal_speedup_3 = 100  # 1000 nodes / 10 nodes
        
        efficiency_2 = (speedup_2_vs_1 / ideal_speedup_2) * 100
        efficiency_3 = (speedup_3_vs_1 / ideal_speedup_3) * 100
        
        print(f"Actual efficiency (Scenario 2): {efficiency_2:.1f}%")
        print(f"Actual efficiency (Scenario 3): {efficiency_3:.1f}%")
        print()
        print("Note: Perfect scaling would be 100%. Network latency reduces this.")

# ========================
# MAIN MENU
# ========================

def main():
    while True:
        print()
        print("="*80)
        print("🖥️  DISTRIBUTED ATTACK SIMULATOR MENU")
        print("="*80)
        print()
        print("1. 🔍 Scenario 1: Small Cluster (10 GPUs)")
        print("2. 🔍 Scenario 2: Medium Cluster (100 GPUs)")
        print("3. 🔍 Scenario 3: Mega Cluster (1000 GPUs)")
        print("4. 📊 Compare All Scenarios")
        print("5. 🌍 Real-World: Puzzle #71 Analysis")
        print("6. ❌ Exit")
        print()
        
        choice = input("Choose scenario (1-6): ").strip()
        
        if choice == '1':
            scenario_small_cluster()
        
        elif choice == '2':
            scenario_medium_cluster()
        
        elif choice == '3':
            scenario_mega_cluster()
        
        elif choice == '4':
            compare_clusters()
        
        elif choice == '5':
            scenario_real_world()
        
        elif choice == '6':
            print()
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")

# ========================
# RUN
# ========================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("👋 Interrupted. Goodbye!")
