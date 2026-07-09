"""
Bitcoin ECDLP - Interactive Attack Simulator
Compare different algorithms for finding private keys
"""

import time
import random
from collections import defaultdict

print("="*80)
print("🎮 BITCOIN ECDLP - INTERACTIVE ATTACK SIMULATOR")
print("="*80)
print()

# ========================
# TINY CURVE SETUP
# ========================

P = 17  # Prime field
a = 0   # Curve: y² = x³ + 7
b = 7

def mod_inverse(a, m):
    """Extended Euclidean algorithm for modular inverse"""
    if a < 0:
        a = (a % m + m) % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def extended_gcd(a, b):
    """Extended Euclidean algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def point_add(p1, p2, p_mod, a_coeff):
    """Add two points on elliptic curve"""
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
    """Scalar multiplication: k * P"""
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

# Find all curve points
def find_curve_points(p, a, b):
    points = [(0, 0)]
    for x in range(p):
        y_squared = (x**3 + a*x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))
    return sorted(set(points))

points = find_curve_points(P, a, b)
G = (2, 5)  # Generator
N = len(points)  # Order of curve

print(f"🔧 SETUP")
print(f"-" * 80)
print(f"Curve: y² = x³ + 7 (mod {P})")
print(f"Total points: {N}")
print(f"Generator G: {G}")
print(f"Points: {points}")
print()

# ========================
# MENU SYSTEM
# ========================

def print_menu():
    print()
    print("="*80)
    print("📋 ATTACK SIMULATOR MENU")
    print("="*80)
    print()
    print("1. 🔍 Brute Force Attack (Try all keys)")
    print("2. 🦘 Pollard's Rho Attack (Cycle detection)")
    print("3. 🦗 Baby-Step Giant-Step Attack (Meet-in-middle)")
    print("4. 🎯 Compare All Attacks")
    print("5. 📊 Statistics & Comparison")
    print("6. ⚙️  Configure & Run Custom Attack")
    print("7. 🆚 Battle: Different Attacks Race")
    print("8. ❌ Exit")
    print()

# ========================
# ATTACK 1: BRUTE FORCE
# ========================

def brute_force_attack(public_key, verbose=True):
    """Try all possible private keys"""
    if verbose:
        print()
        print("🔍 BRUTE FORCE ATTACK")
        print("-" * 80)
        print(f"Target public key: {public_key}")
        print(f"Searching through {N} possible keys...")
        print()
    
    start_time = time.time()
    operations = 0
    
    for test_key in range(1, N):
        test_public = point_multiply(test_key, G, P, a)
        operations += 1
        
        if verbose and test_key % max(1, N//10) == 0:
            print(f"  Tried {test_key}/{N} keys...")
        
        if test_public == public_key:
            elapsed = time.time() - start_time
            if verbose:
                print()
                print(f"✅ FOUND! Private key: {test_key}")
                print(f"   Operations: {operations}")
                print(f"   Time: {elapsed*1000:.2f}ms")
            return test_key, operations, elapsed
    
    return None, operations, time.time() - start_time

# ========================
# ATTACK 2: POLLARD'S RHO
# ========================

def pollard_rho_attack(public_key, verbose=True):
    """Pollard's Rho with cycle detection"""
    if verbose:
        print()
        print("🦘 POLLARD'S RHO ATTACK")
        print("-" * 80)
        print(f"Target public key: {public_key}")
        print("Looking for cycle in sequence...")
        print()
    
    start_time = time.time()
    operations = 0
    
    def rho_function(state):
        """Deterministic rho function"""
        x, a, b = state
        if x[0] % 3 == 0:
            return (point_add(x, x, P, a), (a*2) % N, (b*2) % N)
        elif x[0] % 3 == 1:
            return (point_add(x, G, P, a), (a+1) % N, b)
        else:
            return (point_add(x, public_key, P, a), a, (b+1) % N)
    
    # Random starting point
    x = (random.randint(0, P), random.randint(0, N), random.randint(0, N))
    y = x
    d = 1
    
    iterations = 0
    max_iterations = min(100, N)  # Limit iterations
    
    while d == 1 and iterations < max_iterations:
        x = rho_function(x)
        y = rho_function(rho_function(y))
        operations += 2
        iterations += 1
        
        if verbose and iterations % 10 == 0:
            print(f"  Iteration {iterations}... (current point: {x[0]})")
        
        # Check if cycle detected
        if x[0] == y[0]:
            # Found potential collision
            xa, xb = x[1], x[2]
            ya, yb = y[1], y[2]
            
            # Try to solve: (xa - ya) * k ≡ (yb - xb) (mod N)
            diff_b = (yb - xb) % N
            diff_a = (xa - ya) % N
            
            if diff_a != 0:
                try:
                    k = (diff_b * mod_inverse(diff_a, N)) % N
                    if k > 0:
                        test_public = point_multiply(k, G, P, a)
                        if test_public == public_key:
                            elapsed = time.time() - start_time
                            if verbose:
                                print()
                                print(f"✅ FOUND! Private key: {k}")
                                print(f"   Operations: {operations}")
                                print(f"   Iterations: {iterations}")
                                print(f"   Time: {elapsed*1000:.2f}ms")
                            return k, operations, elapsed
                except:
                    pass
    
    elapsed = time.time() - start_time
    if verbose:
        print(f"❌ Not found within {max_iterations} iterations")
    
    return None, operations, elapsed

