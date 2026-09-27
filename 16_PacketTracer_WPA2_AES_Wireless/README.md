# Practical 16: Design and Implement a Secure Wireless Network using WPA2 Encryption (AES) in Cisco Packet Tracer

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 16
- **Practical Problem Statement:** Design and implement a secure wireless network using WPA2 encryption (AES) in Cisco Packet Tracer, and verify secure communication.
- **Tool Required:** Cisco Packet Tracer 8.x
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Design and simulate a secure Wireless Local Area Network (WLAN) topology in **Cisco Packet Tracer**.
2. Configure a Wireless Access Point / Router with **WPA2-Personal (WPA2-PSK)** using **AES-CCMP** encryption.
3. Configure wireless network interfaces (`WPC300N` NICs) on endpoint laptops and smartphones with matching SSID and pre-shared credentials.
4. Verify secure association, DHCP IP assignment, and end-to-end communication via ICMP ping simulation.
5. Demonstrate rejection and association failure for unauthorized rogue clients.

---

## 🛠️ Tool Setup & Environment
- **Tool:** Cisco Packet Tracer 8.x
- **Network Topology Architecture:**

```text
+------------------------------------------------------------------------+
|           CISCO PACKET TRACER WPA2-AES SECURE WLAN TOPOLOGY            |
+------------------------------------------------------------------------+
|                                                                        |
|  [CORPORATE LAN BACKBONE]                                              |
|  +--------------------+             +--------------------+             |
|  | Central Web Server |             | 2960 Core Switch   |             |
|  | IP: 192.168.1.10   | ----------- | (Switch0)          |             |
|  +--------------------+             +--------------------+             |
|                                                |                       |
|                                                | GigabitEthernet 0/1   |
|                                                v                       |
|                             +---------------------------------------+  |
|                             | WRT300N Wireless Access Router (AP)   |  |
|                             | LAN IP: 192.168.1.1 (DHCP Server)     |  |
|                             | SSID: "Crypto_Secure_WLAN"            |  |
|                             | Security: WPA2-PSK [AES]              |  |
|                             | Passphrase: "SecureWirelessPass2026!" |  |
|                             +---------------------------------------+  |
|                                      /                     \           |
|                     802.11n Wireless/                       \          |
|                      (WPA2-AES)    /                         \         |
|                                   v                           v        |
|                       +-----------------------+   +------------------+ |
|                       | Laptop-A (Authorized) |   | Smartphone-1     | |
|                       | IP: 192.168.1.100     |   | IP: 192.168.1.101| |
|                       +-----------------------+   +------------------+ |
|                                                                        |
|                       +-----------------------+                        |
|                       | Rogue Laptop (Failed) | (Wrong Pre-Shared Key) |
|                       | Status: REJECTED      |                        |
|                       +-----------------------+                        |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. Evolution of Wi-Fi Security Standards
- **WEP (Wired Equivalent Privacy):** Used RC4 stream cipher with static 24-bit IVs. Completely broken (FMS attack cracks keys in seconds).
- **WPA (Wi-Fi Protected Access):** Stopgap standard using TKIP (Temporal Key Integrity Protocol). Deprecated due to Beck-Tews attacks.
- **WPA2 (IEEE 802.11i):** Enforces **AES-CCMP** (Counter Mode with Cipher Block Chaining Message Authentication Code Protocol). Guarantees confidentiality, integrity, and replay protection.
- **WPA3:** Introduces SAE (Simultaneous Authentication of Equals) to eliminate offline dictionary attacks on handshakes.

### 2. The IEEE 802.11i 4-Way Handshake
1. **Pairwise Master Key (PMK):** Derived via PBKDF2: $	ext{PMK} = 	ext{PBKDF2}(	ext{Passphrase}, 	ext{SSID}, 4096, 256)$.
2. **Message 1 (AP -> Station):** AP sends random Authenticator Nonce ($ANonce$).
3. **Message 2 (Station -> AP):** Station generates Supplicant Nonce ($SNonce$), derives **Pairwise Transient Key (PTK)** from $(PMK, ANonce, SNonce, 	ext{MAC}_{	ext{AP}}, 	ext{MAC}_{	ext{STA}})$, and sends $SNonce$ + Message Integrity Code (MIC).
4. **Message 3 (AP -> Station):** AP verifies MIC, derives PTK, and transmits encrypted Group Temporal Key (GTK) for broadcast traffic.
5. **Message 4 (Station -> AP):** Station sends confirmation ACK. Encrypted communication begins.

---

## 💻 Step-by-Step Cisco Packet Tracer Configuration

1. **Build the Topology:**
   - Place **1 WRT300N Wireless Router**, **1 Cisco 2960 Switch**, **1 Server-PT**, and **2 Laptops**.
   - Connect Server to Switch `FastEthernet 0/1` via Copper Straight-Through cable.
   - Connect Switch `FastEthernet 0/2` to WRT300N `Ethernet 1` port.
2. **Configure Router Wireless Security:**
   - Click **WRT300N** -> Open **GUI** tab.
   - Go to **Wireless -> Basic Wireless Settings**:
     - Network Mode: `Mixed`
     - Network Name (SSID): `Crypto_Secure_WLAN`
     - SSID Broadcast: `Enabled`
     - Click **Save Settings**.
   - Go to **Wireless -> Wireless Security**:
     - Security Mode: `WPA2 Personal`
     - Encryption: `AES`
     - Passphrase: `SecureWirelessPass2026!`
     - Click **Save Settings**.
   - Go to **Setup -> Basic Setup**:
     - IP Address: `192.168.1.1`
     - Subnet Mask: `255.255.255.0`
     - DHCP Server: `Enabled` (Start IP: `192.168.1.100`, Max Users: 50)
     - Click **Save Settings**.
3. **Equip and Connect Client Laptops:**
   - Click **Laptop-A** -> **Physical** tab -> Turn power OFF -> Drag out Ethernet NIC -> Drag in **WPC300N** wireless card -> Turn power ON.
   - Go to **Desktop** -> **PC Wireless** -> Click **Connect** tab -> Click **Refresh**.
   - Select `Crypto_Secure_WLAN` -> Click **Connect**.
   - Enter WPA2 Passphrase: `SecureWirelessPass2026!` -> Click **Connect**.
   - Wireless signal waves will immediately appear connecting Laptop-A to WRT300N!
4. **Verification:**
   - Open **Laptop-A Command Prompt** -> Run `ipconfig` (Verify IP: `192.168.1.100`).
   - Ping default gateway: `ping 192.168.1.1` (100% Success).
   - Ping server: `ping 192.168.1.10` (100% Success).
5. **Rogue Client Simulation:**
   - Configure a third laptop with wrong passphrase `WrongPassword123`.
   - Observe that the 4-Way Handshake fails (PTK mismatch) and the client is denied association and IP allocation.

---

## 📊 Results & Simulation Verification

```text
===========================================================================
 PACKET TRACER SIMULATION VERIFICATION OUTPUT
