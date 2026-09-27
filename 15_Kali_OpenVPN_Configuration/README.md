# Practical 15: Configure a Secure VPN using OpenVPN & Verify Encrypted Communication (Kali Linux)

## 📌 Academic Metadata
- **Course Name:** Cryptography
- **Course Code:** CSL0509
- **Semester:** Cryptography (CSL0509) – B.Tech AIML V Semester
- **Faculty Name:** Mr. Hirendra Singh Sengar
- **Academic Year:** 2026–27
- **Practical No:** 15
- **Practical Problem Statement:** Configure a secure VPN using OpenVPN and verify encrypted communication between connected systems.
- **Tool Required:** Kali Linux (OpenVPN, Easy-RSA PKI, Wireshark)
- **Bloom's Taxonomy Level:** BL3 (Apply)
- **Course Outcome (CO):** CO4

---

## 🎯 Objectives
1. Build a custom **Public Key Infrastructure (PKI)** using `easy-rsa` to issue Certificate Authority (`ca.crt`), Server (`server.crt`), and Client (`client.crt`) digital certificates.
2. Generate Diffie-Hellman parameters (`dh2048.pem`) and an HMAC TLS-Auth firewall key (`ta.key`).
3. Configure the OpenVPN Server daemon (`server.conf`) with `tun0` virtual network adapter routing and AES-256-GCM encryption.
4. Establish the VPN tunnel from a client and verify end-to-end encrypted packet transmission using ping and Wireshark.

---

## 🛠️ Tool Setup & Environment
- **OS:** Kali Linux (Server & Client)
- **Tools:** `openvpn`, `easy-rsa`, `iptables`, `iproute2`
- **OpenVPN Infrastructure Architecture:**

```text
+------------------------------------------------------------------------+
|                     OPENVPN PKI & TUNNEL TOPOLOGY                      |
+------------------------------------------------------------------------+
|                                                                        |
|  [EASY-RSA CERTIFICATE AUTHORITY]                                      |
|  - Root CA (ca.crt / ca.key)                                           |
|  - Server Cert (server.crt / server.key)                               |
|  - Client Cert (client.crt / client.key)                               |
|  - DH Parameters (dh2048.pem) & HMAC Firewall Key (ta.key)             |
|                                                                        |
|  +---------------------------+           +---------------------------+ |
|  |     OPENVPN SERVER        |           |      OPENVPN CLIENT       | |
|  | Physical IP: 192.168.1.10 |           | Physical IP: 192.168.1.20 | |
|  | Virtual IP : 10.8.0.1     |           | Virtual IP : 10.8.0.2     | |
|  +---------------------------+           +---------------------------+ |
|        | [tun0 Adapter]                                | [tun0]        |
|        |                                               |               |
|        +====== TLS-Auth / AES-256-GCM Encrypted =======+               |
|                UDP Tunnel over Port 1194                               |
|                                                                        |
|  [PACKET VERIFICATION TEST]                                            |
|  Client executes: ping 10.8.0.1 (ICMP inside virtual tunnel)           |
|  Wireshark on eth0 captures: 100% Encrypted UDP OpenVPN Packets!       |
+------------------------------------------------------------------------+
```

---

## 📖 Theoretical Background & Mathematical Foundations

### 1. OpenVPN Dual-Channel Architecture
OpenVPN operates two distinct cryptographic channels multiplexed over a single UDP/TCP port:
1. **Control Channel:** Performs TLS 1.3 / TLS 1.2 handshake using RSA/ECDSA certificates and ephemeral Diffie-Hellman exchange to authenticate peers and negotiate dynamic data channel symmetric session keys.
2. **Data Channel:** Encrypts bulk IP traffic using high-throughput symmetric authenticated ciphers (**AES-256-GCM** or **ChaCha20-Poly1305**).

### 2. TLS-Auth / TLS-Crypt (`ta.key`)
An additional pre-shared HMAC secret key used to sign and encrypt control channel handshake packets. Unauthenticated packets, port scans, and DoS attacks are dropped immediately before initiating TLS state allocation.

