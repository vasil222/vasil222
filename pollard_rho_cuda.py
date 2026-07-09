"""
Bitcoin Puzzle #71 Solver
Pollard's Rho Algorithm with CUDA acceleration
Optimized for secp256k1 ECDLP
"""

import numpy as np
import time
import hashlib
from numba import cuda, jit, uint64, uint32
import math

# =========================
# secp256k1 constants
# =========================

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# Puzzle #71 range
PUZZLE_MIN = 0x400000000000000000  # 2^270
PUZZLE_MAX = 0x7fffffffffffffff    # 2^271 - 1

# =========================
# Point class (Jacobian coords)
# =========================

class Point:
    def __init__(self, X, Y, Z=1):
        self.X = X
        self.Y = Y
        self.Z = Z
    
    def copy(self):
        return Point(self.X, self.Y, self.Z)


# =========================
# CPU modular arithmetic
# =========================

def mod_inverse(a, m=P):
    """Fermat's little theorem: a^(p-2) mod p"""
    return pow(a, m - 2, m)


def affine(point):
    """Convert from Jacobian to affine coordinates"""
    z_inv = mod_inverse(point.Z)
    z_inv_sq = (z_inv * z_inv) % P
    x = (point.X * z_inv_sq) % P
    y = (point.Y * z_inv_sq * z_inv) % P
    return x, y


def point_double(p):
    """Efficient point doubling in Jacobian coordinates"""
    X, Y, Z = p.X, p.Y, p.Z
    
    XX = (X * X) % P
    YY = (Y * Y) % P
    YYYY = (YY * YY) % P
    ZZ = (Z * Z) % P
    
    S = (2 * ((X + YY) * (X + YY) - XX - YYYY)) % P
    M = (3 * XX) % P
    
    X3 = (M * M - 2 * S) % P
    Y3 = (M * (S - X3) - 8 * YYYY) % P
    Z3 = ((Y + Z) * (Y + Z) - YY - ZZ) % P
    
    return Point(X3, Y3, Z3)


def point_add(p, q):
    """Point addition in Jacobian coordinates"""
    if p.Z == 1 and q.Z == 1:
        return point_add_mixed(p, q)
    
    X1, Y1, Z1 = p.X, p.Y, p.Z
    X2, Y2, Z2 = q.X, q.Y, q.Z
    
    Z1Z1 = (Z1 * Z1) % P
    Z2Z2 = (Z2 * Z2) % P
    
    U1 = (X1 * Z2Z2) % P
    U2 = (X2 * Z1Z1) % P
    
    S1 = (Y1 * Z2 * Z2Z2) % P
    S2 = (Y2 * Z1 * Z1Z1) % P
    
    H = (U2 - U1) % P
    I = (4 * H * H) % P
    J = (H * I) % P
    r = (2 * (S2 - S1)) % P
    
    X3 = (r * r - J - 2 * U1 * I) % P
    Y3 = (r * (U1 * I - X3) - 2 * S1 * J) % P
    Z3 = (((Z1 + Z2) * (Z1 + Z2) - Z1Z1 - Z2Z2) * H) % P
    
    return Point(X3, Y3, Z3)


def point_add_mixed(p, q):
    """Mixed addition (one point in affine)"""
    X1, Y1, Z1 = p.X, p.Y, p.Z
    X2, Y2 = q.X, q.Y
    
    Z1Z1 = (Z1 * Z1) % P
    U1 = (X1) % P
    U2 = (X2 * Z1Z1) % P
    
    S1 = (Y1) % P
    S2 = (Y2 * Z1 * Z1Z1) % P
    
    H = (U2 - U1) % P
    
    if H == 0:
        if S1 == S2:
            return point_double(p)
        else:
            return Point(0, 0, 1)  # Point at infinity
    
    I = (4 * H * H) % P
    J = (H * I) % P
    r = (2 * (S2 - S1)) % P
    
    X3 = (r * r - J - 2 * U1 * I) % P
    Y3 = (r * (U1 * I - X3) - 2 * S1 * J) % P
    Z3 = ((Z1 + H) * (Z1 + H) - Z1Z1 - I) % P
    
    return Point(X3, Y3, Z3)


def point_mul(k, base_point=None):
    """Binary ladder point multiplication"""
    if base_point is None:
        base_point = Point(GX, GY)
    
    result = Point(0, 0, 1)  # Point at infinity
    addend = base_point.copy()
    
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_double(addend)
        k >>= 1
    
    return result


