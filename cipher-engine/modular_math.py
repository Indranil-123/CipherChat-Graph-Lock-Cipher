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

