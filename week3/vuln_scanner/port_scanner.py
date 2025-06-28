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
    #subnet --> turn into list of host IPs on the subnet
    live_hosts, unresponsive_hosts = [], []
    network = ipaddress.ip_network(subnet)
    for host_ip in network.hosts(): # Every potential host IP addr (IPv4Address) on the network
        try:
            echo = IP(dst=str(host_ip)) / ICMP()
            reply = sr1(echo, retry=3, timeout=timeout, verbose=False)
            if reply:
                live_hosts.append(str(host_ip))
            else:
                unresponsive_hosts.append(str(host_ip))
        except OSError as e:
            print(f"Socket error: {e}")
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

def finger_printing(hosts: Dict[str, List[str]]):
    fp_result = []
    for host, ports in hosts.items():
        banners = {}
        for port in ports:
            if port == 80:
                response = requests.get(f"http://{host}:80")
                try:
                    headers = response.headers
                    server = headers["Server"]
                    server = server.strip()
                    banners[port] = server
                except HTTPError as e:
                    print(f"HTTP error occurred: {e}")
                    print(f"Status code: {response.status_code}")
                except Exception as e:
                    print(f"Unexpected error occurred: {e}")
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
                except Exception as e:
                    print(f"Unexpected error occurred: {e}")
            # for SSH (port 22), open a raw TCP socket, send a newline, and read the banner
            if port == 22:
                with socket.create_connection((host, port), timeout=1) as s:
                    try:
                        s.send(b"\n")
                        response = s.recv(1024) # bytes object
                        decode_resp = response.decode("utf-8").strip()
                        banners[port] = decode_resp
                    except ConnectionRefusedError as e:
                        print(f"Connection could not be established with {host}:{port}: {e}")
                    except socket.timeout as e:
                        print(f"Timeout: {e}")
                    except Exception as e:
                        print(f"Unexpected error occurred: {e}")
        fp_result.append({"ip": host, "ports": ports, "banners": banners})
    return fp_result

def inline_list(match):
    # inner block
    inner = match.group(1).strip()
    # collapse all into single spaces
    collapsed = ' '.join(inner.split())
    return '[' + collapsed + ']'

def main():
    parser = argparse.ArgumentParser(prog="port_scanner.py", description="used to 1) ICMP-sweep a subnet, 2) TCP-connect scan any unresponsive hosts")
    parser.add_argument("-s", "--subnet", required=True, type=str, help="Subnet to scan i.e. 127.0.0.1/24")
    parser.add_argument("-p", "--port", default="22,80,443", type=str, help="Comma-separated ports used for TCP fallback: i.e. 22,80,443")
    parser.add_argument("-t", "--timeout", default=1.0, type=float, help="Used to override default timeout value")

    args = parser.parse_args()

    try:
        network = ipaddress.ip_network(args.subnet)
    except ValueError as e:
        parser.error(f"Invalid subnet: {args.subnet}")

    ports = [int(p) for p in args.port.split(",")]
    final_hosts = {}

    icmp_alive, dead = ping_sweeper(args.subnet, args.timeout)
    icmp_alive_tcp = tcp_fallback(icmp_alive, ports, args.timeout)
    icmp_info = {ip:[] for ip in icmp_alive}
    for host, ports in icmp_alive_tcp.items():
        icmp_info[host] = ports

    tcp_alive = tcp_fallback(dead, ports, args.timeout)
    final_hosts.update(icmp_info)
    final_hosts.update(tcp_alive)

    result = finger_printing(final_hosts)
    json_format = json.dumps(result, indent=2)

    pattern = re.compile(r'\[\s+([^\[\]]*?)\s+\]', re.DOTALL)
    pretty_format = pattern.sub(inline_list, json_format)
    print(pretty_format)

if __name__ == "__main__":
    main()