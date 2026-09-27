# Practical 11: Capture and Analyze Encrypted VPN Traffic vs Unencrypted Traffic using Wireshark

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 11
- **Practical Problem Statement:** Capture and analyze encrypted VPN traffic using Wireshark, and compare it with unencrypted network communication.
- **Tool Required:** Wireshark Network Protocol Analyzer
- **Bloom's Taxonomy Level:** BL4 (Analyze)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Capture unencrypted network packets (HTTP, DNS, Telnet) and observe cleartext payload exposure.
2. Capture encapsulated VPN tunnel packets (OpenVPN / IPsec ESP / WireGuard) over the physical interface.
3. Compare packet headers, payload entropy, protocol visibility, and metadata leakage between unencrypted and VPN-tunneled traffic.
4. Understand tunneling protocols, IP encapsulation, and data confidentiality.

---

## 🛠️ Tool Setup & Environment
- **Tool:** Wireshark
- **Comparison Architecture:**

```text
+------------------------------------------------------------------------+
|                 UNENCRYPTED TRAFFIC VS VPN TUNNEL TRAFFIC              |
+------------------------------------------------------------------------+
|                                                                        |
|  [SCENARIO A: UNENCRYPTED CLEAR-TEXT COMMUNICATION]                    |
|  [User PC] =================[ Public Internet ]=================> [Web]|
|    Packet: [ IP Header | TCP Header | HTTP GET /login.php user=admin ] |
|    * Wireshark Eavesdropper: Sees full URL, passwords, & raw payload!  |
|                                                                        |
|  [SCENARIO B: ENCRYPTED VPN TUNNEL (OPENVPN / WIREGUARD / IPSEC)]      |
|  [User PC] -----[ Virtual tun0: IP/TCP/HTTP ]-----+                    |
|                      |                            |                    |
|                      v (AES-256-GCM Encrypted)    |                    |
|  [Physical NIC: Outer IP Header | UDP Port 1194 | High Entropy Crypto ]|
|                      |                                                 |
|                      v                                                 |
|  =================[ Encrypted VPN Tunnel ]=========================>  |
|    * Wireshark Eavesdropper: Sees only random encrypted UDP bytes!     |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. VPN Encapsulation Mechanics
A Virtual Private Network creates a virtual network interface (e.g., `tun0`). When an application sends data:
1. Inner Packet generated: `[Src: 10.8.0.2 -> Dst: 93.184.216.34 | TCP | HTTP Payload]`
2. The entire inner packet is encrypted using symmetric AEAD (AES-256-GCM / ChaCha20-Poly1305).
3. Outer Packet constructed: `[Src: 192.168.1.50 -> Dst: 203.0.113.1 (VPN Server) | UDP Port 1194 | Encrypted Inner Packet]`

### 2. High Shannon Entropy of Ciphertext
Unencrypted ASCII text has low entropy ($H pprox 4.0 - 4.5\ 	ext{bits/byte}$). Encrypted VPN payloads exhibit maximum entropy ($H pprox 7.99 - 8.0\ 	ext{bits/byte}$), making pattern analysis and deep packet inspection (DPI) impossible without the session key.

---

## 💻 Step-by-Step Procedure in Wireshark

1. **Capture Unencrypted Traffic:**
   - Start Wireshark on physical interface.
   - Run in terminal: `curl http://testphp.vulnweb.com/login.php`
   - Apply filter: `http`
   - Right-click packet -> **Follow -> TCP Stream**. Observe raw HTML and parameters visible in plain text.
2. **Capture Encrypted VPN Traffic:**
   - Connect to OpenVPN or WireGuard tunnel.
   - Run the same web request through the active VPN tunnel.
   - Filter Wireshark on physical interface: `udp.port == 1194 or esp or udp.port == 51820`
   - Right-click packet -> **Follow -> UDP Stream**. Observe completely unreadable random binary ciphertext.

---

## 📊 Results & Side-by-Side Packet Dissection

```text
===========================================================================
 COMPARATIVE PACKET INSPECTION LOGS
===========================================================================

[+] 1. UNENCRYPTED HTTP PACKET (Port 80):
  - Transmission Control Protocol (TCP): Src Port 54321 -> Dst Port 80
  - Hypertext Transfer Protocol:
      GET /login.php HTTP/1.1
      Host: testphp.vulnweb.com
      User-Agent: curl/7.88.1
      Cookie: user=admin; session_id=SECRET_SESSION_12345
  -> SECURITY STATUS: CRITICAL RISK - Eavesdropper captured session cookie!

[+] 2. ENCRYPTED VPN PACKET (OpenVPN Port 1194 / WireGuard Port 51820):
  - User Datagram Protocol (UDP): Src Port 51820 -> Dst Port 51820
  - WireGuard / OpenVPN Encrypted Data (128 bytes):
      0000  04 00 00 00 a1 b2 c3 d4  e5 f6 07 18 29 3a 4b 5c
      0010  9f 8e 7d 6c 5b 4a 39 28  17 06 f5 e4 d3 c2 b1 a0
      ... (High Entropy: 7.998 bits/byte)
  -> SECURITY STATUS: SECURE - Zero payload, destination, or protocol leakage!
===========================================================================
```

---

## 📈 Comparative Analysis Matrix (BL4 Analyze)

| Analysis Parameter | Unencrypted Traffic (HTTP / DNS / Telnet) | Encrypted VPN Traffic (OpenVPN / IPsec) |
|:---|:---|:---|
| **Payload Visibility** | 100% Plaintext readable | 100% Encrypted (AES-256-GCM / ChaCha20) |
| **Destination IP Exposure** | Real target destination IP is public | Only VPN Gateway IP is visible |
| **DNS Query Privacy** | Plaintext DNS requests leak visited domains | Encapsulated inside encrypted VPN tunnel |
| **Integrity Protection** | None (Susceptible to MITM injection) | Cryptographic HMAC / Poly1305 AEAD Tag |
| **Overhead** | Minimal headers | Additional 40–60 bytes encapsulation overhead |

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: What metadata is still visible to an ISP or eavesdropper when a user is connected to a VPN?**
   - **Answer:** The eavesdropper can see the user's IP, the VPN server's IP, the port number (e.g., UDP 1194 or 51820), the connection timestamp, and packet size/timing patterns (traffic analysis), but cannot see visited URLs, DNS queries, or payload contents.

2. **Q2: What is the difference between IPsec Tunnel Mode and Transport Mode?**
   - **Answer:** Transport Mode encrypts only the IP payload while keeping the original IP header intact (host-to-host). Tunnel Mode encrypts the **entire original IP packet** (header + payload) and adds a completely new outer IP header (network-to-network VPN gateway).

3. **Q3: What is a "DNS Leak" in the context of VPNs?**
   - **Answer:** A DNS leak occurs when DNS requests bypass the encrypted VPN tunnel and are sent unencrypted to the default ISP DNS server, revealing visited domain names to eavesdroppers.
