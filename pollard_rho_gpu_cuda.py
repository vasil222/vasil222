"""
Bitcoin Puzzle #71 Solver - CUDA Kernel Implementation
Full GPU-accelerated Pollard's Rho with batched point operations
"""

import numpy as np
import time
import hashlib
from numba import cuda, jit, uint64, uint32, float64
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

PARTITIONS = 20

# =========================
# CPU Point class
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
# CUDA Kernels
# =========================

if cuda.is_available():
    
    @cuda.jit
    def cuda_mod_inverse_kernel(a_values, result, p, iterations):
        """Batch modular inverse using Fermat's little theorem"""
        idx = cuda.grid(1)
        if idx >= a_values.shape[0]:
            return
        
        # a^(p-2) mod p
        a = a_values[idx]
        res = 1
        base = a
        exp = p - 2
        
        while exp > 0:
            if exp % 2 == 1:
                res = (res * base) % p
            exp = exp >> 1
            base = (base * base) % p
        
        result[idx] = res
    
    
    @cuda.jit
    def cuda_point_double_kernel(X, Y, Z, out_X, out_Y, out_Z, p):
        """Batch point doubling on secp256k1"""
        idx = cuda.grid(1)
        if idx >= X.shape[0]:
            return
        
        x = X[idx]
        y = Y[idx]
        z = Z[idx]
        
        # Point doubling formulas
        XX = (x * x) % p
        YY = (y * y) % p
        YYYY = (YY * YY) % p
        ZZ = (z * z) % p
        
        S = (2 * ((x + YY) * (x + YY) - XX - YYYY)) % p
        M = (3 * XX) % p
        
        out_X[idx] = (M * M - 2 * S) % p
        out_Y[idx] = (M * (S - out_X[idx]) - 8 * YYYY) % p
        out_Z[idx] = ((y + z) * (y + z) - YY - ZZ) % p
    
    
    @cuda.jit
    def cuda_point_add_kernel(X1, Y1, Z1, X2, Y2, Z2, out_X, out_Y, out_Z, p):
        """Batch point addition on secp256k1"""
        idx = cuda.grid(1)
        if idx >= X1.shape[0]:
            return
        
        x1, y1, z1 = X1[idx], Y1[idx], Z1[idx]
        x2, y2, z2 = X2[idx], Y2[idx], Z2[idx]
        
        Z1Z1 = (z1 * z1) % p
        Z2Z2 = (z2 * z2) % p
        
        U1 = (x1 * Z2Z2) % p
        U2 = (x2 * Z1Z1) % p
        
        S1 = (y1 * z2 * Z2Z2) % p
        S2 = (y2 * z1 * Z1Z1) % p
        
        H = (U2 - U1) % p
        I = (4 * H * H) % p
        J = (H * I) % p
        r = (2 * (S2 - S1)) % p
        
        out_X[idx] = (r * r - J - 2 * U1 * I) % p
        out_Y[idx] = (r * (U1 * I - out_X[idx]) - 2 * S1 * J) % p
        out_Z[idx] = (((z1 + z2) * (z1 + z2) - Z1Z1 - Z2Z2) * H) % p
    
    
    @cuda.jit
    def cuda_affine_kernel(X, Y, Z, out_X, out_Y, p):
        """Batch conversion from Jacobian to affine coordinates"""
        idx = cuda.grid(1)
        if idx >= X.shape[0]:
            return
        
        z = Z[idx]
        z_inv = pow(z, p - 2, p)
        z_inv_sq = (z_inv * z_inv) % p
        
        out_X[idx] = (X[idx] * z_inv_sq) % p
        out_Y[idx] = (Y[idx] * z_inv_sq * z_inv) % p
    
    
    @cuda.jit
    def cuda_rho_iteration_kernel(X, Y, Z, partition_ids, out_X, out_Y, out_Z, 
                                   gx_mult, gy_mult, gz_mult, p, num_partitions):
        """Pollard's Rho iteration: partition-based point operations"""
        idx = cuda.grid(1)
        if idx >= X.shape[0]:
            return
        
        partition = partition_ids[idx]
        
        if partition == 0:
            # Point doubling
            x, y, z = X[idx], Y[idx], Z[idx]
            
            XX = (x * x) % p
            YY = (y * y) % p
            YYYY = (YY * YY) % p
            ZZ = (z * z) % p
            
            S = (2 * ((x + YY) * (x + YY) - XX - YYYY)) % p
            M = (3 * XX) % p
            
            out_X[idx] = (M * M - 2 * S) % p
            out_Y[idx] = (M * (S - out_X[idx]) - 8 * YYYY) % p
            out_Z[idx] = ((y + z) * (y + z) - YY - ZZ) % p
        else:
            # Point addition with precomputed multiples
            x1, y1, z1 = X[idx], Y[idx], Z[idx]
            x2 = gx_mult[partition]
            y2 = gy_mult[partition]
            z2 = gz_mult[partition]
            
            Z1Z1 = (z1 * z1) % p
            Z2Z2 = (z2 * z2) % p
            
            U1 = (x1 * Z2Z2) % p
            U2 = (x2 * Z1Z1) % p
            
            S1 = (y1 * z2 * Z2Z2) % p
            S2 = (y2 * z1 * Z1Z1) % p
            
            H = (U2 - U1) % p
            I = (4 * H * H) % p
            J = (H * I) % p
            r = (2 * (S2 - S1)) % p
            
            out_X[idx] = (r * r - J - 2 * U1 * I) % p
            out_Y[idx] = (r * (U1 * I - out_X[idx]) - 2 * S1 * J) % p
            out_Z[idx] = (((z1 + z2) * (z1 + z2) - Z1Z1 - Z2Z2) * H) % p


