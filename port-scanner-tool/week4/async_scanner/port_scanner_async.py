#ICMP sweep and TCP fallback with asynchronous I/O
import asyncio, aiohttp
import argparse
import logging
import ipaddress
import sys
import time
import json
from scapy.all import IP, ICMP, sr
from typing import Tuple, List, Dict, Optional

log = logging.getLogger(__name__)

def async_ping_sweep(subnet: str, timeout: float) -> Tuple[List[str], List[str]]:
    live_hosts, dead_hosts = [], []
    network = ipaddress.ip_network(subnet)
    try:
        batch_echo = IP(dst=str(network)) / ICMP()  # send packets as a batch to all IP addr on the network
        answered, unanswered = sr(batch_echo, timeout=timeout, verbose=False)
        for _, reply in answered:
            live_hosts.append(reply[IP].src)
        for pckt in unanswered:
            dead_hosts.append(pckt[IP].dst)
    except OSError as e:
        log.error("Socket error: %s", e)
        return [], []
    except Exception:
        log.exception("Unexpected error during ICMP sweep on %s", network)
        return [], []
    return live_hosts, dead_hosts


async def async_tcp_scan(host: str, port: int, timeout: float, sem: asyncio.Semaphore) -> Tuple[str, int, bool]:
    """Returns a dictionary of IP addr -> list of ports TCP connection = successful"""
    async with sem:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port),
                                                    timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return host, port, True
        except Exception:
            return host, port, False


async def async_finger_printing(host: str, port: int, timeout: float, sem: asyncio.Semaphore) -> Tuple[Optional[str], bool]:
    """Return , each containing relevant info to the finger printing service result"""
    async with sem:
        if port in (80,443):
            try:
                async with aiohttp.ClientSession() as sess:
                    prefix = "http" if port == 80 else "https"
                    async with sess.head(f"{prefix}://{host}:{port}") as resp:
                        banner = resp.headers.get("Server")
                        if resp:
                            return host, port, banner, True
                        else:
                            return host, port, banner, False
            except Exception:
                log.error("Port 80/443 finger printing error occurred")
                return None, False
        if port == 22:
            try:
                reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
                writer.write(b"\n")
                await writer.drain()
                resp = await reader.read(1024)
                banner = resp.decode("utf-8").strip()
                writer.close()
                await writer.wait_closed()
                return (host, port, banner, True) if banner else (host, port, None, False)
            except Exception:
                log.error("Port 22 finger printing error occurred")
                return host, port, None, False


async def async_gather_finger_print(hosts: Dict[str, List[int]], timeout: float, max_conc: int) -> List[Tuple[Optional[str], bool]]:
    sem = asyncio.Semaphore(max_conc)
    # Implement a "greedy" way of fingerprinting -> fingerprint hosts w/ most ports open first
    dict_list = hosts.items()
    host_port_list = sorted(dict_list, key=lambda pair:len(pair[1]), reverse=True)
    tasks = [asyncio.create_task(async_finger_printing(host, port, timeout, sem))
                                 for host, ports in host_port_list for port in ports]
    results = await asyncio.gather(*(tasks))
    return results


async def async_gather_tcp(hosts: List[str], ports: List[int], timeout: float, max_conc: int) -> List[Tuple[str, int, bool]]:
    #want to turn each host and port into a Task so that each can be scheduled
    sem = asyncio.Semaphore(max_conc)
    tasks = [asyncio.create_task(async_tcp_scan(host, port, timeout, sem))
                                 for host in hosts for port in ports]
    results = await asyncio.gather(*(tasks))  # list of return values for each Task ran
    return results


def setup_logging(verbosity: int) -> None:
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG
    logging.basicConfig(level=level)


async def main():
    start = time.perf_counter()
    parser = argparse.ArgumentParser(prog="port_scanner.py",
                                     description="used to 1) ICMP-sweep a subnet, " \
                                     "2) TCP-connect scan any unresponsive hosts, " \
                                     "3) 'Fingerprint' each service that responded to either one or both")
    parser.add_argument("-s", "--subnet", required=True, type=str,
                        help="Subnet to scan i.e. 127.0.0.1/24")
    parser.add_argument("-p", "--port", default="22,80,443", type=str,
                        help="Comma-separated ports used for TCP fallback: i.e. 22,80,443." \
                        "ONLY ports 22, 80, and 443 are supported as of now")
    parser.add_argument("-t", "--timeout", default=1.0, type=float,
                        help="Used to override default timeout value")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Set your own verbosity (use -v or for more detail i.e. -vv)")
    parser.add_argument("-c", "--concurrent", type=int, default=100,
                        help="Max number of tasks that can run at once (default = 100)")

    args = parser.parse_args()

    setup_logging(args.verbose)

    log.debug("Debugging is on")

    try:
        network = ipaddress.ip_network(args.subnet)
    except ValueError:
        parser.error(f"Invalid subnet: {args.subnet}")

    log.info("Scanning subnet: %s", network)
    ports = [int(p) for p in args.port.split(",")]
    # Find ICMP responders
    icmp_alive, dead = async_ping_sweep(network, args.timeout)
    log.info("Number of ICMP alive hosts: %d", len(icmp_alive))
    # See those that create successful TCP connection (on 'alive')
    icmp_alive_tcp = await asyncio.create_task(async_gather_tcp(icmp_alive, ports, args.timeout, args.concurrent))
    open_ports = {}
    for h,p,tf in icmp_alive_tcp:
        if tf:
            if h in open_ports:
                open_ports[h].append(p)
            else:
                open_ports[h] = [p]
    # See those that create successful TCP connection (on 'dead')
    tcp_only = await asyncio.create_task(async_gather_tcp(dead, ports, args.timeout, args.concurrent))
    for h,p,tf in tcp_only:
        count = count + 1 if tf else count
        if tf:
            if h in open_ports:
                open_ports[h].append(p)
            else:
                open_ports[h] = [p]

    fingerprint_result = await asyncio.create_task(async_gather_finger_print(open_ports,
                                                                             args.timeout,
                                                                             args.concurrent))
    banners = {}
    for h,p,b,tf in fingerprint_result:
        if tf:
            if h in banners:
                banners[h].append(b)
            else:
                banners[h] = [b]
    
    final_hosts = []
    for ip, ports in open_ports.items():
        final_hosts.append({"ip": ip, "open_ports": ports, "server_banners": banners.get(ip)})

    end = time.perf_counter() - start
    final = {
        "scanned_subnet": str(network),
        "hosts": final_hosts,
        "elapsed_time": round(end, 2)
    }
    fd = open("reports.json", 'w')
    json.dump(final, fd, indent=2)  # Print final result into json file


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(1)