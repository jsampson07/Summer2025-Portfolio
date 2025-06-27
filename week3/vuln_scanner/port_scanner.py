#TCP-connect scan fallback (on ICMP failure) feature
import socket
import ipaddress
import argparse
import json
import requests
import re
from requests import HTTPError
from scapy.all import IP, ICMP, sr1
from typing import List, Dict, Tuple

def ping_sweeper(subnet: str, timeout: float) -> Tuple[List[str], List[str]]:
    """Returns a list of IPs in the subnet specified that replied to ICMP"""
    #WE ARE PASSED IN A SUBNET so generate a whole list of host IPs
    live_hosts, unresponsive_hosts = [], []
    network = ipaddress.ip_network(subnet)
    for host_ip in network.hosts(): #network.hosts is an Iterable object containing all IP addresses except network addr and network broadcast addr
        #cast host to a str since it is IPv4Address right now
        try:
            echo = IP(dst=str(host_ip)) / ICMP()
            reply = sr1(echo, retry=3, timeout=timeout, verbose=False)
            if reply: #will get at most 1 reply back because 1 request made
                #print(f"Echo reply received from host: {str(host_ip)}")
                live_hosts.append(str(host_ip))
            else:
                unresponsive_hosts.append(str(host_ip))
        except Exception as e:
            print(f"Oops an unknown exception has occurred: {e}")
    return live_hosts, unresponsive_hosts

def tcp_fallback(hosts: List[str], ports: List[int], timeout: float) -> Dict[str, List[int]]:
    """Returns a list of IPs in the subnet specified that created a successful TCP connection"""
    #A dict with {host: [ports...]} that established successful TCP connection
    success = {}
    for host in hosts:
        for port in ports:
            try:
                with socket.create_connection((host,port)) as s:
                    if host not in success:
                        success[host] = [port]
                    else:
                        success[host].append(port)
            except socket.timeout as e:
                print(f"No response received within {timeout} seconds: {e}")
            except ConnectionRefusedError as e:
                print(f"Connection could not be established: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    return success

"""

2. **Add Service Fingerprinting**  
   - Use the `requests` library (install via `pip install requests`) to issue `HEAD` or `GET` to `http://<ip>:80/` 
    for any found HTTP port; parse `Server:` header.  
   - For SSH (port 22), open a raw TCP socket, send a newline, and read the banner.  
   - **Deliverable:** update `vuln_scanner.py` to output JSON:
     ```jsonc
     {
       "ip": "192.168.1.5",
       "open_ports": [22, 80],
       "server_banner": "nginx/1.18.0"
     }
     ```
"""
def finger_printing(hosts: Dict[str, List[str]]):
    fp_result = []
    for host, ports in hosts.items():
        banners = {}
        for port in ports:
            if port == 80:
                response = requests.get(f"http://{host}:80")
                try:
                    #print(response.text)
                    headers = response.headers
                    server = headers["Server"]
                    server = server.strip()
                    banners[port] = server
                except HTTPError as e:
                    print(f"HTTP error occurred: {e}")
                    print(f"Status code: {response.status_code}")
            if port == 443:
                response = requests.get(f"https://{host}:443")
                try:
                    headers = response.headers
                    server = headers["Server"]
                    server = server.strip()
                    banners[port] = server
                except HTTPError as e:
                    print(f"HTTP error occurred: {e}")
                    print(f"Status code: {response.status_code}")
            #- For SSH (port 22), open a raw TCP socket, send a newline, and read the banner. 
            if port == 22:
                with socket.create_connection((host, port), timeout=1) as s:
                    try:
                        s.send(b"\n")
                        response = s.recv(1024) #returns BYTES object
                        decode_resp = response.decode("utf-8").strip()
                        #print(response)
                        banners[port] = decode_resp
                    except ConnectionRefusedError as e:
                        print(f"Connection could not be established with {host}:{port}: {e}")
                    except socket.timeout as e:
                        print(f"Timeout: {e}")
        fp_result.append({
            "ip": host,
            "ports": ports,
            "banners": banners
        })
    return fp_result

def inline_list(match):
    # inner block
    inner = match.group(1).strip()
    # collapse all into single spaces
    collapsed = ' '.join(inner.split())
    return '[' + collapsed + ']'

def main():
    #TEST REALLY QUICKLY
    parser = argparse.ArgumentParser(prog="port_scanner.py", description="used to 1) ICMP-sweep a subnet, 2) TCP-connect scan any unresponsive hosts")
    parser.add_argument("-s", "--subnet", required=True, type=str, help="Subnet to scan i.e. 127.0.0.1/24")
    parser.add_argument("-p", "--port", default="22,80,443", type=str, help="Comma-separated ports used for TCP fallback: i.e. 22,80,443")
    #default value in "port" just for testing purposes (REMOVE after)
    parser.add_argument("-t", "--timeout", default=1.0, type=float, help="Used to override default timeout value")

    args = parser.parse_args()

    try:
        network = ipaddress.ip_network(args.subnet)
    except ValueError as e:
        parser.error(f"Invalid subnet: {args.subnet}")

    ports = [int(p) for p in args.port.split(",")]
    final_hosts = {}

    #Scan for ICMP responders and scan ports for each
    icmp_alive, dead = ping_sweeper(args.subnet, args.timeout)
    #print(f"ICMP_alive output: {icmp_alive}")
    icmp_alive_tcp = tcp_fallback(icmp_alive, ports, args.timeout)
    icmp_info = {ip:[] for ip in icmp_alive}
    for host, ports in icmp_alive_tcp.items():
        icmp_info[host] = ports

    #Scan for TCP hosts on unresponsive hosts for ICMP (and scan ports for each)
    tcp_alive = tcp_fallback(dead, ports, args.timeout)
    final_hosts.update(icmp_info)
    final_hosts.update(tcp_alive)
    
    #print(json.dumps(final_hosts, indent=2))

    result = finger_printing(final_hosts)
    json_format = json.dumps(result, indent=2)

    pattern = re.compile(r'\[\s+([^\[\]]*?)\s+\]', re.DOTALL)
    pretty_format = pattern.sub(inline_list, json_format)
    print(pretty_format)

    #takes in subnet, port, and/or timeout val
    

if __name__ == "__main__":
    main()