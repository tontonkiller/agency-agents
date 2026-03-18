#!/usr/bin/env python3
"""Serveur local pour The Wisdom Engine — ouvre index.html sur mobile."""
import http.server
import os
import socket
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Trouver l'IP locale pour accès mobile
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

handler = http.server.SimpleHTTPRequestHandler
server = http.server.HTTPServer(("0.0.0.0", PORT), handler)

ip = get_local_ip()
print(f"\n  The Wisdom Engine — Serveur local")
print(f"  ──────────────────────────────────")
print(f"  PC      : http://localhost:{PORT}")
print(f"  Mobile  : http://{ip}:{PORT}")
print(f"  (ton tel doit être sur le même WiFi)\n")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n  Serveur arrêté.")