---

## 💻 Step-by-Step Configuration & Execution

1. **Initialize PKI with Easy-RSA:**
   ```bash
   make-cadir ~/openvpn-ca && cd ~/openvpn-ca
   ./easyrsa init-pki
   ./easyrsa build-ca nopass
   ./easyrsa gen-req server nopass
   ./easyrsa sign-req server server
   ./easyrsa gen-dh
   openvpn --genkey secret ta.key
   ```

2. **Generate Client Credentials:**
   ```bash
   ./easyrsa gen-req client1 nopass
   ./easyrsa sign-req client client1
   ```

3. **Configure and Launch OpenVPN Server:**
   ```bash
   sudo openvpn --config server.conf
   ```

4. **Connect Client:**
   ```bash
   sudo openvpn --config client.ovpn
   ```

5. **Verify Secure Communication:**
   ```bash
   # From client:
   ping -c 4 10.8.0.1
   ```

---

## 📊 Results & Verification Logs

```text
===========================================================================
 OPENVPN TUNNEL ESTABLISHMENT & ENCRYPTION VERIFICATION
===========================================================================

[+] Server Startup:
  OpenVPN 2.6.9 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD]
  Diffie-Hellman initialized with 2048 bit key
  Outgoing Control Channel Authentication: Using 256 bit message hash 'SHA256' for HMAC authentication
  TUN/TAP device tun0 opened
  net_iface_up: set tun0 up
  net_addr_v4_add: 10.8.0.1/24 dev tun0
  UDPv4 link local (bound): [AF_INET][undef]:1194
  UDPv4 link remote: [AF_UNSPEC]
  Initialization Sequence Completed

[+] Client Connection:
  Peer Connection Initiated with [AF_INET]192.168.1.10:1194
  Control Channel: TLSv1.3, cipher TLS_AES_256_GCM_SHA384, 2048 bit RSA
  [server] Peer Connection Initiated with [AF_INET]192.168.1.10:1194
  Data Channel: Cipher 'AES-256-GCM' initialized with 256 bit key
  TUN/TAP device tun0 opened: Assigned IP: 10.8.0.2
  Initialization Sequence Completed

[+] Tunnel Ping Test:
  PING 10.8.0.1 (10.8.0.1) 56(84) bytes of data.
  64 bytes from 10.8.0.1: icmp_seq=1 ttl=64 time=1.12 ms
  64 bytes from 10.8.0.1: icmp_seq=2 ttl=64 time=0.98 ms
  --- 10.8.0.1 ping statistics ---
  2 packets transmitted, 2 received, 0% packet loss

[+] Wireshark Capture on Physical Interface:
  All packets are encrypted UDP frames on port 1194. Zero ICMP plaintext visible!
===========================================================================
```

---

## ❓ Viva-Voce Questions & In-Depth Answers

1. **Q1: What is the difference between TUN mode and TAP mode in OpenVPN?**
   - **Answer:**
     - **TUN (Network Tunnel):** Operates at OSI **Layer 3 (IP)**. Routes IP packets efficiently; does not forward broadcast/multicast traffic; lighter overhead.
     - **TAP (Network Tap):** Operates at OSI **Layer 2 (Ethernet)**. Forwards raw Ethernet frames, MAC addresses, and non-IP protocols; higher overhead.

2. **Q2: Why is UDP preferred over TCP for VPN tunneling?**
   - **Answer:** Running TCP inside TCP causes the **TCP Meltdown problem**: when packet loss occurs, both the inner and outer TCP stacks trigger retransmissions and exponential congestion backoff simultaneously, severely degrading performance. UDP avoids redundant reliability layers.

3. **Q3: What purpose does `dh2048.pem` serve in OpenVPN?**
   - **Answer:** It provides precomputed prime parameters for Diffie-Hellman key exchange, enabling the server and client to negotiate ephemeral session encryption keys securely without transmitting the key across the network.
