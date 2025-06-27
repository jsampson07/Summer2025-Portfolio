from scapy.all import IP, ICMP, sr
import netifaces
import ipaddress

#ICMP sweep across a /24 network
#Print the live hosts

def ping_sweeper():
    #get some /24 network - NOTE: under the hood, scapy will see the "/24" and generate every address in that block and perform some action
    #Get the interface name
    interfaces = netifaces.interfaces()
    fin_interface = None
    for inter in interfaces:
        if inter == 'eth0':
            fin_interface = inter
            break
    #Get the interfaces relevant IPv4 block and get the mask as well
        #this is to derive the IP address that is relevant to us
    if fin_interface is None:
        raise RuntimeError("No valid eth0 interface")
    print(fin_interface)
    #echo_pckt = IP(dst="")
    my_networks = netifaces.ifaddresses(fin_interface)[netifaces.AF_INET]
    list_of_networks = []
    for network in my_networks:
        addr, netmask = network["addr"], network["netmask"]
        list_of_networks.append((addr, netmask))
    for add, nmask in list_of_networks:
        network_iface = ipaddress.IPv4Interface(f"{add}/{nmask}") #IPv4Network object
        network_iface = network_iface.network #this gets the network IP address which can now be used w/ ICMP
        print(f"We are scanning: {network_iface}")
        echo_message = IP(dst=str(network_iface)) / ICMP() #must cast the IP address w/ type IPv4Network to a str
        ans, unans = sr(echo_message, timeout=1, verbose=False)
        for send, reply in ans:
            print(f"Echo reply from host: {reply[IP].src}")

def main():
    ping_sweeper()

if __name__ == "__main__":
    main()