# ========================
# ATTACK 3: BABY-STEP GIANT-STEP
# ========================

def baby_step_giant_step(public_key, verbose=True):
    """Baby-step giant-step meet-in-middle attack"""
    if verbose:
        print()
        print("🦗 BABY-STEP GIANT-STEP ATTACK")
        print("-" * 80)
        print(f"Target public key: {public_key}")
        print("Computing baby steps and giant steps...")
        print()
    
    start_time = time.time()
    operations = 0
    
    m = int(N**0.5) + 1
    
    # Baby steps: compute j*G for j = 0, 1, ..., m
    baby_steps = {}
    if verbose:
        print(f"Baby steps: computing {m} multiples of G...")
    
    for j in range(m):
        point = point_multiply(j, G, P, a)
        baby_steps[point] = j
        operations += 1
        if verbose and j % max(1, m//5) == 0:
            print(f"  {j}/{m} baby steps computed...")
    
    # Compute G_inv = -G
    gx, gy = G
    g_inv = (gx, (-gy) % P)
    
    # Giant steps: compute Q - i*m*G
    if verbose:
        print(f"Giant steps: checking {m} multiples...")
    
    gamma = point_multiply(m, g_inv, P, a)
    
    for i in range(m):
        point = point_multiply(i, gamma, P, a)
        test_point = point_add(public_key, point, P, a)
        operations += 1
        
        if test_point in baby_steps:
            j = baby_steps[test_point]
            k = (i * m + j) % N
            
            # Verify
            if point_multiply(k, G, P, a) == public_key:
                elapsed = time.time() - start_time
                if verbose:
                    print()
                    print(f"✅ FOUND! Private key: {k}")
                    print(f"   Baby steps: {m}")
                    print(f"   Giant steps: {i}")
                    print(f"   Operations: {operations}")
                    print(f"   Time: {elapsed*1000:.2f}ms")
                return k, operations, elapsed
        
        if verbose and i % max(1, m//5) == 0:
            print(f"  {i}/{m} giant steps checked...")
    
    elapsed = time.time() - start_time
    if verbose:
        print(f"❌ Not found")
    
    return None, operations, elapsed

# ========================
# MAIN INTERACTION LOOP
# ========================

def main():
    global G, P, a, N, points
    
    secret_key = None
    target_public = None
    
    while True:
        print_menu()
        choice = input("Choose attack (1-8): ").strip()
        
        # Setup puzzle
        if choice in ['1', '2', '3', '4', '6', '7']:
            if secret_key is None:
                secret_key = random.randint(1, N-1)
                target_public = point_multiply(secret_key, G, P, a)
                
                print()
                print(f"🎯 NEW PUZZLE GENERATED")
                print(f"-" * 80)
                print(f"Secret private key: {secret_key} (HIDDEN)")
                print(f"Target public key: {target_public}")
                print()
        
        # Attack 1: Brute Force
        if choice == '1':
            result, ops, elapsed = brute_force_attack(target_public, verbose=True)
            input("\nPress Enter to continue...")
        
        # Attack 2: Pollard's Rho
        elif choice == '2':
            result, ops, elapsed = pollard_rho_attack(target_public, verbose=True)
            input("\nPress Enter to continue...")
        
        # Attack 3: Baby-Step Giant-Step
        elif choice == '3':
            result, ops, elapsed = baby_step_giant_step(target_public, verbose=True)
            input("\nPress Enter to continue...")
        
        # Compare all attacks
        elif choice == '4':
            print()
            print("⚙️  COMPARING ALL ATTACKS")
            print("="*80)
            print()
            
            results = {}
            
            print("1/3 Running Brute Force...")
            result1, ops1, time1 = brute_force_attack(target_public, verbose=False)
            results['Brute Force'] = (ops1, time1)
            
            print("2/3 Running Pollard's Rho...")
            result2, ops2, time2 = pollard_rho_attack(target_public, verbose=False)
            results['Pollard\'s Rho'] = (ops2, time2)
            
            print("3/3 Running Baby-Step Giant-Step...")
            result3, ops3, time3 = baby_step_giant_step(target_public, verbose=False)
            results['Baby-Step Giant-Step'] = (ops3, time3)
            
            print()
            print("📊 COMPARISON RESULTS")
            print("="*80)
            print(f"{'Algorithm':<25} {'Operations':<15} {'Time (ms)':<15}")
            print("-"*80)
            
            for name, (ops, elapsed) in sorted(results.items(), key=lambda x: x[1][1]):
                print(f"{name:<25} {ops:<15} {elapsed*1000:<15.2f}")
            
            print()
            fastest = min(results.items(), key=lambda x: x[1][1])
            print(f"✅ Fastest: {fastest[0]} ({fastest[1][1]*1000:.2f}ms)")
            
            input("\nPress Enter to continue...")
        
        # Statistics
        elif choice == '5':
            print()
            print("📊 STATISTICS")
            print("="*80)
            print()
            print(f"Curve parameters:")
            print(f"  Prime field P: {P}")
            print(f"  Total points: {N}")
            print(f"  Generator G: {G}")
            print()
            print(f"Algorithm complexity comparison:")
            print()
            print(f"{'Algorithm':<30} {'Worst Case':<20} {'Average':<20}")
            print("-"*80)
            print(f"{'Brute Force':<30} {'O(N)':<20} {'O(N/2)':<20}")
            print(f"{'Pollard\'s Rho':<30} {'O(√N)':<20} {'O(√N)':<20}")
            print(f"{'Baby-Step Giant-Step':<30} {'O(√N)':<20} {'O(√N)':<20}")
            print()
            print(f"For this curve (N={N}):")
            print(f"  Brute Force avg: {N//2} operations")
            print(f"  Pollard's Rho avg: {int(N**0.5)} operations")
            print(f"  Baby-Step Giant-Step: {int(N**0.5)*2} operations")
            print()
            print(f"Real Bitcoin (N=2^256):")
            print(f"  Brute Force: 2^255 operations (IMPOSSIBLE)")
            print(f"  Pollard's Rho: ~2^128 operations (extremely hard)")
            print(f"  Baby-Step Giant-Step: ~2^128 operations (extremely hard)")
            print()
            
            input("Press Enter to continue...")
        
        # Custom attack
        elif choice == '6':
            print()
            print("⚙️  CUSTOM ATTACK CONFIGURATION")
            print("="*80)
            print()
            
            custom_key = input(f"Enter private key to hide (1-{N-1}): ").strip()
            try:
                custom_key = int(custom_key)
                if 1 <= custom_key < N:
                    secret_key = custom_key
                    target_public = point_multiply(secret_key, G, P, a)
                    print()
                    print(f"✓ Puzzle set with private key: {secret_key}")
                    print(f"  Target public key: {target_public}")
                else:
                    print(f"❌ Key must be between 1 and {N-1}")
            except:
                print("❌ Invalid input")
            
            input("\nPress Enter to continue...")
        
        # Race
        elif choice == '7':
            print()
            print("��� ATTACK RACE - WHO'S FASTEST?")
            print("="*80)
            print()
            print(f"Target: {target_public}")
            print()
            
            print("🏁 GO!")
            print()
            
            # Run all 3 simultaneously (timed)
            start = time.time()
            result1, _, time1 = brute_force_attack(target_public, verbose=False)
            time1_from_start = time.time() - start
            
            result2, _, time2 = pollard_rho_attack(target_public, verbose=False)
            time2_from_start = time.time() - start
            
            result3, _, time3 = baby_step_giant_step(target_public, verbose=False)
            time3_from_start = time.time() - start
            
            print()
            print("🏁 RACE RESULTS!")
            print("="*80)
            print()
            
            results_race = [
                ("🥇 1st Place", "Brute Force", time1_from_start),
                ("🥈 2nd Place", "Pollard's Rho", time2_from_start),
                ("🥉 3rd Place", "Baby-Step Giant-Step", time3_from_start),
            ]
            
            results_race.sort(key=lambda x: x[2])
            
            for medal, name, t in results_race:
                print(f"{medal:<15} {name:<25} {t*1000:>10.2f}ms")
            
            print()
            input("Press Enter to continue...")
        
        # Exit
        elif choice == '8':
            print()
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Try again.")

# ========================
# RUN SIMULATOR
# ========================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("👋 Simulator interrupted. Goodbye!")
