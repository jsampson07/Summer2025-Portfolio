# Port Scanner (ICMP + TCP Fallback)

A Python-based port scanning tool that combines **ICMP sweeps**, **TCP-connect fallback scanning**, and basic **service fingerprinting**.  
This project demonstrates the use of raw sockets, TCP connections, and lightweight HTTP/SSH banner grabbing to identify responsive hosts and their running services across a subnet.  

It’s designed as a practical, educational tool for network administrators and cybersecurity enthusiasts to understand both **host discovery** and **service identification**.

---

## Features
- **ICMP Sweep**: Identifies hosts that respond to ICMP echo requests (ping).  
- **TCP Fallback**: Attempts TCP connections on specified ports for hosts that fail to respond to ICMP, ensuring no live host is missed.  
- **Service Fingerprinting**:
  - HTTP (port 80) and HTTPS (port 443) banner extraction using HTTP `HEAD` requests.
  - SSH (port 22) banner grabbing via raw TCP.  
- **JSON Output**: Pretty-printed JSON with IPs, open ports, and captured banners.  
- **Customizable**: Subnet, ports, timeouts, and verbosity are fully configurable from the CLI.  
- **Error Handling**: Gracefully handles timeouts, refused connections, and malformed responses.  

---

## Tech Stack
- **Language**: Python 3  
- **Libraries**: `socket`, `ipaddress`, `argparse`, `requests`, `scapy`  
- **Protocols**: ICMP, TCP/IP, HTTP/HTTPS, SSH  

---

## Usage

### Setup
```bash
#Clone the repository

git clone https://github.com/jsampson07/Summer2025-Portfolio.git
cd Summer2025-Portfolio/port-scanner-tool/week3/port-scanner

#Run the scanner

python3 port_scanner.py -s <subnet> -p <ports> -t <timeout> -v
