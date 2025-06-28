from scapy.all import IP, ICMP, sr
import netifaces
import ipaddress

#ICMP sweep across a /24 network
#Print the live hosts

def ping_sweeper():
    interfaces = netifaces.interfaces()
    fin_interface = None
    for inter in interfaces:
        if inter == 'eth0':
            fin_interface = inter
            break
    # If we didn't find our target interface, fail early
    if fin_interface is None:
        raise RuntimeError("No valid eth0 interface")
    # Retrieve all configured IPv4 addresses and their netmasks for our chosen interface so we can calculate each local IPv4 subnet for sweeping
    my_networks = netifaces.ifaddresses(fin_interface)[netifaces.AF_INET]
    list_of_networks = []
    for network in my_networks:
        addr, netmask = network["addr"], network["netmask"]
        list_of_networks.append((addr, netmask))
    for addr, nmask in list_of_networks:
        network_iface = ipaddress.IPv4Interface(f"{addr}/{nmask}") # IPv4Network object
        network_iface = network_iface.network # Get the network IP address which we can use in our ICMP message
        print(f"We are scanning: {network_iface}")
        echo_message = IP(dst=str(network_iface)) / ICMP()
        ans, unans = sr(echo_message, timeout=1, verbose=False)
        for send, reply in ans:
            print(f"Echo reply from host: {reply[IP].src}")

def main():
    ping_sweeper()

if __name__ == "__main__":
    main()