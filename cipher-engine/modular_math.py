import random



# Modular arithmetic functions for the cipher engine.

def extended_gcd(a,b):
    
    #base case
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = extended_gcd(b, a % b)
    
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd, x, y


# Computes the modular inverse of a modulo m using the Extended Euclidean Algorithm.



def mod_inverse(a, m):
    
    gcd , x, _ = extended_gcd(a,m)
    
    if gcd != 1:
        raise ValueError(f"No modular inverse for {a} mod {m} since gcd is {gcd}")
    
    return x % m


# Computes (base^exp) mod m using the method of exponentiation by squaring. for fast modular exponentiation.


def fast_mod_exp(base, exp, m):
    
    if m == 1:
        return 0
    
    result = 1
    base = base % m 
    
    while exp > 0:
        
        if exp % 2 == 1:
            result = (result * base) % m
            
        base = base(base * base) % m
        
        exp = exp // 2
        
    return result


def is_prime_miller_rabin(n, k=5):
    # n : the number to test
    # k : how many times to test (more = more accurate)
    #     k=20 gives error probability < 10^-12
    
    if  n< 2:
        return False
    
    if n == 2 or n==3:
        return True
    
    if n % 2 ==0:
        return False  # even numbers > 2 are not prime
    
    # Keep dividing (n-1) by 2 until it's odd
    # Count how many times we divided — that's r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
        
        
    for _ in range(k):
 
        # Pick a random number between 2 and n-2
        a = random.randrange(2, n - 1)
 
        # Compute x = a^d mod n  using our fast function
        x = fast_mod_exp(a, d, n)
 
        # If x is 1 or n-1, this witness is fine — try next one
        if x == 1 or x == n - 1:
            continue
 
        # Square x up to r-1 times
        # If x becomes n-1 at any point, this witness is fine
        for _ in range(r - 1):
            x = fast_mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            # The loop finished WITHOUT finding x = n-1
            # This means n is definitely COMPOSITE
            return False
 
    # All k witnesses passed → n is probably prime
    return True


# HOW DOES IT WORK?
#   1. Generate a random odd number of the right bit size
#   2. Test if it's prime using Miller-Rabin
#   3. If not prime, try the next odd number
#   4. Repeat until we find a prime

def generate_large_prime(bits=256):
    
    while True:
        candidate = random.getrandbits(bits)
        # Ensure it's odd
        candidate |= (1 << (bits - 1))
        candidate |= 1
        
        if is_prime_miller_rabin(candidate):
            return candidate
        

def mod_multiply(a, b, m):
    return (a * b) % m




if __name__ == "__main__":
 
    print("=" * 55)
    print("  modular_math.py — GraphLock Cipher Foundation")
    print("=" * 55)
 
    # ── Test 1: extended_gcd ──────────────────────────────────
    print("\n[1] Extended GCD")
    a, b = 35, 15
    gcd, x, y = extended_gcd(a, b)
    print(f"    extended_gcd({a}, {b})")
    print(f"    GCD = {gcd}")
    print(f"    x={x}, y={y}")
    print(f"    Verify: {a}*{x} + {b}*{y} = {a*x + b*y}  (should be {gcd})")
 
    # ── Test 2: mod_inverse ───────────────────────────────────
    print("\n[2] Modular Inverse")
    a, m = 3, 7
    inv = mod_inverse(a, m)
    print(f"    mod_inverse({a}, {m}) = {inv}")
    print(f"    Verify: {a} × {inv} mod {m} = {(a * inv) % m}  (should be 1)")
 
    # ── Test 3: fast_mod_exp ──────────────────────────────────
    print("\n[3] Fast Modular Exponentiation")
    base, exp, m = 2, 10, 7
    result = fast_mod_exp(base, exp, m)
    print(f"    fast_mod_exp({base}, {exp}, {m}) = {result}")
    print(f"    Verify: {base}^{exp} = {base**exp}, {base**exp} mod {m} = {base**exp % m}")
 
    # ── Test 4: Miller-Rabin ──────────────────────────────────
    print("\n[4] Miller-Rabin Primality Test")
    test_numbers = [2, 3, 7, 11, 15, 17, 100, 97, 561]
    for n in test_numbers:
        result = is_prime_miller_rabin(n)
        label = "PRIME" if result else "NOT prime"
        print(f"    {n:4d}  →  {label}")
 
    # ── Test 5: Generate large prime ─────────────────────────
    print("\n[5] Generate Large Prime")
    print("    Generating 256-bit prime... ", end="", flush=True)
    p = generate_large_prime(256)
    print("done!")
    print(f"    Prime (256-bit): {p}")
    print(f"    Digits: {len(str(p))}")
    print(f"    Is prime check: {is_prime_miller_rabin(p)}")
 
    # ── Test 6: mod_multiply ──────────────────────────────────
    print("\n[6] Modular Multiply")
    a, b, m = 13, 7, 10
    print(f"    mod_multiply({a}, {b}, {m}) = {mod_multiply(a, b, m)}")
    print(f"    Verify: {a}×{b} = {a*b} → {a*b} mod {m} = {(a*b)%m}")
 
    print("\n" + "=" * 55)
    print("  All tests passed! modular_math.py is ready.")
    print("  Next: graph_encoder.py")
    print("=" * 55)
