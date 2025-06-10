#This is a mini lab task to get accustomed to and build on intro Scapy knowledge
from scapy.all import IP, ICMP, TCP, UDP, DNS, sr, srp, sr1, sniff
import pprint

def main():
    #This is the script that I am creating

    #Part 1: Host Reachability
        #to check host reachability --> use ICMP
            #ICMP is used for ping and traceroute commands
                #==> sends ECHO request packets to target device(s), if device = reachable ==> echo reply
    ping_pckt = IP(dst="8.8.8.8") / ICMP()
    reply = sr1(ping_pckt, timeout=1) #want to use sr1 because I am sending request and getting reply
    #if want to dump all of a packets fields then call .show() on the Packet Object
    if reply is None:
        print("There is no host listening on this server")
        exit()
    reply.show()

    #Part 2: Port Probing
    #first need to find out the IP of the web server
    packet = IP(dst="scanme.nmap.org") / UDP(dport=53) / DNS()
    response = sr1(packet)
    dest_ip = response[IP].src
    print(dest_ip)
    packet = IP(dst=dest_ip) / TCP(dport=80)
    response = sr1(packet, timeout=1)
    response.show()
    
    #print("SPACING LINE\n\n\n\n\n")
    """ AUTOMATICALLY RESOLVES HOSTNAME FOR ME UNDER THE HOOD IN **SCAPY**
    packet = IP(dst="scanme.nmap.org") / TCP(dport=80)
    response = sr1(packet, timeout=1)
    response.show()
    """

    #Part 3: Passive Sniffing
        #this is how you eavesdrop on a network and all communications on the network
    sniffed = sniff(count=10) #sniff returnns a Packet List
    #for packets in sniffed:
     #   packets.show()
    sniffed.summary()
    

if __name__ == "__main__":
    main()