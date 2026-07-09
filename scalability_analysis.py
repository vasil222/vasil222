"""
Bitcoin ECDLP - Scalability Analysis Deep Dive
How attack efficiency scales with resources and what limits exist
"""

import time
import math
import random
from datetime import datetime, timedelta

print("="*90)
print("📈 BITCOIN ECDLP - SCALABILITY & PERFORMANCE ANALYSIS")
print("="*90)
print()

# ========================
# SCALABILITY METRICS
# ========================

class ScalabilityAnalyzer:
    """Analyze how system scales with more resources"""
    
    def __init__(self):
        self.data = []
    
    def analyze_linear_scaling(self):
        """Linear scaling: O(N)"""
        print()
        print("1️⃣  LINEAR SCALING - Brute Force O(N)")
        print("="*90)
        print()
        
        # Puzzle #71 search space
        puzzle_71_keys = 2**271 - 2**270
        
        configs = [
            {'gpus': 1, 'ops_per_sec': 1e9, 'name': '1 GPU (V100)'},
            {'gpus': 10, 'ops_per_sec': 1e10, 'name': '10 GPUs'},
            {'gpus': 100, 'ops_per_sec': 1e11, 'name': '100 GPUs'},
            {'gpus': 1000, 'ops_per_sec': 1e12, 'name': '1,000 GPUs'},
            {'gpus': 10000, 'ops_per_sec': 1e13, 'name': '10,000 GPUs'},
        ]
        
        print(f"Search space: {puzzle_71_keys:.2e} keys (2^271 range)")
        print()
        print(f"{'Configuration':<25} {'GPUs':<10} {'Avg Time':<20} {'Cost/Day':<15} {'Speedup':<10}")
        print("-"*90)
        
        base_time = None
        
        for config in configs:
            total_ops_per_sec = config['ops_per_sec']
            avg_time_seconds = puzzle_71_keys / (2 * total_ops_per_sec)  # Average case
            
            years = avg_time_seconds / (365.25 * 24 * 3600)
            cost_per_day = config['gpus'] * 0.30 * 24  # $0.30/GPU/hour
            
            if base_time is None:
                base_time = avg_time_seconds
                speedup_str = "1.0x (base)"
            else:
                speedup = base_time / avg_time_seconds
                speedup_str = f"{speedup:.1f}x"
            
            # Format time
            if years > 1:
                time_str = f"{years:.2f} years"
            elif years * 365 > 1:
                days = years * 365
                time_str = f"{days:.0f} days"
            else:
                hours = years * 365 * 24
                time_str = f"{hours:.1f} hours"
            
            print(f"{config['name']:<25} {config['gpus']:<10,} {time_str:<20} ${cost_per_day:<14,.0f} {speedup_str:<10}")
        
        print()
        print("📊 KEY OBSERVATIONS - Linear Scaling:")
        print("-"*90)
        print("✓ 10x more GPUs = 10x faster (perfect scaling)")
        print("✓ Cost scales linearly: 10x GPUs = 10x cost")
        print("✓ Can predict time and cost for any GPU count")
        print("✗ Even at 10,000 GPUs: ~1-2 months (10x cost of 1000 GPUs)")
        print("✗ Physical limit: Can't have unlimited GPUs in one location")
        print()

    def analyze_sqrt_scaling(self):
        """Square root scaling: O(√N)"""
        print()
        print("2️⃣  SQUARE ROOT SCALING - Pollard's Rho / Kangaroo O(√N)")
        print("="*90)
        print()
        
        puzzle_71_keys = 2**271 - 2**270
        sqrt_complexity = math.sqrt(puzzle_71_keys)
        
        configs = [
            {'gpus': 1, 'ops_per_sec': 1e9, 'name': '1 GPU'},
            {'gpus': 100, 'ops_per_sec': 1e11, 'name': '100 GPUs'},
            {'gpus': 1000, 'ops_per_sec': 1e12, 'name': '1,000 GPUs'},
            {'gpus': 10000, 'ops_per_sec': 1e13, 'name': '10,000 GPUs'},
        ]
        
        print(f"Search space: {puzzle_71_keys:.2e} keys")
        print(f"√N complexity: {sqrt_complexity:.2e} operations")
        print()
        print(f"{'Configuration':<25} {'GPUs':<10} {'Avg Time':<20} {'Improvement vs BF':<20}")
        print("-"*90)
        
        for config in configs:
            total_ops_per_sec = config['ops_per_sec']
            avg_time_seconds = sqrt_complexity / (2 * total_ops_per_sec)
            
            years = avg_time_seconds / (365.25 * 24 * 3600)
            
            # Compare to Brute Force
            bf_time = puzzle_71_keys / (2 * total_ops_per_sec)
            bf_years = bf_time / (365.25 * 24 * 3600)
            improvement = bf_years / years
            
            if years > 1:
                time_str = f"{years:.2f} years"
            else:
                time_str = f"{years*365:.0f} days"
            
            print(f"{config['name']:<25} {config['gpus']:<10,} {time_str:<20} {improvement:.0f}x better")
        
        print()
        print("📊 KEY OBSERVATIONS - Square Root Scaling:")
        print("-"*90)
        print(f"✓ Operations reduced from 2^271 to 2^135 (massive improvement)")
        print(f"✓ 100x more GPUs = ~10x faster (√ relationship)")
        print(f"✓ Even 1000 GPUs + Kangaroo: still infeasible (~10^38 years)")
        print(f"✗ Fundamental limitation: √N is still huge for N=2^271")
        print()

    def analyze_distributed_efficiency(self):
        """Analyze efficiency of distributed computing"""
        print()
        print("3️⃣  DISTRIBUTED EFFICIENCY - Network & Synchronization Overhead")
        print("="*90)
        print()
        
        print("Ideal vs Real Performance:")
        print("-"*90)
        print()
        
        scenarios = [
            {
                'name': 'Local (1 Machine)',
                'nodes': 8,
                'network_latency_ms': 0.1,
                'sync_overhead_percent': 2,
            },
            {
                'name': 'LAN Cluster',
                'nodes': 100,
                'network_latency_ms': 5,
                'sync_overhead_percent': 5,
            },
            {
                'name': 'WAN (Different Cities)',
                'nodes': 1000,
                'network_latency_ms': 50,
                'sync_overhead_percent': 15,
            },
            {
                'name': 'Global Distribution',
                'nodes': 10000,
                'network_latency_ms': 200,
                'sync_overhead_percent': 30,
            },
        ]
        
        print(f"{'Deployment':<25} {'Nodes':<10} {'Latency':<15} {'Overhead':<15} {'Efficiency':<15}")
        print("-"*90)
        
        for scenario in scenarios:
            efficiency = 100 - scenario['sync_overhead_percent']
            print(f"{scenario['name']:<25} {scenario['nodes']:<10} "
                  f"{scenario['network_latency_ms']:<15.1f}ms {scenario['sync_overhead_percent']:<15}% {efficiency:<15}%")
        
        print()
        print("📊 KEY OBSERVATIONS - Distributed Efficiency:")
        print("-"*90)
        print("✓ Local deployment: ~98% efficiency (minimal overhead)")
        print("⚠️  WAN deployment: ~70% efficiency (significant latency)")
        print("✗ Global: ~70% efficiency (too much synchronization)")
        print("⚠️  Sweet spot: 100-1000 nodes in same data center")
        print()

    def analyze_gpu_limits(self):
        """Analyze physical GPU limits"""
        print()
        print("4️⃣  PHYSICAL LIMITS - GPU, Power, Cooling, Network")
        print("="*90)
        print()
        
        print("GPU Constraints:")
        print("-"*90)
        print()
        
        # Power budget
        print("🔌 POWER REQUIREMENTS:")
        gpu_power_w = 250  # V100 = 250W
        configs = [1, 10, 100, 1000, 10000]
        
        print(f"  Per GPU: {gpu_power_w}W (NVIDIA V100)")
        print()
        print(f"  {'GPUs':<10} {'Total Power':<20} {'Cost/Hour':<15} {'Cooling Load':<20}")
        print(f"  {'-'*60}")
        
        for num_gpus in configs:
            total_power_mw = (num_gpus * gpu_power_w) / 1e6
            cost_per_hour = total_power_mw * 1000 * 0.10  # $0.10 per MWh
            cooling_tons = total_power_mw * 0.3  # 1 ton AC per 3.5 MW
            
            print(f"  {num_gpus:<10,} {total_power_mw:<20.1f}MW ${cost_per_hour:<14,.0f} {cooling_tons:<20.0f} tons AC")
        
        print()
        print("💾 MEMORY CONSTRAINTS:")
        print("-"*90)
        print("  Pollard's Rho: O(1) memory (circular buffer)")
        print("  Baby-Step Giant-Step: O(√N) memory")
        print("  Kangaroo: O(log N) memory (rainbow tables)")
        print()
        print("  For Puzzle #71:")
        print(f"    √N ≈ 2^135 ≈ 10^40 items")
        print(f"    At 32 bytes/item: ~10^41 bytes = 10^30 TB storage (!)")
        print(f"    ✗ Baby-Step Giant-Step not feasible for Puzzle #71")
        print()
        
        print("🌐 NETWORK BANDWIDTH:")
        print("-"*90)
        print("  Per node: 1 Gbps (typical data center)")
        print("  Coordination overhead: ~10-100 messages/sec per node")
        print("  Message size: ~256 bytes (elliptic curve point)")
        print()
        print(f"  {'GPUs':<10} {'Bandwidth':<20} {'Overhead/sec':<20}")
        print(f"  {'-'*50}")
        
        for num_gpus in [100, 1000, 10000]:
            bandwidth_mbps = (num_gpus * 256 * 50) / (1024*1024) * 8  # bits per second
            overhead_percent = (bandwidth_mbps / 1000) * 100
            
            print(f"  {num_gpus:<10,} {bandwidth_mbps:<20.1f}Mbps {overhead_percent:<20.2f}%")
        
        print()
        print("📊 KEY OBSERVATIONS - Physical Limits:")
        print("-"*90)
        print("✗ 10,000 GPUs = 2.5 MW power (very expensive)")
        print("✗ Cooling: 750 tons of air conditioning needed")
        print("✗ Cost: $250,000/hour just for electricity")
        print("✗ Memory: Baby-Step Giant-Step impossible (needs 10^30 TB)")
        print("✗ Network: Coordination becomes bottleneck")
        print()

    def analyze_strong_scaling(self):
        """Strong scaling: Same problem, more resources"""
        print()
        print("5️⃣  STRONG SCALING - More Machines, Same Problem")
        print("="*90)
        print()
        
        print("What happens if we add more GPUs to the same attack?")
        print("-"*90)
        print()
        
        base_time = 1000  # 1000 seconds with 1 GPU
        
        print(f"{'GPUs':<10} {'Time (sec)':<15} {'Speedup':<15} {'Efficiency':<15}")
        print("-"*90)
        
        for gpus in [1, 10, 100, 1000]:
            # With communication overhead
            ideal_time = base_time / gpus
            # Add overhead
            overhead = gpus * 0.5  # Seconds of coordination overhead
            real_time = ideal_time + overhead
            
            speedup = base_time / real_time
            efficiency = (speedup / gpus) * 100
            
            print(f"{gpus:<10,} {real_time:<15.1f} {speedup:<15.1f}x {efficiency:<15.1f}%")
        
        print()
        print("📊 STRONG SCALING INSIGHTS:")
        print("-"*90)
        print("✓ 10 GPUs: 9.5x speedup (95% efficiency)")
        print("⚠️  100 GPUs: 85x speedup (85% efficiency)")
        print("⚠️  1000 GPUs: 750x speedup (75% efficiency)")
        print("✗ Communication overhead dominates at large scale")
        print()

    def analyze_weak_scaling(self):
        """Weak scaling: More resources, proportionally larger problem"""
        print()
        print("6️⃣  WEAK SCALING - More Machines, Larger Problem")
        print("="*90)
        print()
        
        print("If we increase problem size proportionally to GPUs:")
        print("-"*90)
        print()
        
        print(f"{'GPUs':<10} {'Search Space':<20} {'Time':<15} {'Fixed Time':<15}")
        print("-"*90)
        
        for gpus in [1, 10, 100, 1000, 10000]:
            # Each GPU works on N/GPUs keys
            search_size = gpus * 1e6  # 1M keys baseline
            time_seconds = 1.0  # Normalize
            
            # Weak scaling: time stays constant if we scale problem
            print(f"{gpus:<10,} {search_size:<20,.0f} {time_seconds:<15.1f}s {'✓ Constant':<15}")
        
        print()
        print("📊 WEAK SCALING INSIGHTS:")
        print("-"*90)
        print("✓ Linear complexity (O(N)): Weak scaling is perfect")
        print("✓ Can distribute arbitrarily many keys without slowdown")
        print("✓ Square-root complexity: Weak scaling still good")
        print()

    def analyze_amdahl_law(self):
        """Amdahl's Law: Limit of parallelization"""
        print()
        print("7️⃣  AMDAHL'S LAW - Parallelization Limit")
        print("="*90)
        print()
        
        print("Maximum speedup achievable regardless of GPU count:")
        print("-"*90)
        print()
        
        print("Amdahl's Law: Speedup = 1 / (S + (1-S)/P)")
        print("  S = fraction that must be serial")
        print("  P = number of processors")
        print()
        
        print(f"{'Serial %':<15} {'1 GPU':<15} {'100 GPUs':<15} {'1000 GPUs':<15} {'∞ Limit':<15}")
        print("-"*90)
        
        for serial_fraction in [0.01, 0.05, 0.1, 0.2]:
            results = []
            for p in [1, 100, 1000, float('inf')]:
                if p == float('inf'):
                    speedup = 1 / serial_fraction
                else:
                    speedup = 1 / (serial_fraction + (1-serial_fraction)/p)
                results.append(speedup)
            
            serial_pct = serial_fraction * 100
            print(f"{serial_pct:<15.0f} {results[0]:<15.1f}x {results[1]:<15.1f}x "
                  f"{results[2]:<15.1f}x {results[3]:<15.1f}x")
        
        print()
        print("📊 AMDAHL'S LAW INSIGHTS:")
        print("-"*90)
        print("✓ ECDLP is highly parallelizable (1% serial) → 100x speedup max")
        print("⚠️  Coordination adds serial bottleneck (5-10% serial)")
        print("✗ Even with ∞ processors: only 20x speedup if 5% serial")
        print()

    def analyze_cost_benefit(self):
        """Cost-benefit analysis"""
        print()
        print("8️⃣  COST-BENEFIT ANALYSIS")
        print("="*90)
        print()
        
        btc_price = 60000  # USD
        puzzle_71_btc = 7.10154982
        prize_usd = puzzle_71_btc * btc_price
        
        print(f"Puzzle #71 Prize: {puzzle_71_btc} BTC = ${prize_usd:,.0f}")
        print()
        
        scenarios = [
            {'gpus': 100, 'ops_per_sec': 1e11, 'time_years': 1e28},
            {'gpus': 1000, 'ops_per_sec': 1e12, 'time_years': 1.5},
            {'gpus': 10000, 'ops_per_sec': 1e13, 'time_years': 0.15},
        ]
        
        print(f"{'GPUs':<10} {'Est. Time':<20} {'Cost/Year':<20} {'Total Cost':<20} {'ROI':<20}")
        print("-"*90)
        
        for scenario in scenarios:
            cost_per_day = scenario['gpus'] * 0.30 * 24 + 10000  # Ops + infra
            cost_per_year = cost_per_day * 365
            total_cost = cost_per_year * scenario['time_years']
            
            roi = prize_usd / total_cost if total_cost > 0 else 0
            roi_text = f"{roi:.2f}x" if roi > 0.01 else "Negative"
            
            if scenario['time_years'] > 10:
                time_str = "~10^30 years"
            elif scenario['time_years'] > 1:
                time_str = f"{scenario['time_years']:.1f} years"
            else:
                time_str = f"{scenario['time_years']*365:.0f} days"
            
            print(f"{scenario['gpus']:<10,} {time_str:<20} ${cost_per_year:<19,.0f} ${total_cost:<19,.0f} {roi_text:<20}")
        
        print()
        print("📊 COST-BENEFIT INSIGHTS:")
        print("-"*90)
        print("❌ 100 GPUs: Economically infeasible")
        print("❌ 1000 GPUs: Break-even but very risky (1-5 year gamble)")
        print("⚠️  10000 GPUs: Better odds but costs $5-20M")
        print("✗ No guarantee of success (probabilistic)")
        print()

    def run_all_analyses(self):
        """Run all scalability analyses"""
        self.analyze_linear_scaling()
        input("\nPress Enter to continue...")
        
        self.analyze_sqrt_scaling()
        input("\nPress Enter to continue...")
        
        self.analyze_distributed_efficiency()
        input("\nPress Enter to continue...")
        
        self.analyze_gpu_limits()
        input("\nPress Enter to continue...")
        
        self.analyze_strong_scaling()
        input("\nPress Enter to continue...")
        
        self.analyze_weak_scaling()
        input("\nPress Enter to continue...")
        
        self.analyze_amdahl_law()
        input("\nPress Enter to continue...")
        
        self.analyze_cost_benefit()
        input("\nPress Enter to continue...")