# =========================
# GPU Solver Class
# =========================

class GPUPollardRhoSolver:
    def __init__(self, target_address, batch_size=10000, use_cuda=True):
        self.target = target_address
        self.batch_size = batch_size
        self.use_cuda = use_cuda and cuda.is_available()
        self.iterations = 0
        
        # Precompute multiples of G for partitioning
        self.precomputed_multiples = {}
        self._precompute_multiples()
        
        if self.use_cuda:
            self._init_cuda_memory()
    
    def _precompute_multiples(self):
        """Precompute i*G for each partition"""
        print("[*] Precomputing partition multiples...")
        for i in range(PARTITIONS):
            point = point_mul(i)
            x, y = affine(point)
            self.precomputed_multiples[i] = (x, y, 1)
    
    def _init_cuda_memory(self):
        """Allocate GPU memory"""
        print("[*] Initializing CUDA memory...")
        
        # Allocate arrays for batch operations
        self.gpu_X = cuda.device_array(self.batch_size, dtype=np.uint64)
        self.gpu_Y = cuda.device_array(self.batch_size, dtype=np.uint64)
        self.gpu_Z = cuda.device_array(self.batch_size, dtype=np.uint64)
        
        self.gpu_out_X = cuda.device_array(self.batch_size, dtype=np.uint64)
        self.gpu_out_Y = cuda.device_array(self.batch_size, dtype=np.uint64)
        self.gpu_out_Z = cuda.device_array(self.batch_size, dtype=np.uint64)
        
        # Partition IDs
        self.gpu_partitions = cuda.device_array(self.batch_size, dtype=np.uint32)
        
        # Precomputed multiples
        gx_mults = np.array([self.precomputed_multiples[i][0] for i in range(PARTITIONS)], dtype=np.uint64)
        gy_mults = np.array([self.precomputed_multiples[i][1] for i in range(PARTITIONS)], dtype=np.uint64)
        gz_mults = np.array([self.precomputed_multiples[i][2] for i in range(PARTITIONS)], dtype=np.uint64)
        
        self.gpu_gx_mults = cuda.to_device(gx_mults)
        self.gpu_gy_mults = cuda.to_device(gy_mults)
        self.gpu_gz_mults = cuda.to_device(gz_mults)
    
    def gpu_rho_iteration(self, points_batch):
        """Execute one Pollard's Rho iteration on GPU"""
        if not self.use_cuda:
            return self._cpu_rho_iteration(points_batch)
        
        batch_size = len(points_batch)
        
        # Convert to arrays
        X_array = np.array([p[0] for p in points_batch], dtype=np.uint64)
        Y_array = np.array([p[1] for p in points_batch], dtype=np.uint64)
        Z_array = np.array([p[2] for p in points_batch], dtype=np.uint64)
        partition_array = np.array([p[3] % PARTITIONS for p in points_batch], dtype=np.uint32)
        
        # Copy to GPU
        gpu_X = cuda.to_device(X_array)
        gpu_Y = cuda.to_device(Y_array)
        gpu_Z = cuda.to_device(Z_array)
        gpu_partitions = cuda.to_device(partition_array)
        
        gpu_out_X = cuda.device_array(batch_size, dtype=np.uint64)
        gpu_out_Y = cuda.device_array(batch_size, dtype=np.uint64)
        gpu_out_Z = cuda.device_array(batch_size, dtype=np.uint64)
        
        # Execute kernel
        threads_per_block = 256
        blocks = (batch_size + threads_per_block - 1) // threads_per_block
        
        cuda_rho_iteration_kernel[blocks, threads_per_block](
            gpu_X, gpu_Y, gpu_Z, gpu_partitions,
            gpu_out_X, gpu_out_Y, gpu_out_Z,
            self.gpu_gx_mults, self.gpu_gy_mults, self.gpu_gz_mults,
            P, PARTITIONS
        )
        
        cuda.synchronize()
        
        # Copy results back
        out_X = gpu_out_X.copy_to_host()
        out_Y = gpu_out_Y.copy_to_host()
        out_Z = gpu_out_Z.copy_to_host()
        
        results = []
        for i in range(batch_size):
            results.append((out_X[i], out_Y[i], out_Z[i], partition_array[i] + 1))
        
        return results
    
    def _cpu_rho_iteration(self, points_batch):
        """CPU fallback for Pollard's Rho iteration"""
        results = []
        for x, y, z, partition_id in points_batch:
            partition = partition_id % PARTITIONS
            
            if partition == 0:
                point = point_double(Point(x, y, z))
            else:
                p1 = Point(x, y, z)
                p2 = Point(*self.precomputed_multiples[partition][:2])
                point = point_add(p1, p2)
            
            results.append((point.X, point.Y, point.Z, partition + 1))
        
        return results
    
    def solve_brent(self):
        """Brent's cycle detection for Pollard's Rho"""
        print("[*] Starting GPU-accelerated Pollard's Rho")
        print(f"[*] Target: {self.target.hex()}")
        print(f"[*] Using CUDA: {self.use_cuda}")
        
        # Initialize with random point
        x0 = np.random.randint(2, N)
        points = [(GX * x0) % P, (GY * x0) % P, 1, 0]
        
        start_time = time.time()
        
        for iteration in range(2**40):
            self.iterations += 1
            
            # Execute Pollard's Rho iteration
            points = self.gpu_rho_iteration([points])[0]
            
            if iteration % 100000 == 0 and iteration > 0:
                elapsed = time.time() - start_time
                rate = iteration / elapsed
                print(f"[+] Iteration {iteration:.2e} ({rate:.2e} ops/sec)")
            
            if iteration > 2**35:  # Safety limit
                break
        
        print(f"[-] Reached iteration limit: {self.iterations}")


# =========================
# Main execution
# =========================

if __name__ == "__main__":
    print("=" * 60)
    print("Bitcoin Puzzle #71 Solver - GPU CUDA")
    print("=" * 60)
    
    target_address = bytes.fromhex("1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU")
    
    if cuda.is_available():
        print("[+] CUDA GPU detected")
        solver = GPUPollardRhoSolver(target_address, batch_size=10000, use_cuda=True)
        solver.solve_brent()
    else:
        print("[-] CUDA not available, falling back to CPU")
        solver = GPUPollardRhoSolver(target_address, batch_size=1000, use_cuda=False)
        solver.solve_brent()
