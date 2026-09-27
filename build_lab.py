"""
Builder script to generate full, beautiful, production-grade practical files for Cryptography Lab.
"""

import os

BASE_DIR = r"c:\Users\PRAVASH\Desktop\Cryptography"

# -------------------------------------------------------------------------------------------------
# PRACTICAL DATA DEFINITIONS
# -------------------------------------------------------------------------------------------------

PRACTICALS = {
    "01_Classical_Ciphers_CrypTool": {
        "readme": """# Practical 01: Implementation of Caesar, Vigenère, and Rail Fence Ciphers

## 📌 Practical Overview
- **Practical No:** 01
- **Practical Statement:** Implement Caesar, Vigenère, and Rail Fence ciphers and compare their encryption and decryption processes.
- **Tool Required:** CrypTool 1 / CrypTool 2 & Python
- **Course Outcome (CO):** CO1
- **Bloom's Level (BL):** BL3 (Apply)

---

## 🎯 Objectives
1. Understand the working mechanism of Classical Substitution and Transposition Ciphers.
2. Execute Caesar Cipher (Monoalphabetic Substitution), Vigenère Cipher (Polyalphabetic Substitution), and Rail Fence Cipher (Transposition) using **CrypTool**.
3. Compare encryption complexity, key size, and resistance against brute-force cryptanalysis.

---

## 📖 Theoretical Background

### 1. Caesar Cipher (Monoalphabetic Substitution)
- **Concept:** Replaces each character in the plaintext by shifting it $k$ positions down the alphabet.
- **Encryption Equation:**
  $$C = E(P, k) = (P + k) \\pmod{26}$$
- **Decryption Equation:**
  $$P = D(C, k) = (C - k + 26) \\pmod{26}$$
- **Key Space:** $25$ possible keys. Highly vulnerable to brute-force search and single-letter frequency analysis.

### 2. Vigenère Cipher (Polyalphabetic Substitution)
- **Concept:** Employs a repeating keyword to shift plaintext characters by varying amounts based on the key sequence.
- **Encryption Equation:**
  $$C_i = E(P_i, K_i) = (P_i + K_{i \\pmod m}) \\pmod{26}$$
- **Decryption Equation:**
  $$P_i = D(C_i, K_i) = (C_i - K_{i \\pmod m} + 26) \\pmod{26}$$
- **Key Space:** $26^m$. Significantly masks single-character frequencies; however, vulnerable to Kasiski examination and Friedman test (Index of Coincidence).

### 3. Rail Fence Cipher (Transposition)
- **Concept:** Writes plaintext in a zigzag pattern across $d$ depth levels and reads off row by row.
- **Key Space:** $N-1$ where $N$ is message length. Preserves character frequencies identically to plaintext.

---

## 💻 Step-by-Step Procedure in CrypTool
1. Open **CrypTool 1**.
2. Click `File` -> `New` and enter: `CRYPTOGRAPHY AND NETWORK SECURITY`.
3. **Caesar:** `Crypt/Decrypt` -> `Symmetric (classic)` -> `Caesar / Rot-13...` -> Key: `3` -> `Encrypt`.
4. **Vigenère:** `Crypt/Decrypt` -> `Symmetric (classic)` -> `Vigenère...` -> Key: `SECRET` -> `Encrypt`.
5. **Rail Fence:** `Crypt/Decrypt` -> `Symmetric (classic)` -> `Scytale / Rail Fence...` -> Depth: `3` -> `Encrypt`.

---

## 📊 Comparison Matrix

| Parameter | Caesar Cipher | Vigenère Cipher | Rail Fence Cipher |
|:---|:---|:---|:---|
| **Cipher Type** | Monoalphabetic Substitution | Polyalphabetic Substitution | Transposition (Permutation) |
| **Key Type** | Single integer ($0 \\le k \\le 25$) | Keyword string of length $m$ | Integer depth ($2 \\le d \\le N$) |
| **Key Space Size** | 25 | $26^m$ | $\\approx N$ |
| **Letter Frequency** | Preserved (shifted) | Flattened / Smoothed | Perfectly preserved |
| **Primary Vulnerability**| Brute-Force (25 trials) | Kasiski Analysis, Babbage Attack | Anagramming & Bigram Analysis |

---

## ❓ Viva Questions & Answers
1. **Q:** Why is the Caesar cipher insecure?
   - **A:** It only has 25 possible keys, making exhaustive brute-force search trivial.
2. **Q:** How does Vigenère cipher defeat single-letter frequency analysis?
   - **A:** By rotating through multiple shift alphabets, a single letter like 'E' maps to different ciphertext characters.
3. **Q:** What is the difference between Substitution and Transposition?
   - **A:** Substitution changes the identity of characters; Transposition rearranges their positions without altering identity.
""",
        "code": {
            "classical_ciphers.py": """\"\"\"
Practical 01: Implementation of Caesar, Vigenère, and Rail Fence Ciphers
\"\"\"

def caesar_encrypt(plaintext: str, shift: int = 3) -> str:
    ciphertext = []
    print(f"\\n[*] Caesar Encryption Process (Shift = {shift}):")
    print(f"    Formula: C = (P + {shift}) mod 26")
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            ciphertext.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            ciphertext.append(char)
    res = "".join(ciphertext)
    print(f"    Plaintext:  '{plaintext}'")
    print(f"    Ciphertext: '{res}'")
    return res

def caesar_decrypt(ciphertext: str, shift: int = 3) -> str:
    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            plaintext.append(chr((ord(char) - base - shift + 26) % 26 + base))
        else:
            plaintext.append(char)
    res = "".join(plaintext)
    print(f"[*] Caesar Decrypted: '{res}'")
    return res

def vigenere_encrypt(plaintext: str, key: str = "SECRET") -> str:
    ciphertext = []
    key_upper = key.upper()
    key_len = len(key_upper)
    print(f"\\n[*] Vigenere Polyalphabetic Encryption (Key = '{key_upper}'):")
    print(f"    Formula: C_i = (P_i + K_i) mod 26")
    key_idx = 0
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base
            k_val = ord(key_upper[key_idx % key_len]) - ord('A')
            ciphertext.append(chr((p_val + k_val) % 26 + base))
            key_idx += 1
        else:
            ciphertext.append(char)
    res = "".join(ciphertext)
    print(f"    Plaintext:  '{plaintext}'")
    print(f"    Ciphertext: '{res}'")
    return res

def vigenere_decrypt(ciphertext: str, key: str = "SECRET") -> str:
    plaintext = []
    key_upper = key.upper()
    key_len = len(key_upper)
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c_val = ord(char) - base
            k_val = ord(key_upper[key_idx % key_len]) - ord('A')
            plaintext.append(chr((c_val - k_val + 26) % 26 + base))
            key_idx += 1
        else:
            plaintext.append(char)
    res = "".join(plaintext)
    print(f"[*] Vigenere Decrypted: '{res}'")
    return res

def rail_fence_encrypt(plaintext: str, rails: int = 3) -> str:
    clean_text = "".join(plaintext.split())
    print(f"\\n[*] Rail Fence Transposition Encryption (Rails/Depth = {rails}):")
    matrix = [["." for _ in range(len(clean_text))] for _ in range(rails)]
    row, direction = 0, 1
    for col, char in enumerate(clean_text):
        matrix[row][col] = char
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    for r in range(rails):
        print(f"    Rail {r+1}: " + " ".join(matrix[r]))
    ciphertext = [matrix[r][c] for r in range(rails) for c in range(len(clean_text)) if matrix[r][c] != "."]
    res = "".join(ciphertext)
    print(f"    Ciphertext: '{res}'")
    return res

def rail_fence_decrypt(ciphertext: str, rails: int = 3) -> str:
    matrix = [["." for _ in range(len(ciphertext))] for _ in range(rails)]
    row, direction = 0, 1
    for col in range(len(ciphertext)):
        matrix[row][col] = "*"
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    idx = 0
    for r in range(rails):
        for c in range(len(ciphertext)):
            if matrix[r][c] == "*" and idx < len(ciphertext):
                matrix[r][c] = ciphertext[idx]
                idx += 1
    plaintext = []
    row, direction = 0, 1
    for col in range(len(ciphertext)):
        plaintext.append(matrix[row][col])
        row += direction
        if row == 0 or row == rails - 1:
            direction = -direction
    res = "".join(plaintext)
    print(f"[*] Rail Fence Decrypted: '{res}'")
    return res

def main():
    print("=" * 75)
    print("      PRACTICAL 01: CAESAR, VIGENERE & RAIL FENCE CIPHER EXECUTION")
    print("=" * 75)
    sample_text = "CRYPTOGRAPHY AND NETWORK SECURITY"
    print(f"\\n[+] Input Plaintext Message: '{sample_text}'")
    
    c_cipher = caesar_encrypt(sample_text, shift=3)
    caesar_decrypt(c_cipher, shift=3)
    
    v_cipher = vigenere_encrypt(sample_text, key="SECRET")
    vigenere_decrypt(v_cipher, key="SECRET")
    
    rf_cipher = rail_fence_encrypt(sample_text, rails=3)
    rail_fence_decrypt(rf_cipher, rails=3)
    
    print("\\n" + "=" * 75)
    print(" [OK] Practical 01 Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "02_Frequency_Analysis_CrypTool": {
        "readme": """# Practical 02: Frequency Analysis on Classical Ciphers & Cryptanalysis Resistance

## 📌 Practical Overview
- **Practical No:** 02
- **Practical Statement:** Perform frequency analysis on classical ciphers and analyze their resistance to cryptanalysis.
- **Tool Required:** CrypTool 1 / CrypTool 2 & Python
- **Course Outcome (CO):** CO1
- **Bloom's Level (BL):** BL4 (Analyze)

---

## 🎯 Objectives
1. Perform statistical letter frequency analysis on English text, monoalphabetic substitution ciphers, and polyalphabetic ciphers.
2. Demonstrate that monoalphabetic ciphers retain the exact statistical distribution of natural language.
3. Observe how polyalphabetic ciphers flatten character histograms, resisting simple frequency substitution.

---

## 📖 Theoretical Background
- **English Letter Frequency:** 'E' (~12.7%), 'T' (~9.1%), 'A' (~8.2%), 'O' (~7.5%), 'I' (~7.0%), 'N' (~6.7%).
- **Index of Coincidence (IoC):** Probability that two randomly selected letters from ciphertext are identical.
  - English Plaintext: $IoC \\approx 0.0667$
  - Monoalphabetic (Caesar): $IoC \\approx 0.0667$ (Unchanged!)
  - Polyalphabetic (Vigenère): $IoC \\approx 0.0385 - 0.045$ (Flattened distribution)

---

## 💻 Step-by-Step Procedure in CrypTool
1. Open CrypTool and enter a long English paragraph.
2. Check Plaintext histogram: `Analysis` -> `Tools for Analysis` -> `Frequency Test...`.
3. Encrypt with Caesar (shift 11), re-open `Frequency Test` -> notice exact shape simply shifted.
4. Auto-break Caesar: `Analysis` -> `Symmetric (classic)` -> `Caesar...` -> `Decrypt (Ciphertext only)`.
5. Encrypt with Vigenère (Key: `CIPHER`) -> notice flat uniform distribution.

---

## ❓ Viva Questions & Answers
1. **Q:** What is Index of Coincidence (IoC)?
   - **A:** Measure of letter distribution roughness. High IoC (~0.067) indicates monoalphabetic cipher; low IoC (~0.038) indicates polyalphabetic cipher.
2. **Q:** How does a Kasiski attack work on Vigenère cipher?
   - **A:** It finds repeated ciphertext n-grams, measures the distances between occurrences, and computes the GCD of distances to discover keyword length.
""",
        "code": {
            "frequency_cryptanalysis.py": """\"\"\"
Practical 02: Frequency Analysis & Automated Cryptanalysis
\"\"\"

import collections
import string

ENGLISH_FREQ = {
    'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7,
    'F': 2.2, 'G': 2.0, 'H': 6.1, 'I': 7.0, 'J': 0.15,
    'K': 0.77,'L': 4.0, 'M': 2.4, 'N': 6.7, 'O': 7.5,
    'P': 1.9, 'Q': 0.095,'R': 6.0,'S': 6.3, 'T': 9.1,
    'U': 2.8, 'V': 0.98,'W': 2.4, 'X': 0.15,'Y': 2.0, 'Z': 0.074
}

def calculate_frequencies(text: str) -> dict:
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    if total == 0: return {c: 0.0 for c in string.ascii_uppercase}
    counts = collections.Counter(letters)
    return {c: (counts[c] / total) * 100.0 for c in string.ascii_uppercase}

def calculate_ioc(text: str) -> float:
    letters = [c.upper() for c in text if c.isalpha()]
    N = len(letters)
    if N <= 1: return 0.0
    counts = collections.Counter(letters)
    return sum(n * (n - 1) for n in counts.values()) / (N * (N - 1))

def chi_squared_score(text: str) -> float:
    letters = [c.upper() for c in text if c.isalpha()]
    N = len(letters)
    if N == 0: return float('inf')
    counts = collections.Counter(letters)
    chi2 = 0.0
    for char, exp_pct in ENGLISH_FREQ.items():
        exp = (exp_pct / 100.0) * N
        obs = counts.get(char, 0)
        chi2 += ((obs - exp) ** 2) / exp
    return chi2

def crack_caesar(ciphertext: str):
    best_shift, best_chi2, best_plain = 0, float('inf'), ""
    for shift in range(26):
        candidate = []
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                candidate.append(chr((ord(char) - base - shift + 26) % 26 + base))
            else:
                candidate.append(char)
        dec = "".join(candidate)
        score = chi_squared_score(dec)
        if score < best_chi2:
            best_chi2, best_shift, best_plain = score, shift, dec
    return best_shift, best_plain, best_chi2

def print_hist(freqs: dict, title: str):
    print(f"\\n--- {title} (Top 8 Letters) ---")
    for char, val in sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:8]:
        bar = "#" * int(val * 2)
        print(f"  {char}: {val:5.2f}% | {bar}")

def main():
    print("=" * 75)
    print(" PRACTICAL 02: FREQUENCY ANALYSIS & AUTOMATED CRYPTANALYSIS")
    print("=" * 75)
    sample = (
        "Cryptography is the practice and study of techniques for secure communication "
        "in the presence of adversarial third parties. Modern cryptography heavily relies "
        "on mathematical theory and computer science practice."
    )
    print(f"\\n[+] Sample Plaintext: '{sample[:80]}...'")
    print(f"    Plaintext IoC: {calculate_ioc(sample):.4f} (Expected English ~0.067)")
    print_hist(calculate_frequencies(sample), "Plaintext")

    # Caesar
    shift = 11
    caesar_text = "".join(chr((ord(c) - ord('A') + shift) % 26 + ord('A')) if c.isupper() else
                          chr((ord(c) - ord('a') + shift) % 26 + ord('a')) if c.islower() else c for c in sample)
    print(f"\\n[+] Caesar Ciphertext (Shift={shift}):")
    print(f"    Caesar IoC: {calculate_ioc(caesar_text):.4f} (Retains high monoalphabetic IoC)")
    print_hist(calculate_frequencies(caesar_text), "Caesar Shifted")
    
    rec_shift, rec_plain, score = crack_caesar(caesar_text)
    print(f"\\n[*] Auto-Cracking Caesar: Recovered Key = {rec_shift} (Chi2 = {score:.2f})")
    print(f"    Decrypted: '{rec_plain[:60]}...'")

    # Vigenere
    key = "CIPHER"
    vig = []
    k_idx = 0
    for c in sample:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            k_val = ord(key[k_idx % len(key)]) - ord('A')
            vig.append(chr((ord(c) - base + k_val) % 26 + base))
            k_idx += 1
        else:
            vig.append(c)
    vig_text = "".join(vig)
    print(f"\\n[+] Vigenère Ciphertext (Key='{key}'):")
    print(f"    Vigenère IoC: {calculate_ioc(vig_text):.4f} (Dropped IoC indicates flattened polyalphabetic)")
    print_hist(calculate_frequencies(vig_text), "Vigenère Smoothed")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "03_DES_vs_AES_CrypTool": {
        "readme": """# Practical 03: Performance & Security Comparison of DES and AES

## 📌 Practical Overview
- **Practical No:** 03
- **Practical Statement:** Compare DES and AES encryption by encrypting sample data and evaluating their security and performance.
- **Tool Required:** CrypTool 1 / CrypTool 2 & Python
- **Course Outcome (CO):** CO2
- **Bloom's Level (BL):** BL4 (Analyze)

---

## 🎯 Objectives
1. Compare Feistel Network (DES) with Substitution-Permutation Network (AES).
2. Measure Avalanche Effect (bit difference on 1-bit input change).
3. Evaluate execution throughput and modern cryptanalytic resistance.

---

## 📊 Comprehensive Comparison Table

| Metric | DES / TripleDES | AES-256 |
|:---|:---|:---|
| **Structure** | 16-round Feistel Network | Substitution-Permutation Network (SPN) |
| **Block Size** | 64 bits | 128 bits |
| **Key Size** | 56 bits (DES) / 168 bits (3DES) | 256 bits |
| **Avalanche Effect** | $\\approx 50\\%$ | $\\approx 50\\%$ |
| **Vulnerabilities** | Small key space, Sweet32 (64b collisions) | Immune to Sweet32, No practical attack |
| **Hardware Acceleration** | Poor | Standard Intel/AMD AES-NI |
| **NIST Status** | Deprecated | Global Standard (FIPS 197) |

---

## ❓ Viva Questions & Answers
1. **Q:** What is the Avalanche Effect?
   - **A:** Changing 1 bit of plaintext or key causes approximately 50% of ciphertext bits to flip.
2. **Q:** Why was DES replaced by AES instead of 3DES?
   - **A:** 3DES is computationally slow (48 Feistel rounds) and retains a 64-bit block size vulnerable to Sweet32 birthday collision attacks.
""",
        "code": {
            "des_vs_aes_benchmark.py": """\"\"\"
Practical 03: DES vs AES Performance & Avalanche Benchmark
\"\"\"

import time
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def bit_diff(b1: bytes, b2: bytes):
    diff = sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))
    total = len(b1) * 8
    return diff, total, (diff / total) * 100.0

def main():
    print("=" * 75)
    print(" PRACTICAL 03: DES VS AES PERFORMANCE & AVALANCHE BENCHMARK")
    print("=" * 75)
    
    # Avalanche Test
    p1 = b"Hello, World! 12"
    p2 = b"Hello, World! 13" # 1 bit flipped
    aes_k = os.urandom(32)
    iv = os.urandom(16)
    
    c1 = Cipher(algorithms.AES(aes_k), modes.CBC(iv), backend=default_backend()).encryptor().update(p1)
    c2 = Cipher(algorithms.AES(aes_k), modes.CBC(iv), backend=default_backend()).encryptor().update(p2)
    diff, total, pct = bit_diff(c1, c2)
    print(f"\\n[+] AES-256 Avalanche Effect: {diff}/{total} bits flipped ({pct:.2f}%) [Ideal ~50%]")
    
    # Speed Benchmark
    iterations = 5000
    data = os.urandom(1024)
    des_k = os.urandom(24)
    des_iv = os.urandom(8)
    
    t0 = time.perf_counter()
    for _ in range(iterations):
        Cipher(algorithms.AES(aes_k), modes.CBC(iv), backend=default_backend()).encryptor().update(data)
    aes_time = time.perf_counter() - t0
    
    t0 = time.perf_counter()
    for _ in range(iterations):
        Cipher(algorithms.TripleDES(des_k), modes.CBC(des_iv), backend=default_backend()).encryptor().update(data)
    des_time = time.perf_counter() - t0
    
    mb = (iterations * 1024) / (1024 * 1024)
    print(f"\\n[+] Speed Benchmark ({iterations} iterations = {mb:.1f} MB):")
    print(f"    AES-256 Throughput:   {mb / aes_time:8.2f} MB/s ({aes_time:.4f} s)")
    print(f"    TripleDES Throughput: {mb / des_time:8.2f} MB/s ({des_time:.4f} s)")
    print(f"    Speedup: AES is {des_time / aes_time:.2f}x faster than TripleDES in software.")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "04_RSA_Keys_File_Crypto_OpenSSL": {
        "readme": """# Practical 04: RSA Public/Private Key Generation & File Cryptography using OpenSSL

## 📌 Practical Overview
- **Practical No:** 04
- **Tool Required:** OpenSSL CLI
- **Course Outcome (CO):** CO3 (BL3 Apply)

---

## 💻 Step-by-Step OpenSSL Commands
1. Generate Private Key:
   ```bash
   openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
   ```
2. Extract Public Key:
   ```bash
   openssl rsa -pubout -in private_key.pem -out public_key.pem
   ```
3. Encrypt File (RSA-OAEP-SHA256):
   ```bash
   openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in plaintext.txt -out ciphertext.bin -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256
   ```
4. Decrypt File:
   ```bash
   openssl pkeyutl -decrypt -inkey private_key.pem -in ciphertext.bin -out decrypted.txt -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256
   ```

---

## ❓ Viva Questions & Answers
1. **Q:** Why is OAEP padding required for RSA?
   - **A:** Textbook RSA is deterministic. OAEP adds randomized entropy to prevent chosen-ciphertext and Bleichenbacher attacks.
2. **Q:** Can RSA encrypt arbitrary large files?
   - **A:** No, RSA payload is limited by key size (max 190 bytes for 2048-bit RSA-OAEP). Large files use hybrid encryption (AES key encrypted with RSA).
""",
        "code": {
            "run_openssl_rsa.py": """\"\"\"
Practical 04: OpenSSL RSA Keypair Generation & File Cryptography
\"\"\"
import subprocess, os, shutil

def get_openssl():
    if shutil.which("openssl"): return "openssl"
    p = r"C:\\Program Files\\Git\\usr\\bin\\openssl.exe"
    return p if os.path.exists(p) else "openssl"

def main():
    print("=" * 75)
    print(" PRACTICAL 04: OPENSSL RSA KEYPAIR GENERATION & FILE ENCRYPTION")
    print("=" * 75)
    openssl = get_openssl()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    subprocess.run([openssl, "genpkey", "-algorithm", "RSA", "-out", "private_key.pem", "-pkeyopt", "rsa_keygen_bits:2048"], check=True)
    subprocess.run([openssl, "rsa", "-pubout", "-in", "private_key.pem", "-out", "public_key.pem"], check=True)
    
    msg = "Confidential Payload: Engineering Cryptography OpenSSL Practical Verification."
    with open("plaintext.txt", "w") as f: f.write(msg)
    print(f"\\n[+] Plaintext: '{msg}'")
    
    subprocess.run([openssl, "pkeyutl", "-encrypt", "-pubin", "-inkey", "public_key.pem", "-in", "plaintext.txt", "-out", "ciphertext.bin", "-pkeyopt", "rsa_padding_mode:oaep", "-pkeyopt", "rsa_oaep_md:sha256"], check=True)
    print(f"[+] Encrypted: 'ciphertext.bin' ({os.path.getsize('ciphertext.bin')} bytes)")
    
    subprocess.run([openssl, "pkeyutl", "-decrypt", "-inkey", "private_key.pem", "-in", "ciphertext.bin", "-out", "decrypted.txt", "-pkeyopt", "rsa_padding_mode:oaep", "-pkeyopt", "rsa_oaep_md:sha256"], check=True)
    with open("decrypted.txt", "r") as f: dec = f.read()
    print(f"[+] Decrypted: '{dec}'")
    assert dec == msg
    print("\\n[SUCCESS] RSA Encryption & Decryption 100% Verified!")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "05_SHA256_Digital_Signatures_OpenSSL": {
        "readme": """# Practical 05: SHA-256 Hashing & Digital Signatures using OpenSSL

## 📌 Practical Overview
- **Practical No:** 05
- **Tool Required:** OpenSSL CLI
- **Course Outcome (CO):** CO4 (BL3 Apply)

---

## 💻 Step-by-Step OpenSSL Commands
1. Generate Signer Key:
   ```bash
   openssl genpkey -algorithm RSA -out signer_private.pem -pkeyopt rsa_keygen_bits:2048
   openssl rsa -pubout -in signer_private.pem -out signer_public.pem
   ```
2. Hash Document:
   ```bash
   openssl dgst -sha256 transaction.txt
   ```
3. Sign Document:
   ```bash
   openssl dgst -sha256 -sign signer_private.pem -out signature.bin transaction.txt
   ```
4. Verify Authentic Signature:
   ```bash
   openssl dgst -sha256 -verify signer_public.pem -signature signature.bin transaction.txt
   ```
   *Output:* `Verified OK`
""",
        "code": {
            "run_openssl_signatures.py": """\"\"\"
Practical 05: OpenSSL SHA-256 Digital Signatures & Verification
\"\"\"
import subprocess, os, shutil

def get_openssl():
    if shutil.which("openssl"): return "openssl"
    p = r"C:\\Program Files\\Git\\usr\\bin\\openssl.exe"
    return p if os.path.exists(p) else "openssl"

def main():
    print("=" * 75)
    print(" PRACTICAL 05: OPENSSL SHA-256 HASHING & DIGITAL SIGNATURES")
    print("=" * 75)
    openssl = get_openssl()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    subprocess.run([openssl, "genpkey", "-algorithm", "RSA", "-out", "signer_private.pem", "-pkeyopt", "rsa_keygen_bits:2048"], check=True)
    subprocess.run([openssl, "rsa", "-pubout", "-in", "signer_private.pem", "-out", "signer_public.pem"], check=True)
    
    msg = "Official Order: Transfer 10,000 USD to Account 88921"
    with open("transaction.txt", "w") as f: f.write(msg)
    
    res = subprocess.run([openssl, "dgst", "-sha256", "transaction.txt"], capture_output=True, text=True)
    print(f"\\n[+] SHA-256: {res.stdout.strip()}")
    
    subprocess.run([openssl, "dgst", "-sha256", "-sign", "signer_private.pem", "-out", "signature.bin", "transaction.txt"], check=True)
    print(f"[+] Digital Signature generated ({os.path.getsize('signature.bin')} bytes)")
    
    res_v = subprocess.run([openssl, "dgst", "-sha256", "-verify", "signer_public.pem", "-signature", "signature.bin", "transaction.txt"], capture_output=True, text=True)
    print(f"[+] Authentic Verification: {res_v.stdout.strip()}")
    
    with open("transaction_tampered.txt", "w") as f: f.write("Official Order: Transfer 90,000 USD to Account 88921")
    res_t = subprocess.run([openssl, "dgst", "-sha256", "-verify", "signer_public.pem", "-signature", "signature.bin", "transaction_tampered.txt"], capture_output=True, text=True)
    print(f"[+] Tamper Test Result: " + ("TAMPER DETECTED / REJECTED" if res_t.returncode != 0 else "FAILED"))
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "06_X509_Certificates_OpenSSL": {
        "readme": """# Practical 06: Create and Inspect Self-Signed X.509 Digital Certificates

## 📌 Practical Overview
- **Practical No:** 06
- **Tool Required:** OpenSSL CLI
- **Course Outcome (CO):** CO4 (BL4 Analyze)

---

## 💻 Step-by-Step OpenSSL Commands
1. Generate Self-Signed Certificate:
   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server_private.key -out server_cert.crt -subj "/C=IN/ST=MH/L=Mumbai/O=College/CN=crypto.lab.local"
   ```
2. Inspect Attributes:
   ```bash
   openssl x509 -in server_cert.crt -issuer -subject -dates -fingerprint -sha256 -noout
   ```
""",
        "code": {
            "run_openssl_x509.py": """\"\"\"
Practical 06: OpenSSL X.509 Certificate Generation & Inspection
\"\"\"
import subprocess, os, shutil

def get_openssl():
    if shutil.which("openssl"): return "openssl"
    p = r"C:\\Program Files\\Git\\usr\\bin\\openssl.exe"
    return p if os.path.exists(p) else "openssl"

def main():
    print("=" * 75)
    print(" PRACTICAL 06: X.509 CERTIFICATE GENERATION & ATTRIBUTE DISSECTION")
    print("=" * 75)
    openssl = get_openssl()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    cmd = [
        openssl, "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048", "-keyout", "server_private.key", "-out", "server_cert.crt",
        "-subj", "/C=IN/ST=Maharashtra/L=Mumbai/O=EngineeringCollege/CN=crypto.lab.local",
        "-addext", "subjectAltName=DNS:crypto.lab.local,IP:127.0.0.1"
    ]
    subprocess.run(cmd, check=True)
    print("\\n[+] Certificate 'server_cert.crt' created successfully!")
    
    res = subprocess.run([openssl, "x509", "-in", "server_cert.crt", "-issuer", "-subject", "-dates", "-fingerprint", "-sha256", "-noout"], capture_output=True, text=True)
    for line in res.stdout.strip().splitlines():
        print(f"    {line}")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "07_RSA_and_Diffie_Hellman_Python": {
        "readme": """# Practical 07: RSA and Diffie-Hellman Key Exchange in Python

## 📌 Practical Overview
- **Practical No:** 07
- **Tool Required:** VS Code (Python 3.x)
- **Course Outcome (CO):** CO3 (BL3 Apply)

---

## 📖 Theoretical Background
- **RSA:** $C = M^e \\pmod n, M = C^d \\pmod n$ where $d \\equiv e^{-1} \\pmod{\\phi(n)}$.
- **Diffie-Hellman:** $A = g^a \\pmod p, B = g^b \\pmod p \\Rightarrow K = B^a = A^b = g^{ab} \\pmod p$.
""",
        "code": {
            "rsa_and_diffie_hellman.py": """\"\"\"
Practical 07: RSA and Diffie-Hellman Key Exchange Implementation
\"\"\"
import math, random

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    return gcd, y1 - (b // a) * x1, x1

def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1: raise ValueError("No mod inverse")
    return (x % phi + phi) % phi

def is_prime(n, k=5):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def gen_prime(bits=14):
    while True:
        p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p): return p

def main():
    print("=" * 75)
    print(" PRACTICAL 07: RSA & DIFFIE-HELLMAN KEY EXCHANGE")
    print("=" * 75)
    
    # RSA
    p, q = gen_prime(14), gen_prime(14)
    while p == q: q = gen_prime(14)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537 if math.gcd(65537, phi) == 1 else 3
    d = mod_inverse(e, phi)
    
    msg = "CONFIDENTIAL_KEY_2026"
    ct = [pow(ord(c), e, n) for c in msg]
    dec = "".join(chr(pow(x, d, n)) for x in ct)
    print(f"[+] RSA Modulus n: {n}, Public Key: ({e}, {n}), Private Key: ({d}, {n})")
    print(f"    Plaintext:  '{msg}'")
    print(f"    Ciphertext: {ct[:6]}...")
    print(f"    Decrypted:  '{dec}' (Verified: {dec == msg})")
    
    # Diffie-Hellman
    p_dh, g_dh = 104729, 2
    a, b = random.randint(2, p_dh-2), random.randint(2, p_dh-2)
    A, B = pow(g_dh, a, p_dh), pow(g_dh, b, p_dh)
    ka, kb = pow(B, a, p_dh), pow(A, b, p_dh)
    print(f"\\n[+] Diffie-Hellman Shared Secret Agreement:")
    print(f"    Alice Secret: {ka} | Bob Secret: {kb} | Match: {ka == kb}")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "08_AES_and_SHA256_Messaging_Python": {
        "readme": """# Practical 08: AES Encryption and SHA-256 Hashing for Secure Messaging

## 📌 Practical Overview
- **Practical No:** 08
- **Tool Required:** VS Code (Python 3.x)
- **Course Outcome (CO):** CO2 (BL3 Apply)
""",
        "code": {
            "secure_messaging.py": """\"\"\"
Practical 08: AES-256-CBC and SHA-256 / HMAC Secure Messaging
\"\"\"
import os, hashlib, hmac, base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def main():
    print("=" * 75)
    print(" PRACTICAL 08: AES-256 & SHA-256 SECURE MESSAGING")
    print("=" * 75)
    aes_k = os.urandom(32)
    hmac_k = os.urandom(32)
    iv = os.urandom(16)
    
    msg = "Mission Directive: Transfer operative to safehouse Alpha at 0200 hrs."
    print(f"\\n[+] Alice Sends: '{msg}'")
    
    padder = padding.PKCS7(128).padder()
    padded = padder.update(msg.encode()) + padder.finalize()
    ct = Cipher(algorithms.AES(aes_k), modes.CBC(iv), backend=default_backend()).encryptor().update(padded)
    mac = hmac.new(hmac_k, iv + ct, hashlib.sha256).hexdigest()
    
    print(f"[+] Ciphertext (Base64): {base64.b64encode(ct).decode()[:40]}...")
    print(f"[+] HMAC-SHA256 Tag:    {mac}")
    
    # Decrypt & Verify
    assert hmac.compare_digest(hmac.new(hmac_k, iv + ct, hashlib.sha256).hexdigest(), mac)
    unpadder = padding.PKCS7(128).unpadder()
    dec = unpadder.update(Cipher(algorithms.AES(aes_k), modes.CBC(iv), backend=default_backend()).decryptor().update(ct)) + unpadder.finalize()
    print(f"[+] Bob Decrypted: '{dec.decode()}'")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "09_Password_Hashing_Salting_Python": {
        "readme": """# Practical 09: Password Hashing with and without Salting & Attack Resistance

## 📌 Practical Overview
- **Practical No:** 09
- **Tool Required:** VS Code (Python 3.x)
- **Course Outcome (CO):** CO5 (BL4 Analyze)
""",
        "code": {
            "password_hashing_attacks.py": """\"\"\"
Practical 09: Salted vs Unsalted Password Hashing & Attack Simulation
\"\"\"
import hashlib, os, time, secrets

USERS = [("alice", "dragon123"), ("bob", "dragon123"), ("charlie", "admin123")]
WORDS = ["password", "123456", "dragon123", "admin123"]

def main():
    print("=" * 75)
    print(" PRACTICAL 09: PASSWORD HASHING, SALTING & ATTACK EVALUATION")
    print("=" * 75)
    
    unsalted = {u: hashlib.sha256(p.encode()).hexdigest() for u, p in USERS}
    salted = {u: (secrets.token_bytes(16), hashlib.pbkdf2_hmac('sha256', p.encode(), secrets.token_bytes(16), 100000)) for u, p in USERS}
    
    print(f"\\n[+] Unsalted (Notice Alice and Bob have SAME hash):")
    for u, h in unsalted.items(): print(f"    {u:<10}: {h[:20]}...")
    
    # Crack Unsalted
    t0 = time.perf_counter()
    lookup = {hashlib.sha256(w.encode()).hexdigest(): w for w in WORDS}
    cracked_u = {u: lookup[h] for u, h in unsalted.items() if h in lookup}
    tu = time.perf_counter() - t0
    print(f"\\n[+] Unsalted Attack: Cracked in {tu * 1000:.4f} ms -> {cracked_u}")
    
    # Crack Salted
    t0 = time.perf_counter()
    cracked_s = {}
    for u, (s, h) in salted.items():
        for w in WORDS:
            if hashlib.pbkdf2_hmac('sha256', w.encode(), s, 100000) == h:
                cracked_s[u] = w
                break
    ts = time.perf_counter() - t0
    print(f"[+] Salted Attack:   Cracked in {ts:.4f} s ({ts * 1000:.2f} ms)")
    print(f"\\n[SUCCESS] Salted PBKDF2 is {ts / tu:,.1f}x slower for attacker!")
    print("=" * 75)

if __name__ == "__main__":
    main()
"""
        }
    },

    "10_Wireshark_HTTPS_TLS_Handshake": {
        "readme": """# Practical 10: Capture HTTPS Traffic and Identify TLS Handshake, Certificates, and Cipher Suites

## 📌 Practical Overview
- **Practical No:** 10
- **Tool Required:** Wireshark
- **Course Outcome (CO):** CO4 (BL4 Analyze)

---

## 🔍 Wireshark Filters
- Filter TLS Handshake: `tls.handshake`
- Filter Client Hello: `tls.handshake.type == 1`
- Filter Server Hello: `tls.handshake.type == 2`
- Filter Certificate: `tls.handshake.type == 11`

---

## 📊 Observations
| Message | Key Fields Extracted |
|:---|:---|
| **Client Hello** | Supported Cipher Suites, SNI (`google.com`), Key Share (X25519) |
| **Server Hello** | Selected Cipher Suite (`TLS_AES_128_GCM_SHA256`), Server Key Share |
| **Application Data** | 100% Encrypted HTTP/2 or HTTP/3 payload |
"""
    },

    "11_Wireshark_VPN_vs_Unencrypted_Traffic": {
        "readme": """# Practical 11: Capture and Analyze Encrypted VPN Traffic vs Unencrypted Communication

## 📌 Practical Overview
- **Practical No:** 11
- **Tool Required:** Wireshark
- **Course Outcome (CO):** CO4 (BL4 Analyze)

---

## 🔍 Comparison
- **Unencrypted (`http || dns`):** Cleartext URLs, HTTP headers, plaintext passwords visible.
- **VPN (`openvpn || udp.port == 1194`):** Only Gateway IP and encrypted payload visible.
"""
    },

    "12_Wireshark_Secure_vs_Insecure_Protocols": {
        "readme": """# Practical 12: Network Packet Analysis to Identify Secure and Insecure Communication Protocols

## 📌 Practical Overview
- **Practical No:** 12
- **Tool Required:** Wireshark
- **Course Outcome (CO):** CO4 (BL4 Analyze)

---

## 📊 Protocol Security Audit Matrix
| Service | Insecure | Port | Secure | Port | Protection |
|:---|:---|:---:|:---|:---:|:---|
| Web | HTTP | 80 | HTTPS | 443 | TLS 1.3 Encryption |
| Shell | Telnet | 23 | SSH | 22 | Encrypted Diffie-Hellman Session |
| File | FTP | 21 | SFTP | 22 | SSH Tunnel Encapsulation |
"""
    },

    "13_Kali_John_The_Ripper": {
        "readme": """# Practical 13: Password Auditing using John the Ripper (Kali Linux)

## 📌 Practical Overview
- **Practical No:** 13
- **Tool Required:** Kali Linux
- **Course Outcome (CO):** CO5 (BL4 Analyze)

---

## 💻 Commands
```bash
sudo unshadow /etc/passwd /etc/shadow > hashes.txt
john --wordlist=/usr/share/wordlists/rockyou.txt --rules hashes.txt
john --show hashes.txt
```
""",
        "code": {
            "audit_demo.sh": """#!/bin/bash
echo "=== Practical 13: John the Ripper Audit ==="
john --wordlist=/usr/share/wordlists/rockyou.txt --rules sample_hashes.txt
john --show sample_hashes.txt
"""
        }
    },

    "14_Kali_SSH_Key_Authentication": {
        "readme": """# Practical 14: SSH Key Generation and Passwordless Authentication (Kali Linux)

## 📌 Practical Overview
- **Practical No:** 14
- **Tool Required:** Kali Linux / OpenSSH
- **Course Outcome (CO):** CO3 (BL3 Apply)

---

## 💻 Commands
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
ssh-copy-id user@remote_ip
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```
""",
        "code": {
            "setup_ssh_keys.sh": """#!/bin/bash
ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa
chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_rsa
"""
        }
    },

    "15_Kali_OpenVPN_Configuration": {
        "readme": """# Practical 15: Configure Secure VPN using OpenVPN (Kali Linux)

## 📌 Practical Overview
- **Practical No:** 15
- **Tool Required:** Kali Linux
- **Course Outcome (CO):** CO4 (BL3 Apply)
""",
        "code": {
            "server.conf": """port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
cipher AES-256-GCM
auth SHA256
"""
        }
    },

    "16_PacketTracer_WPA2_AES_Wireless": {
        "readme": """# Practical 16: Securing Wireless Network with WPA2-AES in Cisco Packet Tracer

## 📌 Practical Overview
- **Practical No:** 16
- **Tool Required:** Cisco Packet Tracer
- **Course Outcome (CO):** CO4 (BL3 Apply)

---

## 💻 Step-by-Step Topology Setup
1. Add `WRT300N` Wireless Router, `2960 Switch`, `Server-PT`, `Laptop-PT`, `Smartphone-PT`.
2. Router Wireless Config:
   - SSID: `Secure_Lab_WiFi`
   - Security: `WPA2-Personal`
   - Encryption: `AES (CCMP)`
   - Passphrase: `P@ssw0rdLab2026`
3. Laptop: Swap NIC to `WPC300N`, connect to `Secure_Lab_WiFi`.
4. Test: `ping 192.168.0.1` -> 0% packet loss.
"""
    }
}

# -------------------------------------------------------------------------------------------------
# WRITE ALL FILES
# -------------------------------------------------------------------------------------------------

for folder_name, contents in PRACTICALS.items():
    dir_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(dir_path, exist_ok=True)
    
    # Write README.md
    with open(os.path.join(dir_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(contents["readme"].strip() + "\n")
        
    # Write Code files
    if "code" in contents:
        for fname, code_str in contents["code"].items():
            with open(os.path.join(dir_path, fname), "w", encoding="utf-8") as f:
                f.write(code_str.strip() + "\n")

print("[OK] All 16 practical directories created and populated!")
