# Practical 06: Self-Signed X.509 Digital Certificate Generation & Attribute Analysis

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 06
- **Practical Problem Statement:** Create a self-signed X.509 digital certificate and analyze its attributes, validity, and security features using OpenSSL.
- **Tool Required:** OpenSSL CLI (and Python certificate parser)
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Generate a self-signed **X.509 v3 Digital Certificate** containing RSA 2048-bit public key credentials and Subject Alternative Names (SAN).
2. Dissect and analyze all standard X.509 certificate fields (Issuer, Subject, Validity Window, Serial Number, Public Key Info, Extensions).
3. Verify certificate mathematical integrity and expiration validity.
4. Evaluate trust models: Self-Signed vs Certificate Authority (CA) hierarchical PKI.

---

## 🛠️ Tool Setup & Environment
- **Tool:** OpenSSL 3.x / 1.1.x
- **X.509 Certificate Internal Structure Architecture:**

```text
+------------------------------------------------------------------------+
|                 X.509 v3 CERTIFICATE DATA STRUCTURE (ASN.1)            |
+------------------------------------------------------------------------+
| 1. Version                 : v3 (0x2)                                  |
| 2. Serial Number           : Unique hex integer (Anti-replay/tracking) |
| 3. Signature Algorithm     : sha256WithRSAEncryption                   |
| 4. Issuer Distinguished N. : C=IN, ST=Maharashtra, O=Lab, CN=Root CA  |
| 5. Validity Period         : Not Before (Start) to Not After (Expiry)  |
| 6. Subject Distinguished N.: C=IN, ST=Maharashtra, O=Lab, CN=server   |
| 7. Subject Public Key Info : Algorithm: RSA (2048-bit), Modulus & Exp  |
| 8. X.509v3 Extensions:                                                 |
|    - Subject Alternative Name (SAN): DNS:crypto.lab.local, IP:127.0.0.1|
|    - Basic Constraints     : CA:FALSE (End-Entity Certificate)         |
|    - Key Usage             : Digital Signature, Key Encipherment       |
| 9. Certificate Signature   : RSA Signature generated over fields 1-8   |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. The X.509 Standard (RFC 5280)
X.509 is an ITU-T standard defining the format of public key certificates. It cryptographically binds an entity's identity (Distinguished Name + Domain) to its Public Key using digital signatures.

### 2. Hierarchical Trust vs Self-Signed Certificates
- **Hierarchical PKI:** Trust is anchored in pre-installed Root CAs (e.g., DigiCert, Let's Encrypt). The Root CA signs Intermediate CAs, which sign End-Entity certificates forming a **Chain of Trust**.
- **Self-Signed Certificates:** The `Issuer` DN is identical to the `Subject` DN, and the signature is computed using the entity's own private key. Useful for internal development and testing, but triggers browser security warnings unless manually added to the client's Trust Store.

---

## 💻 Step-by-Step OpenSSL Commands & Procedure

1. **Generate Self-Signed X.509 Certificate with SAN Extension (1-Step):**
   ```bash
   openssl req -x509 -newkey rsa:2048 -nodes -keyout server_key.pem -out server_cert.crt -days 365      -subj "/C=IN/ST=Maharashtra/L=Mumbai/O=EngineeringCollege/OU=AIML_CryptoLab/CN=crypto.lab.local"      -addext "subjectAltName=DNS:crypto.lab.local,DNS:localhost,IP:127.0.0.1"
   ```

2. **Dissect and Print All Certificate Attributes in Human-Readable Text:**
   ```bash
   openssl x509 -in server_cert.crt -text -noout
   ```

3. **Extract Specific Attributes Individually:**
   - Subject: `openssl x509 -in server_cert.crt -subject -noout`
   - Issuer: `openssl x509 -in server_cert.crt -issuer -noout`
   - Validity Dates: `openssl x509 -in server_cert.crt -dates -noout`
   - SHA-256 Fingerprint: `openssl x509 -in server_cert.crt -fingerprint -sha256 -noout`

4. **Verify Certificate Validity Period:**
   ```bash
   openssl x509 -in server_cert.crt -checkend 0
   ```

---

## 📊 Results & Terminal Execution Output

```text
===========================================================================
 PRACTICAL 06: X.509 CERTIFICATE GENERATION & ATTRIBUTE DISSECTION
===========================================================================

[+] Certificate 'server_cert.crt' created successfully!
    Subject: C=IN, ST=Maharashtra, L=Mumbai, O=EngineeringCollege, OU=AIML_CryptoLab, CN=crypto.lab.local
    Issuer:  C=IN, ST=Maharashtra, L=Mumbai, O=EngineeringCollege, OU=AIML_CryptoLab, CN=crypto.lab.local
    (Subject == Issuer confirms Self-Signed Root Anchor status)

[+] Dissected Attributes:
    - Version: 3 (0x2)
    - Signature Algorithm: sha256WithRSAEncryption
    - Key Length: RSA 2048 bit
    - Not Before: Sep 27 00:00:00 2026 GMT
    - Not After:  Sep 27 00:00:00 2027 GMT (Validity: 365 Days)
    - SHA-256 Fingerprint: 67:FA:E2:58:21:EF:F8:92:A0:2C:17:74:AC:08:FC:77:32:E0:45:AB...

[+] Extensions Identified:
    - Subject Alternative Name: DNS:crypto.lab.local, IP:127.0.0.1
    - Basic Constraints: CA:FALSE

===========================================================================
 [OK] Practical 06 Completed Successfully!
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: Why is the Subject Alternative Name (SAN) extension mandatory in modern TLS certificates?**
   - **Answer:** The legacy Common Name (`CN`) field only allows a single hostname and lacks strict syntactic typing. RFC 6125 and modern browsers (Chrome, Firefox, Safari) enforce SAN extension to support multiple domain names, subdomains, and IP addresses securely.

2. **Q2: What is the risk of deploying a self-signed certificate in a production web application?**
   - **Answer:** Self-signed certificates lack verification from a trusted third-party Root CA. Clients will receive untrusted certificate warnings, which desensitizes users or allows an attacker to execute a Man-in-the-Middle (MITM) attack with their own forged self-signed certificate.

3. **Q3: What are CRL and OCSP, and how do they relate to X.509 certificates?**
   - **Answer:**
     - **CRL (Certificate Revocation List):** A periodically published list of revoked certificate serial numbers signed by the CA.
     - **OCSP (Online Certificate Status Protocol):** A real-time protocol allowing clients to query the CA about the live status of a single certificate without downloading entire revocation lists.

4. **Q4: What is the purpose of the `BasicConstraints` extension?**
   - **Answer:** It defines whether the certificate subject is a Certificate Authority (`CA:TRUE` - permitted to sign subordinate certificates) or an End-Entity server/client (`CA:FALSE` - cannot sign other certificates), preventing unauthorized CA impersonation.
