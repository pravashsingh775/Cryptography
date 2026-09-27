# Practical 08: Develop an Application to Secure Text Messages using AES Encryption and SHA-256 Hashing (VS Code)

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 08
- **Practical Problem Statement:** Develop an application to secure text messages using AES encryption and SHA-256 hashing using VS Code.
- **Tool Required:** Visual Studio Code (Python 3.10+)
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO2

---

## 🎯 Objectives
1. Design an end-to-end secure messaging pipeline implementing **Authenticated Encryption with Associated Data (AEAD)** principles.
2. Encrypt confidential text messages using **AES-256 in CBC mode** with secure random 16-byte Initialization Vectors (IV) and PKCS#7 padding.
3. Guarantee message integrity and origin authentication using **HMAC-SHA256** (Encrypt-then-MAC paradigm).
4. Verify complete resilience against transmission tampering and bit-flipping attacks.

---

## 🛠️ Tool Setup & Environment
- **IDE:** Visual Studio Code
- **Language:** Python 3.10+ (`cryptography` library / `hashlib` / `hmac`)
- **Secure Messaging Architecture:**

```text
+------------------------------------------------------------------------+
|               AUTHENTICATED SECURE MESSAGING ARCHITECTURE              |
+------------------------------------------------------------------------+
|                                                                        |
|  [ALICE - SENDER]                                                      |
|  Plaintext Message: "Mission Directive: Transfer operative at 0200"    |
|         |                                                              |
|         +---> [PKCS#7 Padding]                                         |
|         |                                                              |
|         +---> [AES-256-CBC Encrypt (Key_enc, Random IV)]               |
|                     |                                                  |
|                     v                                                  |
|               Ciphertext (C)                                           |
|                     |                                                  |
|         +-----------+                                                  |
|         v                                                              |
|  [HMAC-SHA256 Compute] (Key_mac, IV || Ciphertext)                     |
|         |                                                              |
|         v                                                              |
|     Tag (T)                                                            |
|                                                                        |
|  TRANSMISSION PAYLOAD: { IV (16B) || Ciphertext || HMAC Tag (32B) }    |
|                               |                                        |
|                               v                                        |
|  ====================== PUBLIC NETWORK ==============================  |
|                               |                                        |
|                               v                                        |
|  [BOB - RECEIVER]                                                      |
|  1. Extract IV, Ciphertext, and Received HMAC Tag                      |
|  2. Recompute Expected HMAC Tag over (IV || Ciphertext)                |
|  3. Constant-time Compare: hmac.compare_digest(Expected, Received)     |
|     - If Tag INVALID -> REJECT IMMEDIATELY (TAMPER DETECTED)           |
|     - If Tag VALID   -> Proceed to AES-256-CBC Decrypt + Strip Padding |
|  4. Recover Plaintext Message                                          |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. AES-256-CBC with PKCS#7 Padding
- **Cipher Block Chaining (CBC):** Each plaintext block is XORed with the previous ciphertext block before encryption:
  $$C_0 = E_K(P_0 \oplus 	ext{IV}), \quad C_i = E_K(P_i \oplus C_{i-1})$$
- **PKCS#7 Padding:** Appends $N$ bytes each with byte value $N$ so that total length is a multiple of 16 bytes.

### 2. Encrypt-then-MAC vs MAC-then-Encrypt
- **Encrypt-then-MAC (EtM):** MAC is calculated over the ciphertext. This guarantees cryptographic doom principle compliance: if an adversary tampers with the ciphertext, the MAC verification fails before ciphertext touches the decryption engine, completely preventing Padding Oracle attacks.

---

## 💻 Python Source Code & Function Structure

- `derive_keys(master_key)`: Uses SHA-256 to derive independent 256-bit Encryption and MAC keys.
- `encrypt_message(plaintext, master_key)`: Generates random IV, pads plaintext, encrypts via AES-256-CBC, and computes HMAC-SHA256 authentication tag.
- `decrypt_message(payload, master_key)`: Verifies HMAC tag in constant time; upon successful authentication, decrypts ciphertext and unpads plaintext.

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 PRACTICAL 08: AES-256 & SHA-256 SECURE MESSAGING IN VS CODE
===========================================================================

[+] Master Shared Key: 'TopSecretSharedKey2026'

[+] Sender (Alice) Transmitting Message:
    'Mission Directive: Transfer operative to safehouse Alpha at 0200 hrs.'

[+] Cryptographic Transformation:
    - Generated IV (16 Bytes): 7a91fc04e8d356ba1289cf01...
    - AES-256 Ciphertext (Base64): dfoSacAuXskT5pirUlfYi5kUCi0X/i436JltR05E...
    - HMAC-SHA256 Tag (Hex):       767e03fc9606e017291ec1775a6e1d007e203a136d9f4784...

[+] Receiver (Bob) Processing:
    [1] Verifying HMAC-SHA256 Authenticity Tag: VALID
    [2] AES-256 Decryption & Padding Validation: SUCCESS
    [3] Decrypted Message: 'Mission Directive: Transfer operative to safehouse Alpha at 0200 hrs.'

[+] Tamper Simulation (Flipping 1 byte in transit):
    [1] Verifying HMAC-SHA256 Authenticity Tag: INVALID / REJECTED!
    [!] Transmission Dropped. Decryption aborted to prevent padding attacks.

===========================================================================
 [OK] Practical 08 Completed Successfully!
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why must the IV (Initialization Vector) in CBC mode be unpredictable and cryptographically random?**
   - **Answer:** If predictable IVs are used, an attacker can launch chosen-plaintext attacks (e.g., BEAST attack against SSL/TLS) by predicting the IV of the next block and cancelling out known bytes.

2. **Q2: Why should encryption keys and MAC keys always be separate?**
   - **Answer:** Using the same key for both encryption and MAC calculation violates cryptographic separation of duties and can create cross-protocol interactions and key leakage vulnerabilities.

3. **Q3: What is the purpose of `hmac.compare_digest` instead of standard `==`?**
   - **Answer:** Standard equality `==` short-circuits on the first mismatched byte, leaking timing information that allows an attacker to reconstruct the valid MAC byte-by-byte via a **Timing Attack**. `compare_digest` runs in constant time.
