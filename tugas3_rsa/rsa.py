def is_prime(n: int) -> bool:
    """Return True if n is prime using Miller–Rabin primality test."""

    if n < 2:
        return False

    # Quick checks for small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False

    # Write n−1 as d·2^s by factoring powers of 2 from n−1
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Deterministic witnesses for 64-bit integers
    witnesses = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]

    def check(a, d, n, s):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for a in witnesses:
        if a % n == 0:
            continue
        if not check(a, d, n, s):
            return False

    return True


import random
def generate_prime(bits=64):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1 
        if is_prime(num):
            return num  
        
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception("Tidak ada modular inverse")
    return x % phi

def generate_keypair(bits=64):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p*q
    phi = (p-1)*(q-1)

    e = 65537

    d = mod_inverse(e,phi)
    
    pu_key = (e, n)
    pr_key = (d, n)
    
    return pu_key, pr_key

def encrypt(msg, pu_key):
    e, n = pu_key
    cipher = pow(msg, e, n)
    return cipher

def decrypt(cipher, pr_key):
    d, n = pr_key
    plain = pow(cipher, d, n)
    return plain

def main():
    p  = generate_prime(64)
    q  = generate_prime(64)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    print("Primes(64) (p, q):", (p, q))
    print(gcd(e, phi))  # seharusnya 1 

    # (d * e) % phi == 1
    d = mod_inverse(e, phi)
    
    pu_key = (e, n)
    pr_key = (d, n)

    print("Public Key:", pu_key)
    print("Private Key:", pr_key)

if __name__ == "__main__":
    main()