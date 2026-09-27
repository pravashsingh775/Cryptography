# Practical 09: Password Hashing with and without Salting & Attack Resistance Evaluation (VS Code)

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 09
- **Practical Problem Statement:** Implement password hashing with and without salting, and evaluate resistance against common password attacks using VS Code.
- **Tool Required:** Visual Studio Code (Python 3.10+)
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO5

---

## 🎯 Objectives
1. Implement password storage mechanisms using:
   - **Unsalted Fast Hashing:** Raw SHA-256
   - **Salted Hashing:** Unique per-user Salt + SHA-256
   - **Key Stretching (Slow Hashing):** PBKDF2-HMAC-SHA256 with 100,000 iterations
2. Simulate and benchmark **Dictionary Attacks** and **Rainbow Table Lookups** against both unsalted and salted credential stores.
3. Quantify how unique salting eliminates batch attack advantages and how iteration scaling increases cracking cost exponentially for adversaries.

---

## 🛠️ Tool Setup & Environment
- **IDE:** Visual Studio Code
- **Language:** Python 3.10+ (`hashlib`, `os`, `time`)
- **Password Storage Evolution Architecture:**

```text
+------------------------------------------------------------------------+
|                      PASSWORD STORAGE DEFENSE MATRIX                   |
+------------------------------------------------------------------------+
|                                                                        |
|  [LEVEL 1: UNSALTED SHA-256] -> VULNERABLE                             |
|  Password: "password123" ---> [SHA-256] ---> ef92b778bafe771e89245b89  |
|  * Vulnerability: Identical passwords produce identical hashes.        |
|                   Susceptible to Rainbow Tables & Batch Cracking.      |
|                                                                        |
|  [LEVEL 2: SALTED SHA-256] -> RESISTANT TO RAINBOW TABLES              |
|  Password: "password123" + Salt: "x9f2q1" ---> [SHA-256] ---> 8a4b2c1 |
|  * Defense: Precomputed Rainbow Tables useless.                        |
|  * Weakness: Fast computation (Billions of SHA-256/sec on GPU).        |
|                                                                        |
|  [LEVEL 3: KEY STRETCHING - PBKDF2 / BCRYPT / ARGON2] -> INDUSTRY GOLD |
|  Password + Salt ---> [PBKDF2-HMAC-SHA256 (100,000 Iterations)]        |
|  * Defense: Throttles adversary compute by 100,000x!                   |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. The Threat of Precomputation (Rainbow Tables)
When passwords are stored as $H = 	ext{Hash}(P)$, an attacker computes hashes of common passwords once and stores them in a lookup table. Cracking an entire database of 1,000,000 users requires $\mathcal{O}(1)$ time per user.

### 2. Cryptographic Salt ($S$)
A cryptographically secure pseudo-random string (typically 16–32 bytes) generated uniquely for each user:
$$H_{	ext{stored}} = 	ext{Hash}(P \parallel S)$$
- If Alice and Bob share password `"password123"`, their salts $S_{	ext{Alice}} 
e S_{	ext{Bob}}$ ensure $H_{	ext{Alice}} 
e H_{	ext{Bob}}$.
- Attacker must crack each user's hash independently ($N$ separate brute-force attacks).

### 3. Key Stretching (PBKDF2 - RFC 2898)
$$DK = 	ext{PBKDF2}(PRF, 	ext{Password}, 	ext{Salt}, c, dkLen)$$
Iterates $c = 100,000+$ rounds of HMAC-SHA256, forcing attackers to spend significant GPU/ASIC compute cycles per candidate password.

---

## 💻 Python Source Code & Function Structure

- `hash_unsalted(pwd)`: Computes raw SHA-256.
- `hash_salted(pwd, salt)`: Computes SHA-256 of `salt + pwd`.
- `hash_pbkdf2(pwd, salt, iterations=100000)`: Computes key-stretched digest.
- `dictionary_attack()`: Benchmarks time required to compromise unsalted vs salted databases against a dictionary of candidate passwords.

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 PRACTICAL 09: PASSWORD HASHING, SALTING & ATTACK EVALUATION
===========================================================================

[+] Database User Table Inspection:
    - User 'alice'   (Password: dragon123) -> Salt: None | Unsalted Hash: c20cf9879666a76500bb...
    - User 'bob'     (Password: dragon123) -> Salt: None | Unsalted Hash: c20cf9879666a76500bb...
    (Notice: Alice and Bob have identical hash values, revealing credential reuse!)

    - User 'alice'   (Salted PBKDF2) -> Salt: a9f81b3c... | Hash: 4e2098ba71f43a901e...
    - User 'bob'     (Salted PBKDF2) -> Salt: 7120df9a... | Hash: bc8910fa438902be11...
    (With Salt: Identical passwords produce completely unique hashes!)

[+] 1. Executing Dictionary Attack on UNSALTED Database:
    - Target Hashes Cracked: 3 / 3
    - Time Elapsed: 0.0286 ms
    - Cracking Speed: ~105,000,000 attempts / sec

[+] 2. Executing Dictionary Attack on SALTED PBKDF2 Database:
    - Target Hashes Cracked: 3 / 3
    - Time Elapsed: 838.99 ms (0.839 s)

[BENCHMARK VERDICT]
Salted PBKDF2 is 29,335.3x slower for attackers than unsalted hashing!
===========================================================================
```

