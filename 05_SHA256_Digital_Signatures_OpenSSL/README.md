# Practical 05: SHA-256 Hash Generation, Digital Signatures, and Verification using OpenSSL

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 05
- **Practical Problem Statement:** Generate SHA-256 hash values, create digital signatures, and verify their authenticity using OpenSSL.
- **Tool Required:** OpenSSL CLI (and Python automation script)
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Compute cryptographic **SHA-256 hash digests** of arbitrary transaction payloads.
2. Sign the hash digest using a sender's **RSA 2048-bit Private Key** to generate a verifiable digital signature.
3. Authenticate and verify the digital signature using the sender's **RSA Public Key**.
4. Perform a **Tamper Detection Test** by intentionally corrupting a single byte in the signed document to verify signature rejection.

---

## 🛠️ Tool Setup & Environment
- **Tool:** OpenSSL 3.x / 1.1.x
- **Digital Signature Workflow Architecture:**

```text
+------------------------------------------------------------------------+
|                     DIGITAL SIGNATURE & TAMPER TESTING                 |
|                                                                        |
|  [SIGNING PHASE - Alice's Private Key]                                 |
|  +--------------------+       +---------+       +-------------------+  |
|  | Transaction Data   | ----> | SHA-256 | ----> | 256-bit Digest    |  |
|  +--------------------+       +---------+       +-------------------+  |
|                                                           |            |
|                                                           v            |
|  +--------------------+                         +-------------------+  |
|  | Alice Private Key  | ----------------------> | RSA Encryption /  |  |
|  | (private_key.pem)  |                         | Digital Signature |  |
|  +--------------------+                         +-------------------+  |
|                                                           |            |
|                                                           v            |
|                                                 +-------------------+  |
|                                                 | signature.bin     |  |
|                                                 +-------------------+  |
|                                                                        |
|  [VERIFICATION PHASE - Bob with Alice's Public Key]                    |
|  +--------------------+       +---------+       +-------------------+  |
|  | Received Document  | ----> | SHA-256 | ----> | Hash Digest H_1   |  |
|  +--------------------+       +---------+       +-------------------+  |
|                                                           |            |
|  +--------------------+       +---------+                 | Compare    |
|  | signature.bin +    | ----> | RSA Pub | ----> | Hash Digest H_2   |  |
|  | Alice Public Key   |       | Decrypt |       +-------------------+  |
|  +--------------------+       +---------+                 |            |
|                                                           v            |
|                                            If H_1 == H_2: Verified OK! |
|                                            If H_1 != H_2: REJECTED!    |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. SHA-256 Cryptographic Hash
- Produces a deterministic, 256-bit (32-byte / 64-hex char) fixed-length digest.
- **Three Essential Security Properties:**
  1. **Preimage Resistance (One-Way):** Given $H$, it is computationally infeasible to find $M$ such that $	ext{SHA256}(M) = H$.
  2. **Second-Preimage Resistance (Weak Collision):** Given $M_1$, it is infeasible to find $M_2 
e M_1$ such that $	ext{SHA256}(M_1) = 	ext{SHA256}(M_2)$.
  3. **Collision Resistance (Strong Collision):** Infeasible to find any pair $(M_1, M_2)$ such that $	ext{SHA256}(M_1) = 	ext{SHA256}(M_2)$ ($2^{128}$ operations via Birthday Bound).

### 2. Digital Signatures with RSA
- **Signature Generation:**
  $$S = (	ext{SHA256}(M))^d \pmod n$$
- **Signature Verification:**
  $$H' = S^e \pmod n$$
  Verify that $H' \stackrel{?}{=} 	ext{SHA256}(M_{	ext{received}})$.
- **Security Guarantees:**
  - **Authenticity:** Only the holder of private key $d$ could have produced $S$.
  - **Integrity:** Any alteration of $M$ alters $	ext{SHA256}(M)$, failing verification.
  - **Non-Repudiation:** The sender cannot deny having generated the signature.

---

## 💻 Step-by-Step OpenSSL Commands & Procedure

1. **Generate RSA Signing Keypair:**
   ```bash
   openssl genpkey -algorithm RSA -out sender_private.pem -pkeyopt rsa_keygen_bits:2048
   openssl pkey -in sender_private.pem -pubout -out sender_public.pem
   ```

2. **Create Transaction Document:**
   ```bash
   echo "AUTHORIZE WIRE TRANSFER: AMOUNT=\$50,000 TO ACCOUNT: 987654321" > transaction.txt
   ```

3. **Compute SHA-256 Hash Digest:**
   ```bash
   openssl dgst -sha256 transaction.txt
   ```

4. **Sign Document with Sender's Private Key:**
   ```bash
   openssl dgst -sha256 -sign sender_private.pem -out signature.bin transaction.txt
   ```

5. **Verify Authentic Signature with Public Key:**
   ```bash
   openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt
   # Output: Verified OK
   ```

6. **Tamper Test (Modify 1 character in payload):**
   ```bash
   sed -i 's/\$50,000/\$90,000/g' transaction.txt
   openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt
   # Output: Verification Failure (TAMPER DETECTED)
   ```

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 PRACTICAL 05: OPENSSL SHA-256 HASHING & DIGITAL SIGNATURES
===========================================================================

[+] Generated RSA 2048-bit Signing Keypair.
[+] Created Target Document 'transaction.txt':
    'AUTHORIZE WIRE TRANSFER: AMOUNT=$50,000 TO ACCOUNT: 987654321'

[+] SHA-256 Hash:
    2e9471067a97782916605886a136d7923fbab1c9139e4fb955452377ba4b6099

[+] Digital Signature Created: 'signature.bin' (256 bytes)

[+] 1. Validating Authentic Signature:
    openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt
    >>> Output: Verified OK

[+] 2. Tampering Document (Altering $50,000 -> $90,000)...
    openssl dgst -sha256 -verify sender_public.pem -signature signature.bin transaction.txt
    >>> Output: Verification Failure

[SUCCESS] Digital Signature accurately guarantees Authenticity, Integrity, and Non-Repudiation!
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why do digital signature schemes sign the hash of a message rather than the raw message itself?**
   - **Answer:** Raw RSA encryption is computationally slow and limited to messages smaller than the key modulus ($< 256$ bytes for 2048-bit keys). Hashing compresses messages of arbitrary length into a fixed 256-bit digest, dramatically accelerating signing and eliminating algebraic homomorphism attacks.

2. **Q2: What is the difference between Message Authentication Codes (MACs) and Digital Signatures?**
   - **Answer:** A MAC (e.g., HMAC-SHA256) relies on a **symmetric shared secret**, meaning both sender and receiver can generate and verify the MAC (does not provide non-repudiation). Digital Signatures use **asymmetric keypairs**, providing non-repudiation because only the private key owner can sign.

3. **Q3: What attack occurs if a weak hash function with known collisions (like MD5 or SHA-1) is used for digital signatures?**
   - **Answer:** An attacker can find two different documents $M_1$ and $M_2$ yielding the identical hash $H(M_1) = H(M_2)$. The attacker gets the victim to sign innocent document $M_1$, then attaches the valid signature to malicious contract $M_2$ (Collision Attack).

4. **Q4: What is the difference between RSA-PKCS#1 v1.5 and RSA-PSS signature padding?**
   - **Answer:** RSA-PKCS#1 v1.5 uses deterministic padding which has theoretical vulnerabilities. RSA-PSS (Probabilistic Signature Scheme) incorporates random salt into the padding, providing provable security reducible to the hardness of RSA in the random oracle model.
