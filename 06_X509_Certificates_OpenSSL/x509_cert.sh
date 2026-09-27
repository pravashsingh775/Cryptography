#!/bin/bash
# Practical 06: Self-Signed X.509 Certificate Generation
echo "=== Practical 06: X.509 Certificate Generation ==="

# Generate Certificate
openssl req -x509 -newkey rsa:2048 -nodes -keyout server_key.pem -out server_cert.crt -days 365   -subj "/C=IN/ST=Maharashtra/L=Mumbai/O=EngineeringCollege/CN=crypto.lab.local"

# View Complete Text Details
openssl x509 -in server_cert.crt -text -noout

# View Subject, Issuer, and Fingerprint
openssl x509 -in server_cert.crt -subject -issuer -fingerprint -sha256 -noout