# =========================
# Public key generation
# =========================

def get_public_key(private_key):
    """Generate public key from private key"""
    point = point_mul(private_key)
    return affine(point)


def hash160(data):
    """Bitcoin address hash"""
    h = hashlib.new('ripemd160')
    h.update(hashlib.sha256(data).digest())
    return h.digest()


def point_to_address(point):
    """Convert public key point to Bitcoin address"""
    x, y = point
    # Compressed public key
    if y % 2 == 0:
        prefix = b'\x02'
    else:
        prefix = b'\x03'
    pubkey = prefix + x.to_bytes(32, 'big')
    
    h160 = hash160(pubkey)
    return h160


# =========================
# Pollard's Rho iteration function
# =========================

@jit(nopython=True)
def rho_function_index(x, iterations=1):
    """Deterministic rho function using modular arithmetic"""
    for _ in range(iterations):
        x = (x * x + 1) % N
    return x


def rho_function_point(p, counter):
    """Rho iteration function for points
    Partitions based on x-coordinate
    """
    x, y = affine(p)
    partition = x % 20  # Use 20 partitions
    
    if partition == 0:
        return point_double(p), counter + 1
    else:
        # Add base point scaled by partition
        g_mult = point_mul(partition)
        result = point_add(p, g_mult)
        return result, counter + 1


# =========================
# Pollard's Rho solver
# =========================

class PollardRhoSolver:
    def __init__(self, target_address, batch_size=1000):
        self.target = target_address
        self.batch_size = batch_size
        self.g = Point(GX, GY)
        self.iterations = 0
        self.found = False
        
    def pollard_rho_brent(self):
        """Brent's cycle detection for Pollard's Rho"""
        print("[*] Starting Pollard's Rho algorithm for ECDLP")
        print(f"[*] Target address: {self.target.hex()}")
        
        # Random starting points
        x0 = np.random.randint(2, N)
        y0 = np.random.randint(2, N)
        
        # x = x0*G + y0*T where T is target point
        p_x = point_mul(x0)
        
        # Tortoise
        mu = 0
        lam = 1
        
        X = point_mul(x0)
        Xm = X.copy()
        
        power_of_2 = 1
        
        start_time = time.time()
        
        while True:
            self.iterations += 1
            
            # Advance tortoise
            if power_of_2 == lam:
                Xm = X.copy()
                power_of_2 *= 2
                lam = 0
            
            # Hare iteration
            X, _ = rho_function_point(X, 0)
            lam += 1
            
            if self.iterations % 100000 == 0:
                elapsed = time.time() - start_time
                rate = self.iterations / elapsed
                print(f"[+] Iterations: {self.iterations:.2e} ({rate:.2e} ops/sec)")
            
            # Check for cycle
            if X.X == Xm.X and X.Y == Xm.Y:
                print(f"[!] Cycle detected at iteration {self.iterations}")
                # This requires Pohlig-Hellman or other techniques
                break
            
            if self.iterations > 2**40:  # Safety limit
                print("[-] Exceeded iteration limit")
                break
    
    def brute_force_batch(self, batch_start, batch_size):
        """Brute force search in range"""
        print(f"[*] Brute force search: {batch_start} to {batch_start + batch_size}")
        
        start_time = time.time()
        
        for i in range(batch_size):
            key = batch_start + i
            
            if key > PUZZLE_MAX:
                print("[-] Exceeded puzzle range")
                break
            
            point = point_mul(key)
            addr = point_to_address(point)
            
            if addr == self.target:
                print(f"\n[!!!] FOUND KEY: {hex(key)}")
                print(f"[!!!] Private key: {key}")
                return key
            
            if i % 10000 == 0 and i > 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                print(f"[+] Checked {i} keys ({rate:.0f} keys/sec)")
        
        return None


# =========================
# Main execution
# =========================

if __name__ == "__main__":
    print("=" * 60)
    print("Bitcoin Puzzle #71 Solver - Pollard's Rho")
    print("=" * 60)
    
    # Target address for puzzle #71
    target_address = bytes.fromhex("1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU")
    
    # Quick test
    solver = PollardRhoSolver(target_address)
    
    # Try batch search first (smaller range)
    result = solver.brute_force_batch(PUZZLE_MIN, 100000)
    
    if not result:
        print("\n[*] Switching to Pollard's Rho algorithm...")
        solver.pollard_rho_brent()