===========================================================================

Laptop-A> ipconfig
FastEthernet0 Connection:(default port)
   Connection-specific DNS Suffix..: 
   Link-local IPv6 Address.........: FE80::201:96FF:FE12:3456
   IPv4 Address....................: 192.168.1.100
   Subnet Mask.....................: 255.255.255.0
   Default Gateway.................: 192.168.1.1

Laptop-A> ping 192.168.1.1
Pinging 192.168.1.1 with 32 bytes of data:
Reply from 192.168.1.1: bytes=32 time=1ms TTL=64
Reply from 192.168.1.1: bytes=32 time=1ms TTL=64
Reply from 192.168.1.1: bytes=32 time=1ms TTL=64
Reply from 192.168.1.1: bytes=32 time=1ms TTL=64

Ping statistics for 192.168.1.1:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 1ms, Maximum = 1ms, Average = 1ms

Laptop-A> ping 192.168.1.10
Pinging 192.168.1.10 with 32 bytes of data:
Reply from 192.168.1.10: bytes=32 time=2ms TTL=128
Reply from 192.168.1.10: bytes=32 time=2ms TTL=128

Ping statistics for 192.168.1.10:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
===========================================================================
```

---

## 📈 Security Comparison Matrix (BL4 Analyze)

| Feature | WEP (Wired Equivalent Privacy) | WPA (Wi-Fi Protected Access) | WPA2 (IEEE 802.11i) | WPA3 |
|:---|:---|:---|:---|:---|
| **Cipher Algorithm** | RC4 Stream Cipher | RC4 with TKIP | **AES in CCMP Mode** | AES-GCM (128/256-bit) |
| **Key Length** | 64 or 128-bit (24-bit IV) | 128-bit TKIP | **128-bit AES** | 128-bit / 192-bit CNSA |
| **Integrity Mechanism**| CRC-32 (Linear, Non-crypto) | Michael MIC (64-bit) | **CBC-MAC (128-bit)** | GMAC (Galois MAC) |
| **Key Exchange** | Static pre-shared key | 4-Way Handshake (TKIP) | **4-Way Handshake (AES PTK)**| SAE (Dragonfly handshake) |
| **Security Status** | **BROKEN** (< 60s crack) | **DEPRECATED** | **ENTERPRISE STANDARD** | **NEXT-GEN STANDARD** |

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: What is CCMP in WPA2 and why is it superior to TKIP?**
   - **Answer:** CCMP (Counter Mode with Cipher Block Chaining Message Authentication Code Protocol) combines AES in Counter mode (for confidentiality) with CBC-MAC (for authentication and integrity). Unlike TKIP which was patched onto weak RC4 hardware, CCMP uses the proven AES block cipher from the ground up.

2. **Q2: What is the difference between WPA2-Personal (PSK) and WPA2-Enterprise?**
   - **Answer:**
     - **WPA2-Personal:** All clients use a shared Pre-Shared Key (passphrase). Suitable for home/SOHO networks.
     - **WPA2-Enterprise:** Uses an **IEEE 802.1X RADIUS server** where each user authenticates with individual unique credentials/certificates, providing individualized encryption keys and central auditing.

3. **Q3: What attack is WPA2-PSK vulnerable to, and how does WPA3 mitigate it?**
   - **Answer:** WPA2-PSK is vulnerable to **offline dictionary attacks** if an attacker captures the 4-Way Handshake packets. WPA3 replaces PSK with **SAE (Simultaneous Authentication of Equals)** based on the Dragonfly handshake, which prevents offline dictionary attacks even if weak passwords are used.
