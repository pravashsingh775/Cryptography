# Practical 10: Capture HTTPS Traffic and Analyze TLS Handshake, Certificates, and Cipher Suites

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 10
- **Practical Problem Statement:** Capture HTTPS network traffic using Wireshark and analyze the TLS handshake, digital certificates, and cipher suites.
- **Tool Required:** Wireshark Network Protocol Analyzer
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Capture real-time HTTPS traffic using Wireshark on an active network interface.
2. Filter and dissect each step of the **TLS 1.2 and TLS 1.3 cryptographic handshake**.
3. Inspect negotiated **Cipher Suites** (e.g., `TLS_AES_128_GCM_SHA256`, `ECDHE-RSA-AES256-GCM-SHA384`).
4. Extract and inspect Server Digital Certificates, Server Name Indication (SNI), and ephemeral Diffie-Hellman Key Exchange parameters.

---

## 🛠️ Tool Setup & Environment
- **Tool:** Wireshark (v4.x / v3.x)
- **Capture Environment:** Active Ethernet / Wi-Fi Adapter
- **TLS Handshake Exchange Sequence:**

```text
+------------------------------------------------------------------------+
|                      TLS 1.3 / 1.2 HANDSHAKE FLOW                      |
+------------------------------------------------------------------------+
|  CLIENT (Browser)                                    SERVER (Web Host) |
|         |                                                   |          |
|         | ----- [1. Client Hello] ------------------------> |          |
|         |       - TLS Version: TLS 1.3 (0x0304)             |          |
|         |       - Random Nonce (32 Bytes)                   |          |
|         |       - Supported Cipher Suites List              |          |
|         |       - Server Name Indication (SNI): google.com  |          |
|         |       - Key Share: Client Public X25519           |          |
|         |                                                   |          |
|         | <---- [2. Server Hello] ------------------------- |          |
|         |       - Selected Cipher Suite (AES_128_GCM_SHA256)|          |
|         |       - Server Key Share: Public X25519           |          |
|         |                                                   |          |
|         | <---- [3. Encrypted Extensions & Certificate] --- |          |
|         |       - Server X.509 Certificate Chain            |          |
|         |       - Certificate Verify (Digital Signature)    |          |
|         |                                                   |          |
|         | <---- [4. Finished (HMAC/AEAD)] ----------------- |          |
|         |                                                   |          |
|         | ----- [5. Finished (Client)] -------------------> |          |
|         |                                                   |          |
|  ====== SECURE ENCRYPTED APPLICATION DATA CHANNEL (HTTP/2 / HTTP/3) == |
|         | <==== [Encrypted Application Data (AEAD)] =======>|          |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. Structure of Cipher Suite String
Example: `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
- **Protocol:** `TLS`
- **Key Exchange Algorithm:** `ECDHE` (Elliptic Curve Diffie-Hellman Ephemeral - provides Perfect Forward Secrecy)
- **Authentication Algorithm:** `RSA` (Server identity verification via RSA signature)
- **Bulk Data Encryption Cipher:** `AES_256_GCM` (Galois/Counter Mode - Authenticated Encryption)
- **Hash / PRF Function:** `SHA384` (Used for Key Derivation and HMAC)

### 2. Perfect Forward Secrecy (PFS)
Using ephemeral Diffie-Hellman keys (`ECDHE`) ensures that even if the server's long-term private RSA key is compromised in the future, past recorded encrypted sessions cannot be decrypted.

---

## 💻 Step-by-Step Wireshark Capture Procedure

1. **Start Wireshark** with administrative/root privileges.
2. Select the active internet-connected network interface (e.g., `Wi-Fi` or `eth0`).
3. Click the blue **Start Capturing Packets** shark fin icon.
4. Open a web browser (or terminal) and access an HTTPS site:
   ```bash
   curl -I https://www.google.com
   ```
5. Return to Wireshark and stop the capture.
6. Apply the display filter in the filter bar:
   ```text
   tls.handshake
   ```
7. Click on the **Client Hello** packet:
   - Expand `Transport Layer Security` -> `TLSv1.2/TLSv1.3 Record Layer` -> `Handshake Protocol: Client Hello`.
   - Inspect `Cipher Suites`, `Extension: server_name`, and `Extension: key_share`.
8. Click on the **Server Hello** packet:
   - Inspect `Cipher Suite: TLS_AES_128_GCM_SHA256 (0x1301)`.
9. Apply filter `tls.record.content_type == 23` to view encrypted application data packets.

---

## 📊 Results & Packet Inspection Breakdown

```text
===========================================================================
 WIRESHARK TLS PACKET DISSECTION LOGS
===========================================================================

[Packet #14] Protocol: TLSv1.3 | Info: Client Hello
  - Frame Length: 517 bytes
  - Extension: server_name (len=15) -> "www.google.com"
  - Cipher Suites (17 suites offered):
      * TLS_AES_256_GCM_SHA384 (0x1302)
      * TLS_CHACHA20_POLY1305_SHA256 (0x1303)
      * TLS_AES_128_GCM_SHA256 (0x1301)
      * TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 (0xc02c)
  - Key Share Extension: Group: x25519, Key Exchange Data: 32 bytes

[Packet #16] Protocol: TLSv1.3 | Info: Server Hello
  - Selected Cipher Suite: TLS_AES_128_GCM_SHA256 (0x1301)
  - Key Share Extension: Group: x25519 (32 bytes server ephemeral public key)

[Packet #18] Protocol: TLSv1.3 | Info: Application Data (Encrypted)
  - Content Type: Application Data (23)
  - Encrypted Payload: 1,370 bytes of high-entropy ciphertext (HTTP/2 payload completely shielded)

===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: What is the Server Name Indication (SNI) extension and why is it sent in the Client Hello?**
   - **Answer:** SNI allows the client to specify the target hostname during the TLS handshake before encryption begins. This enables a single web server with one IP address to host multiple distinct HTTPS domain certificates (Virtual Hosting).

2. **Q2: Why did TLS 1.3 remove static RSA key exchange?**
   - **Answer:** Static RSA key exchange lacks **Forward Secrecy**. If the server's private key was ever leaked in the future, an attacker who recorded historical network traffic could decrypt all past sessions. TLS 1.3 mandates ephemeral Diffie-Hellman (`ECDHE`).

3. **Q3: What Wireshark display filter isolates only TLS Application Data?**
   - **Answer:** `tls.record.content_type == 23` or `tls.app_data`.
