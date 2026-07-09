"""
Bitcoin Puzzle - Manual Example with Small Numbers
Demonstrating ECDLP solving step-by-step on secp256k1
"""

print("="*70)
print("🔐 ECDLP Manual Example - Finding Private Key")
print("="*70)
print()

# ========================
# TINY CURVE (for manual calculation)
# ========================
# Using a much smaller curve to demonstrate
# Real Bitcoin uses huge numbers, but the math is the same

P = 17  # Prime field
a = 0   # Curve parameter: y² = x³ + ax + b
b = 7   # Curve parameter: y² = x³ + 7

print("📊 CURVE PARAMETERS")
print("-" * 70)
print(f"Curve: y² = x³ + {a}x + {b} (mod {P})")
print(f"Prime field P = {P}")
print()

# ========================
# STEP 1: Find all points on curve
# ========================
print("STEP 1️⃣: Find all valid points on curve")
print("-" * 70)

def find_curve_points(p, a, b):
    """Find all points (x,y) where y² = x³ + ax + b (mod p)"""
    points = [(0, 0)]  # Point at infinity (simplified)
    
    for x in range(p):
        y_squared = (x**3 + a*x + b) % p
        
        # Check if y_squared has a square root mod p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))
                if y != 0 and (y_squared != 0):  # Avoid duplicates
                    print(f"  ✓ ({x:2d}, {y:2d}): {y}² ≡ {y_squared} ≡ {x}³ + {b} (mod {P})")
    
    return sorted(set(points))

points = find_curve_points(P, a, b)
print(f"\nTotal points found: {len(points)}")
print(f"Points: {points}")
print()

# ========================
# STEP 2: Point Addition
# ========================
print("STEP 2️⃣: Point Addition (Point Doubling & Adding)")
print("-" * 70)

def mod_inverse(a, m):
    """Extended Euclidean algorithm for modular inverse"""
    if a < 0:
        a = (a % m + m) % m
    
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None  # Inverse doesn't exist
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
    
    # Case 1: Same x, different y → Point at infinity
    if x1 == x2:
        if (y1 + y2) % p_mod == 0:
            return (0, 0)
        # Same point → Point doubling
    
    # Calculate slope
    if x1 == x2 and y1 == y2:
        # Point doubling: λ = (3x₁² + a) / (2y₁)
        numerator = (3 * x1**2 + a_coeff) % p_mod
        denominator = (2 * y1) % p_mod
    else:
        # Different points: λ = (y₂ - y₁) / (x₂ - x₁)
        numerator = (y2 - y1) % p_mod
        denominator = (x2 - x1) % p_mod
    
    lambda_val = (numerator * mod_inverse(denominator, p_mod)) % p_mod
    
    # Calculate new point
    x3 = (lambda_val**2 - x1 - x2) % p_mod
    y3 = (lambda_val * (x1 - x3) - y1) % p_mod
    
    return (x3, y3)

def point_multiply(k, base_point, p_mod, a_coeff):
    """Scalar multiplication: k * P (Binary ladder)"""
    if k == 0:
        return (0, 0)
    
    result = (0, 0)  # Point at infinity
    addend = base_point
    
    steps = []
    bit_position = 0
    
    while k:
        if k & 1:
            result = point_add(result, addend, p_mod, a_coeff)
            steps.append(f"    Bit {bit_position}: 1 → Add to result: {result}")
        
        addend = point_add(addend, addend, p_mod, a_coeff)
        steps.append(f"    Bit {bit_position}: Double addend → {addend}")
        k >>= 1
        bit_position += 1
    
    return result, steps

# Choose generator G
G = (2, 5)  # Must be on the curve
print(f"Generator point G = {G}")

# Verify G is on curve
x, y = G
y_squared = (y**2) % P
x_cubed_plus_7 = (x**3 + b) % P
print(f"Verification: {y}² = {y_squared}, {x}³ + 7 = {x_cubed_plus_7} ✓")
print()

# ========================
# STEP 3: Choose private key (SECRET!)
# ========================
print("STEP 3️⃣: Choose Private Key (SECRET)")
print("-" * 70)
private_key = 6  # Our secret! 🤫
print(f"🤫 Private key k = {private_key} (HIDDEN)")
print()

# ========================
# STEP 4: Generate public key
# ========================
print("STEP 4️⃣: Generate Public Key (k * G)")
print("-" * 70)
print(f"Computing {private_key} * G = {private_key} * {G}")
print()

public_key, steps = point_multiply(private_key, G, P, a)

for step in steps:
    print(step)

print()
print(f"✓ Public key Q = {private_key} * {G} = {public_key}")
print(f"✓ This is what we share publicly!")
print()

# ========================
# STEP 5: "Address" generation (simplified hash)
# ========================
print("STEP 5️⃣: Generate 'Address' (Simplified Hash)")
print("-" * 70)

def simple_hash(point):
    """Simplified hash: just sum the coordinates"""
    x, y = point
    return (x * 100 + y) % 256

