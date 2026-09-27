# Practical 04: RSA Public & Private Keypair Generation & File Encryption using OpenSSL

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 04
- **Practical Problem Statement:** Generate RSA public and private key pairs and perform secure file encryption and decryption using OpenSSL.
- **Tool Required:** OpenSSL CLI (and Python automation script)
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO3

---

## 🎯 Objectives
1. Generate an industrial-grade **RSA 2048-bit Private Key** and extract the corresponding **Public Key** using OpenSSL.
2. Encrypt a confidential payload file using the recipient's RSA Public Key with **OAEP (Optimal Asymmetric Encryption Padding)**.
3. Decrypt the ciphertext file using the matching RSA Private Key and verify payload integrity via SHA-256 checksum comparison.
4. Understand hybrid encryption architectures and padding security against Bleichenbacher attacks.

---

## 🛠️ Tool Setup & Environment
- **Tool:** OpenSSL 3.x / 1.1.x
- **OpenSSL RSA Architecture:**

```text
+------------------------------------------------------------------------+
|                      OPENSSL ASYMMETRIC ENCRYPTION                     |
|                                                                        |
|  [Step 1: Key Generation]                                              |
|  openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
|                                                                        |
|  [Step 2: Public Key Extraction]                                       |
|  openssl pkey -in private_key.pem -pubout -out public_key.pem          |
|                                                                        |
|  [Step 3: RSA-OAEP Encryption]                                         |
|  +--------------------+    +------------------+    +-----------------+ |
|  | Plaintext File     | -> | public_key.pem   | -> | ciphertext.bin  | |
|  | (plaintext.txt)    |    | (RSA Public Key) |    | (256 bytes)     | |
|  +--------------------+    +------------------+    +-----------------+ |
|                                                              |         |
|  [Step 4: RSA Decryption]                                    v         |
|  +--------------------+    +------------------+    +-----------------+ |
|  | Decrypted File     | <- | private_key.pem  | <- | ciphertext.bin  | |
|  | (decrypted.txt)    |    | (RSA Private Key)|    | (256 bytes)     | |
|  +--------------------+    +------------------+    +-----------------+ |
|                                                                        |
|  [Step 5: Integrity Verification]                                      |
|  sha256sum plaintext.txt == sha256sum decrypted.txt                    |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. RSA Mathematical Algorithm
- **Key Generation:**
  1. Select two distinct large prime numbers $p$ and $q$.
  2. Compute modulus $n = p 	imes q$.
  3. Compute Euler's Totient $\phi(n) = (p - 1)(q - 1)$.
  4. Choose public exponent $e$ such that $1 < e < \phi(n)$ and $\gcd(e, \phi(n)) = 1$ (Standard: $e = 65537 = 2^{16} + 1$).
  5. Compute private exponent $d \equiv e^{-1} \pmod{\phi(n)}$ using Extended Euclidean Algorithm ($e \cdot d \equiv 1 \pmod{\phi(n)}$).
- **Public Key:** $(e, n)$
- **Private Key:** $(d, n)$
- **Encryption:** $C = M^e \pmod n$
- **Decryption:** $M = C^d \pmod n$

### 2. OAEP (Optimal Asymmetric Encryption Padding)
- Textbook RSA is deterministic: encrypting the same message with the same key yields identical ciphertext.
- **RSA-OAEP** adds randomized padding and Feistel masking to ensure **IND-CCA2 security** (Indistinguishability under Chosen-Ciphertext Attack), preventing Bleichenbacher padding oracle attacks.

---

## 💻 Step-by-Step OpenSSL Commands & Procedure

1. **Generate 2048-bit RSA Private Key:**
   ```bash
   openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
   ```

2. **Extract RSA Public Key from Private Key:**
   ```bash
   openssl pkey -in private_key.pem -pubout -out public_key.pem
   ```

3. **Inspect Key Parameters (Modulus, Exponents, Primes):**
   ```bash
   openssl pkey -in private_key.pem -text -noout
   ```

4. **Create Sample Plaintext File:**
   ```bash
   echo "Confidential Payload: Engineering Cryptography OpenSSL Practical Verification." > plaintext.txt
   ```

5. **Encrypt File using Public Key with OAEP Padding:**
   ```bash
   openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in plaintext.txt -out ciphertext.bin -pkeyopt rsa_padding_mode:oaep
   ```

6. **Decrypt File using Private Key:**
   ```bash
   openssl pkeyutl -decrypt -inkey private_key.pem -in ciphertext.bin -out decrypted.txt -pkeyopt rsa_padding_mode:oaep
   ```

7. **Verify Cryptographic File Integrity:**
   ```bash
   diff -s plaintext.txt decrypted.txt
   ```

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 PRACTICAL 04: OPENSSL RSA KEYPAIR GENERATION & FILE ENCRYPTION
===========================================================================

[+] Generating 2048-bit RSA Private Key (private_key.pem)...
[+] Extracting RSA Public Key (public_key.pem)...

[+] Input Plaintext:
    'Confidential Payload: Engineering Cryptography OpenSSL Practical Verification.'
    SHA-256 Hash: e7f05256e2993510e14a27546fa01b52a41d9a2ba1fcde6db36d078b6be80251

[+] Encrypted File: 'ciphertext.bin'
    Modulus Size: 2048 bits -> Ciphertext Size: 256 bytes

[+] Decrypted File: 'decrypted.txt'
    Decrypted Content: 'Confidential Payload: Engineering Cryptography OpenSSL Practical Verification.'
    SHA-256 Hash:     e7f05256e2993510e14a27546fa01b52a41d9a2ba1fcde6db36d078b6be80251

[SUCCESS] RSA Encryption & Decryption 100% Verified! SHA-256 Hashes Match.
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why is $e = 65537$ universally chosen as the public exponent in RSA?**
   - **Answer:** $65537$ ($F_4 = 2^{16} + 1$) is a Fermat prime with only two set bits (`0x10001`). This allows modular exponentiation $M^e \pmod n$ to execute in just 17 multiplications using square-and-multiply, while being large enough to resist low-exponent Coppersmith attacks (unlike $e=3$).

2. **Q2: What is the maximum data size that can be directly encrypted using a 2048-bit RSA key with OAEP padding?**
   - **Answer:** A 2048-bit RSA modulus is 256 bytes. Using OAEP with SHA-256 padding consumes $2 	imes hLen + 2 = 2(32) + 2 = 66$ bytes of overhead. Thus, the maximum plaintext payload is $256 - 66 = 190$ bytes. Bulk data must use hybrid encryption (AES session key).

3. **Q3: What is the purpose of RSA-OAEP compared to raw (textbook) RSA?**
   - **Answer:** Raw RSA is deterministic and homomorphic ($E(M_1) \cdot E(M_2) \equiv E(M_1 \cdot M_2)$), making it vulnerable to chosen-ciphertext attacks. OAEP adds random masking and padding, ensuring semantic security (IND-CCA2).

4. **Q4: How does OpenSSL represent RSA keys on disk?**
   - **Answer:** OpenSSL encodes RSA keys using ASN.1 / DER binary representation wrapped inside Base64 PEM (Privacy Enhanced Mail) containers bounded by `-----BEGIN RSA PRIVATE KEY-----` or `-----BEGIN PUBLIC KEY-----`.
