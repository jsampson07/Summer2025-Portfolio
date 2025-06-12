#IMPLEMENT THIS

import socket

def banner_grabber(host, ports=(22, 80, 443), timeout=2):
    for port in ports:
        try:
            # 1. Make a TCP connection (this does the 3-way handshake for you)
            sock = socket.create_connection((host, port), timeout=timeout)
            # 2. Read up to 1024 bytes of whatever comes next
            banner = sock.recv(1024)
            sock.close()
            
            if banner:
                # strip off trailing newlines, decode to text, print
                text = banner.strip().decode('utf-8', errors='ignore')
                print(f"[+] {host}:{port} → {text}")
            else:
                print(f"[-] {host}:{port} → (no banner)")
        except (socket.timeout, ConnectionRefusedError):
            print(f"[-] {host}:{port} → closed or no response")
        except Exception as e:
            print(f"[-] {host}:{port} → error: {e}")

if __name__ == "__main__":
    banner_grabber("scanme.nmap.org")
    # or banner_grabber("YOUR.DROPLET.IP")