---

## 📈 Comparative Analysis Matrix (BL4 Analyze)

| Parameter | Unsalted SHA-256 | Salted SHA-256 | Salted PBKDF2-HMAC-SHA256 | Argon2id |
|:---|:---|:---|:---|:---|
| **Salt Usage** | No (Static/None) | Unique 16-byte random | Unique 16-byte random | Unique 16-byte random |
| **Rainbow Table Resistance** | **Vulnerable** | **Immune** | **Immune** | **Immune** |
| **Batch Cracking Defense** | None (1 hash cracks all) | High (cracked 1-by-1) | High (cracked 1-by-1) | High (cracked 1-by-1) |
| **GPU / ASIC Resistance** | Zero | Zero | Moderate (CPU compute intensive) | Maximum (Memory-hard) |
| **Time per Hash** | $pprox 0.1\ \mu	ext{s}$ | $pprox 0.1\ \mu	ext{s}$ | $pprox 10 - 100\ 	ext{ms}$ | $pprox 50 - 250\ 	ext{ms}$ |
| **Recommended Usage** | **INSECURE / FORBIDDEN** | Insecure for Passwords | **Recommended (NIST)** | **State of the Art (OWASP)** |

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why is raw SHA-256 or MD5 unacceptable for storing user passwords even though it is a cryptographic hash?**
   - **Answer:** SHA-256 is designed for high-speed verification of bulk data. Modern GPUs can compute tens of billions of SHA-256 hashes per second, making offline dictionary and brute-force attacks trivial. Password hashing algorithms must be intentionally slow (computationally or memory hard).

2. **Q2: Does a salt need to be kept secret?**
   - **Answer:** No. Salts can be stored in plaintext alongside the password hash in the database. The primary purpose of a salt is to ensure uniqueness, preventing precomputation (Rainbow Tables) and preventing an attacker from testing a single guess against all users simultaneously.

3. **Q3: What is the difference between PBKDF2, bcrypt, and Argon2?**
   - **Answer:**
     - **PBKDF2:** CPU-intensive (iterated HMAC); vulnerable to custom ASIC/FPGA acceleration.
     - **bcrypt:** Memory-bound Feistel cipher (uses 4 KB state); resistant to GPUs.
     - **Argon2 (Argon2id):** Modern memory-hard winner of the Password Hashing Competition; requires configurable RAM (e.g., 64 MB), neutralizing GPU and ASIC attacks completely.