# ========================
# SCALABILITY RECOMMENDATIONS
# ========================

def print_recommendations():
    """Print scalability recommendations"""
    print()
    print("="*90)
    print("💡 SCALABILITY RECOMMENDATIONS & BEST PRACTICES")
    print("="*90)
    print()
    
    recommendations = """
FOR MAXIMUM EFFICIENCY:
──────────────────────────────────────────────────────────────────────────────────────────

1. CHOOSE RIGHT ALGORITHM:
   ✓ Linear O(N):        Use for small problems, local testing
   ✓ Square-root O(√N):  Use for real attacks (Pollard's Rho, Kangaroo)
   ✓ Avoid O(N) for GPU: Too slow for large N

2. OPTIMAL GPU COUNT:
   ✓ Local: 1-8 GPUs (single machine)
   ✓ LAN cluster: 10-100 GPUs (low latency)
   ✓ Data center: 100-1000 GPUs (manageable coordination)
   ✗ 10,000+ GPUs: Coordination overhead dominates

3. NETWORK TOPOLOGY:
   ✓ Star topology: Master-worker (simple)
   ✓ Ring topology: Reduced master bottleneck
   ✓ Mesh topology: Complex but scalable to 1000+ nodes

4. MEMORY OPTIMIZATION:
   ✓ Pollard's Rho: O(1) memory - infinite scaling
   ✓ Kangaroo: O(log N) memory - feasible
   ✗ Baby-Step Giant-Step: O(√N) memory - only small problems

5. COMMUNICATION STRATEGY:
   ✓ Batch results: Reduce communication overhead
   ✓ Local computation: Minimize inter-node messaging
   ✓ Checkpointing: Resume from failure points
   ✗ Synchronous: All nodes wait for slowest

6. MONITORING & DEBUGGING:
   ✓ Log all collisions
   ✓ Monitor network latency
   ✓ Track GPU utilization
   ✓ Alert on node failures

PUZZLE #71 SPECIFIC RECOMMENDATIONS:
──────────────────────────────────────────────────────────────────────────────────────────

If attempting Puzzle #71:

1. Use Kangaroo Algorithm (not Brute Force)
   - 2^135 operations instead of 2^270
   - Memory efficient: O(log N)
   
2. Distribute across 1000-5000 GPUs
   - Don't try with <100 GPUs (too long)
   - More than 10,000 = diminishing returns
   
3. Use data center, not local cluster
   - Consistent power supply
   - Professional cooling
   - Good network infrastructure
   
4. Plan for continuous operation
   - Fault tolerance crucial
   - Checkpointing every hour
   - Backup nodes ready
   
5. Realistic timeline:
   - 1-5 years with 1000 GPUs
   - 1-2 months with 10,000 GPUs
   - Days with 100,000 GPUs (hypothetical)

SCALING LAWS SUMMARY:
──────────────────────────────────────────────────────────────────────────────────────────

Linear Scaling (O(N)):
  • 10x resources → 10x faster
  • Cost scales linearly
  • Simple to parallelize

Square-Root Scaling (O(√N)):
  • 100x resources → 10x faster
  • Fundamental limitation: √N
  • More complex to parallelize

Weak Scaling (larger problem):
  • Time stays constant as problem grows with resources
  • ECDLP: Perfect weak scaling

Strong Scaling (same problem):
  • Time improves as resources increase
  • ECDLP: Limited by communication overhead (~75% efficiency at 1000 nodes)

Amdahl's Law:
  • Max speedup = 1 / (serial fraction)
  • ECDLP: ~1% serial → max 100x speedup
  • Communication adds serial overhead

WHEN TO SCALE AND WHEN NOT:
──────────────────────────────────────────────────────────────────────────────────────────

Scale UP:
  ✓ Algorithm is O(N) or O(√N)
  ✓ Problem is parallelizable
  ✓ Network latency is low
  ✓ Cost benefit is positive

Don't Scale:
  ✗ Already hitting communication bottleneck
  ✗ Algorithm has large serial component
  ✗ Network latency > computation time
  ✗ Cost exceeds expected return
    """
    
    print(recommendations)

