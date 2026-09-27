# Wireshark HTTPS / TLS Capture Reference Guide

## Quick Wireshark Display Filters for TLS
- View All TLS Packets: `tls`
- View All Handshakes: `tls.handshake`
- Filter Client Hello: `tls.handshake.type == 1`
- Filter Server Hello: `tls.handshake.type == 2`
- Filter Certificate Message: `tls.handshake.type == 11`
- Filter Encrypted App Data: `tls.record.content_type == 23`
- Filter by SNI Domain: `tls.handshake.extensions_server_name contains "google"`
