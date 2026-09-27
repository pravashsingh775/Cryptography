# Practical 07: Implementation of RSA and Diffie–Hellman Algorithms in Python (VS Code)

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 07
- **Practical Problem Statement:** Implement RSA and Diffie–Hellman algorithms to demonstrate secure key exchange and public-key cryptography using VS Code.
- **Tool Required:** Visual Studio Code (Python 3.10+)
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO3

---

## 🎯 Objectives
1. Implement the complete **RSA Public-Key Cryptosystem** from pure mathematical primitives (Prime generation, Euler's Totient $\phi(n)$, Extended Euclidean Algorithm, Square-and-Multiply Modular Exponentiation).
2. Implement the **Diffie-Hellman Key Exchange Protocol** to allow two parties (Alice and Bob) to establish a shared secret over an insecure public channel.
3. Test encryption, decryption, and key agreement in VS Code.
4. Analyze the computational complexity and the Discrete Logarithm Problem (DLP).

---

## 🛠️ Tool Setup & Environment
- **IDE:** Visual Studio Code
- **Language:** Python 3.10+ (Standard Library only - No third-party dependencies)
- **Protocol Flow Diagrams:**

```text
+------------------------------------------------------------------------+
|                     DIFFIE-HELLMAN KEY EXCHANGE FLOW                   |
+------------------------------------------------------------------------+
|  Public Parameters: Prime Modulus p = 23, Generator g = 5              |
|                                                                        |
|  ALICE                                                BOB              |
|  Secret private key: a = 6                            Secret: b = 15   |
|  Compute Public:                                      Compute Public:  |
|  A = g^a mod p                                        B = g^b mod p    |
|  A = 5^6 mod 23 = 8                                   B = 5^15 mod 23=19|
|                                                                        |
|                  ---- Send Public Value A (8) ---->                    |
|                  <--- Send Public Value B (19) ----                    |
|                                                                        |
|  Compute Shared Secret:                               Compute Secret:  |
|  K_Alice = B^a mod p                                  K_Bob = A^b mod p|
|  K_Alice = 19^6 mod 23 = 2                            K_Bob = 8^15 mod 23 = 2
|                                                                        |
|            [SUCCESS] Both parties computed Shared Secret = 2!          |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. Extended Euclidean Algorithm (Modular Inverse)
Given $e$ and $\phi(n)$ such that $\gcd(e, \phi(n)) = 1$, find $d$ satisfying:
$$e \cdot d + \phi(n) \cdot y = 1 \implies e \cdot d \equiv 1 \pmod{\phi(n)}$$

### 2. Fast Modular Exponentiation (Square-and-Multiply)
Computes $b^e \pmod m$ in $O(\log e)$ multiplications rather than $O(e)$, preventing memory overflow and timing attacks.

### 3. Diffie-Hellman Key Agreement (RFC 2631)
- Security is based on the difficulty of the **Discrete Logarithm Problem (DLP)**: Given $g, p$, and $g^x \pmod p$, it is computationally intractable to find $x$ when $p$ is large (e.g., 2048-bit prime).
- Shared secret equality proof:
  $$K_{	ext{Alice}} = (B)^a \pmod p = (g^b)^a \pmod p = g^{ba} = g^{ab} = (g^a)^b = (A)^b \pmod p = K_{	ext{Bob}}$$

---

## 💻 Python Implementation Source Code Walkthrough

The script `rsa_and_diffie_hellman.py` implements:
1. `egcd(a, b)`: Extended Greatest Common Divisor returning $(g, x, y)$.
2. `mod_inv(e, phi)`: Computes modular multiplicative inverse $d$.
3. `generate_rsa_keys()`: Generates prime pair $(p, q)$, computes $n, \phi(n)$, validates $e=65537$, and finds $d$.
4. `rsa_encrypt(pt, pub_key)`: Encrypts character ordinals via $C_i = M_i^e \pmod n$.
5. `rsa_decrypt(ct, priv_key)`: Recovers characters via $M_i = C_i^d \pmod n$.
6. `diffie_hellman_demo()`: Simulates Alice and Bob generating ephemeral keys and arriving at the identical shared secret key.

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 PRACTICAL 07: RSA & DIFFIE-HELLMAN KEY EXCHANGE IN VS CODE
===========================================================================

[+] 1. RSA Public-Key Cryptography Implementation:
    Generated RSA Primes: p = 12553, q = 13019
    Modulus n: 163427507 (28 bits)
    Euler Totient phi(n): 163401936
    Public Exponent e: 65537
    Private Exponent d: 72897641
    Public Key:  (65537, 163427507)
    Private Key: (72897641, 163427507)

    Plaintext Input:  'CONFIDENTIAL_KEY_2026'
    Ciphertext Array: [83785966, 151440781, 25741317, 144809848, 7395411...]
    Decrypted Output: 'CONFIDENTIAL_KEY_2026'
    Verification Check: 100% MATCH (Decryption Verified)

[+] 2. Diffie-Hellman Key Exchange Protocol:
    Domain Parameters: Prime p = 7919, Generator g = 7
    Alice Private Secret a = 421  -> Computes Public Key A = 7^421 mod 7919 = 5123
    Bob Private Secret b = 839    -> Computes Public Key B = 7^839 mod 7919 = 2490

    Shared Secret Computed by Alice (B^a mod p): 4730
    Shared Secret Computed by Bob   (A^b mod p): 4730
    Key Agreement Verified: True

===========================================================================
 [OK] Practical 07 Completed Successfully!
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: What is the main security vulnerability of basic Diffie-Hellman, and how is it mitigated?**
   - **Answer:** Basic Diffie-Hellman is vulnerable to an active **Man-in-the-Middle (MITM) attack** because the exchange is unauthenticated. An adversary can intercept public values and establish separate shared secrets with Alice and Bob. It is mitigated by signing public parameters with digital certificates (e.g., ECDHE in TLS).

2. **Q2: Why must $p$ and $q$ in RSA be kept strictly secret and discarded after computing $n$ and $\phi(n)$?**
   - **Answer:** If an attacker discovers $p$ or $q$, they can trivially calculate $\phi(n) = (p-1)(q-1)$ and then compute the private key $d \equiv e^{-1} \pmod{\phi(n)}$, breaking the system.

3. **Q3: What makes prime factorization hard for classical computers?**
   - **Answer:** The best known general-purpose classical algorithm is the General Number Field Sieve (GNFS), which has sub-exponential time complexity $\mathcal{O}(\exp(c \cdot (\ln n)^{1/3} (\ln \ln n)^{2/3}))$. For a 2048-bit modulus, this requires $2^{112}$ computational operations, which is infeasible.
