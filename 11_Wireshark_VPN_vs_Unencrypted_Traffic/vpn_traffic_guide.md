# VPN Capture Reference Guide

## Wireshark Filters for VPN Protocols
- OpenVPN UDP: `udp.port == 1194`
- OpenVPN TCP: `tcp.port == 1194`
- WireGuard: `udp.port == 51820`
- IPsec ESP: `esp`
- IPsec IKE: `udp.port == 500 or udp.port == 4500`