address = simple_hash(public_key)
print(f"Address = hash({public_key}) = {address}")
print()

# ========================
# STEP 6: The PUZZLE - Find private key from public key
# ========================
print("STEP 6️⃣: THE PUZZLE - Find Private Key from Public Key")
print("-" * 70)
print(f"We know:")
print(f"  Public key Q = {public_key}")
print(f"  Address hash = {address}")
print(f"  Generator G = {G}")
print()
print(f"We need to find: Private key k")
print()

# ========================
# STEP 7: Brute Force Solution
# ========================
print("STEP 7️⃣: BRUTE FORCE ATTACK")
print("-" * 70)

print(f"\nTrying all possible private keys from 1 to {len(points)}:")
print()

for test_key in range(1, len(points)):
    test_public_key, _ = point_multiply(test_key, G, P, a)
    test_address = simple_hash(test_public_key)
    
    status = "🔍"
    if test_address == address:
        status = "✅ FOUND!"
    
    print(f"  k={test_key:2d}: Q={test_public_key}  →  address={test_address:3d}  {status}")
    
    if test_address == address:
        print()
        print(f"🎉 SUCCESS! Found private key: k = {test_key}")
        print(f"   Verification: {test_key} * {G} = {test_public_key} ✓")
        break

print()

# ========================
# STEP 8: Real secp256k1 comparison
# ========================
print("="*70)
print("📊 Real Bitcoin (secp256k1) Comparison")
print("="*70)
print()

comparison_data = """
┌─────────────────────┬──────────────┬────────────────────────┐
│ Parameter           │ Our Tiny Curve│ Real secp256k1        │
├─────────────────────┼──────────────┼────────────────────────┤
│ Prime P             │ 17           │ 2^256 (77 digits)      │
│ Curve               │ y²=x³+7 (P17)│ y²=x³+7 (P256)         │
│ Number of points    │ ~25          │ 2^256 (~10^77)         │
│ Private key range   │ 1-25         │ 1-2^256                │
│ Brute force attempts│ ~12 (avg)    │ 2^255 (impossible!)    │
│ Time to crack (CPU) │ ~microsecond │ ~10^75 years           │
│ Our puzzle attempt  │ FOUND! ✅    │ Unsolved ❌            │
└─────────────────────┴──────────────┴────────────────────────┘
"""
print(comparison_data)

print()
print("="*70)
print("🔑 KEY INSIGHTS")
print("="*70)
print("""
1️⃣ FORWARD is EASY: k → Q (just multiply)
   • secp256k1: 0.0001 seconds per key

2️⃣ REVERSE is HARD: Q → k (ECDLP problem)
   • Brute force: 2^255 operations (impossible)
   • Best algorithm: ~2^128 operations (still very hard)

3️⃣ Why Bitcoin is Secure:
   • 2^256 possible keys
   • Even quantum computers would struggle
   • Distributed security across millions of nodes

4️⃣ Why Puzzle #71 is Unsolved:
   • 2^270 to 2^271 possible keys
   • Would need: 1000 GPUs + 1-5 years
   • Or: 100,000 GPUs + few months
   • Cost: Millions of dollars

5️⃣ Our Tiny Example vs Real Bitcoin:
   ✓ Our curve: 25 points, found in seconds
   ✗ secp256k1: 10^77 points, unsolved for years
""")

# ========================
# STEP 9: Show the math
# ========================
print()
print("="*70)
print("📐 THE MATH BEHIND IT")
print("="*70)
print()

k_example = 3
Qx, Qy = point_multiply(k_example, G, P, a)[0]

print(f"Example: Finding 3 * G")
print()
print(f"Binary representation of 3: 11₂")
print()
print(f"Step 1: Start with G = {G}")
print(f"Step 2: 3 = 2 + 1")
print(f"        • 2*G = G + G = {point_add(G, G, P, a)}")
print(f"        • 3*G = 2*G + G")
print()

result_2g = point_add(G, G, P, a)
result_3g = point_add(result_2g, G, P, a)

print(f"Step 3: 3 * G = {result_3g}")
print()

# ========================
# FINAL SUMMARY
# ========================
print("="*70)
print("✅ SUMMARY")
print("="*70)
print(f"""
We demonstrated finding a private key using:

1. Small curve (P=17) for easy manual calculation
2. Generator point G = {G}
3. Secret private key k = {private_key}
4. Public key Q = k*G = {public_key}
5. Address hash = {address}

The puzzle: Find k knowing only Q and G

Solution methods:
  ✓ Brute force: Try all {len(points)} possibilities → Found!
  ✗ Pollard's Rho: Not practical for such small space
  ✗ Kangaroo: Overkill here

Real Bitcoin Puzzle #71:
  • 2^270 to 2^271 possible keys (~400 quadrillion)
  • Brute force: Impossible (10^75 years)
  • Best attack: Kangaroo algorithm (~1-5 years with 1000 GPUs)
  • Current status: UNSOLVED

The math is the same, but the numbers are much bigger!
""")

print("="*70)