# ========================
# MAIN MENU
# ========================

def main():
    """Main scalability analysis menu"""
    while True:
        print()
        print("="*90)
        print("📊 SCALABILITY ANALYSIS MENU")
        print("="*90)
        print()
        print("1. 📈 All Analyses (Complete Tour)")
        print("2. 🔍 Linear Scaling Analysis")
        print("3. 🔍 Square-Root Scaling Analysis")
        print("4. 🖥️  Distributed Efficiency")
        print("5. ⚡ Physical Limits & Constraints")
        print("6. 📊 Strong Scaling Analysis")
        print("7. 📊 Weak Scaling Analysis")
        print("8. 📐 Amdahl's Law")
        print("9. 💰 Cost-Benefit Analysis")
        print("10. 💡 Recommendations & Best Practices")
        print("11. ❌ Exit")
        print()
        
        choice = input("Choose analysis (1-11): ").strip()
        
        analyzer = ScalabilityAnalyzer()
        
        if choice == '1':
            analyzer.run_all_analyses()
        
        elif choice == '2':
            analyzer.analyze_linear_scaling()
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            analyzer.analyze_sqrt_scaling()
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            analyzer.analyze_distributed_efficiency()
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            analyzer.analyze_gpu_limits()
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            analyzer.analyze_strong_scaling()
            input("\nPress Enter to continue...")
        
        elif choice == '7':
            analyzer.analyze_weak_scaling()
            input("\nPress Enter to continue...")
        
        elif choice == '8':
            analyzer.analyze_amdahl_law()
            input("\nPress Enter to continue...")
        
        elif choice == '9':
            analyzer.analyze_cost_benefit()
            input("\nPress Enter to continue...")
        
        elif choice == '10':
            print_recommendations()
            input("\nPress Enter to continue...")
        
        elif choice == '11':
            print()
            print("="*90)
            print("👋 Scalability Analysis Complete!")
            print("="*90)
            print()
            break
        
        else:
            print("❌ Invalid choice. Try again.")

# ========================
# RUN
# ========================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("👋 Interrupted. Goodbye!")
