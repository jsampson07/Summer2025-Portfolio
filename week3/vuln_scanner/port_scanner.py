# TCP-connect scan fallback (on ICMP failure) feature
"""
Given a subnet, perform an ICMP sweep, and regardless of ICMP-responders or not,
attempt to establish a TCP connection with all hosts on the given subnet.
Then, fingerprint each host that responded to ICMP requests and/or TCP connections
"""
import socket
import ipaddress
import argparse
import json
import re
import logging
from typing import List, Dict, Tuple, Any, Match
import requests
from requests import HTTPError
from scapy.all import IP, ICMP, sr1

log = logging.getLogger(__name__)


def ping_sweeper(subnet: str, timeout: float) -> Tuple[List[str], List[str]]:
    """Returns a list of IPs in the subnet specified that replied to ICMP"""
    # subnet --> turn into list of host IPs on the subnet
    live_hosts, unresponsive_hosts = [], []
    network = ipaddress.ip_network(subnet)
    for host_ip in network.hosts():  # All possible host IP addr on the network
        try:
            echo = IP(dst=str(host_ip)) / ICMP()
            reply = sr1(echo, retry=3, timeout=timeout, verbose=False)
            if reply:
                live_hosts.append(str(host_ip))
            else:
                unresponsive_hosts.append(str(host_ip))
        except OSError as e:
            log.error("Socket error: %s", e)
        except Exception as e:
            log.exception("Unexpected error during ICMP sweep on %s", host_ip)
    return live_hosts, unresponsive_hosts


def tcp_fallback(hosts: List[str],
                 ports: List[int],
                 timeout: float) -> Dict[str, List[int]]:
    """Returns a list of IPs in the subnet specified that created a successful TCP connection"""
    # A dict with {host: [ports...]} that established successful TCP connection
    success = {}
    for host in hosts:
        for port in ports:
            try:
                with socket.create_connection((host, port)):
                    if host not in success:
                        success[host] = [port]
                    else:
                        success[host].append(port)
            except socket.timeout as e:
                log.error("No response received within %f seconds: %s", timeout, e)
            except ConnectionRefusedError as e:
                log.error("Connection could not be established with %s:%d: %s", host, port, e)
            except Exception as e:
                log.exception("Unexpected error occurred while attempting TCP connection with %s:%d", host, port)
    return success


def finger_printing(hosts: Dict[str, List[str]],
                    timeout: float) -> List[Dict[str, Any]]:
    fp_result = []
    for host, ports in hosts.items():
        banners = {}
        for port in ports:
            if port == 80:
                response = requests.head(f"http://{host}:80", timeout=timeout)
                try:
                    response.raise_for_status()
                    server_banner = response.headers.get("Server")
                    if not server_banner:
                        continue
                    server_banner = server_banner.strip()
                    banners[port] = server_banner
                except KeyError as e:
                    log.error("'Server' key does not exist: %s", e)
                except HTTPError as e:
                    log.error("HTTP error occurred: %s", e)
                    log.error("Status code: %d", response.status_code)
                except Exception:
                    log.exception("Unexpected error occurred during HTTP HEAD request")
            if port == 443:
                response = requests.head(f"https://{host}:443", timeout=timeout)
                try:
                    response.raise_for_status()
                    server_banner = response.headers.get("Server")
                    if not server_banner:
                        continue
                    server_banner = server_banner.strip()
                    banners[port] = server_banner
                except KeyError as e:
                    log.error("'Server' key does not exist: %s", e)
                except HTTPError as e:
                    log.error("HTTP error occurred: %s", e)
                    log.error("Status code: %d", response.status_code)
                except Exception:
                    log.exception("Unexpected error occurred during HTTPS HEAD request")
            # for SSH (port 22), open a raw TCP socket, send a newline, and read the banner
            if port == 22:
                with socket.create_connection((host, port), timeout=timeout) as s:
                    try:
                        s.send(b"\n")
                        response = s.recv(1024)  # bytes object
                        decode_resp = response.decode("utf-8").strip()
                        banners[port] = decode_resp
                    except ConnectionRefusedError as e:
                        log.error("Connection could not be established with %s:%d: %s",
                                  host, port, e)
                    except socket.timeout as e:
                        log.error("Socket timeout: %s", e)
                    except Exception:
                        log.exception("Unexpected error occurred during SSH communication")
        fp_result.append({"ip": host, "ports": ports, "banners": banners})
    return fp_result


def inline_list(match: Match[str]) -> str:
    # inner block
    inner = match.group(1).strip()
    # collapse all into single spaces
    collapsed = ' '.join(inner.split())
    return '[' + collapsed + ']'


def setup_logging(verbosity: int) -> None:
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG
    logging.basicConfig(level=level)


def main():
    parser = argparse.ArgumentParser(prog="port_scanner.py",
                                     description="used to 1) ICMP-sweep a subnet, " \
                                     "2) TCP-connect scan any unresponsive hosts, " \
                                     "3) 'Fingerprint' each service that responded to either one or both")
    parser.add_argument("-s", "--subnet", required=True, type=str,
                        help="Subnet to scan i.e. 127.0.0.1/24")
    parser.add_argument("-p", "--port", default="22,80,443", type=str,
                        help="Comma-separated ports used for TCP fallback: i.e. 22,80,443")
    parser.add_argument("-t", "--timeout", default=1.0, type=float,
                        help="Used to override default timeout value")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Set your own verbosity (use -v or for more detail i.e. -vv)")

    args = parser.parse_args()

    setup_logging(args.verbose)

    log.debug("Debugging is on")

    try:
        network = ipaddress.ip_network(args.subnet)
    except ValueError:
        parser.error(f"Invalid subnet: {args.subnet}")

    log.info("Scanning subnet: %s", network)
    ports = [int(p) for p in args.port.split(",")]
    final_hosts = {}

    icmp_alive, dead = ping_sweeper(network, args.timeout)
    log.info("Number of ICMP alive hosts: %d", len(icmp_alive))
    icmp_alive_tcp = tcp_fallback(icmp_alive, ports, args.timeout)
    log.info("Number of TCP-open ICMP hosts: %d", len(icmp_alive_tcp))
    icmp_info = {ip: [] for ip in icmp_alive}
    for host, ports in icmp_alive_tcp.items():
        icmp_info[host] = ports

    tcp_alive = tcp_fallback(dead, ports, args.timeout)
    log.info("Number of TCP-only alive hosts: %d", len(tcp_alive))
    final_hosts.update(icmp_info)
    final_hosts.update(tcp_alive)

    result = finger_printing(final_hosts, args.timeout)
    json_format = json.dumps(result, indent=2)

    pattern = re.compile(r'\[\s+([^\[\]]*?)\s+\]', re.DOTALL)
    pretty_format = pattern.sub(inline_list, json_format)
    print(pretty_format)


if __name__ == "__main__":
    main()
