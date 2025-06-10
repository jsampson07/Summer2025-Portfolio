#This is a mini lab task to get accustomed to and build on intro Scapy knowledge
from scapy.all import IP, ICMP, TCP, UDP, DNS, DNSQR, Raw, sr, srp, sr1, sniff, send, sendp, wrpcap, rdpcap
import pprint
import time

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

    another_host = IP(dst="1.1.1.1") / ICMP()
    another_reply = sr1(another_host, timeout=1)
    if another_reply is None:
        print("There is no host listening on this server")
        exit()
    another_reply.show()




    #Part 2: Port Probing
    #first need to find out the IP of the web server
    #AUTOMATICALLY RESOLVES HOSTNAME FOR ME UNDER THE HOOD IN **SCAPY**
    packet = IP(dst="scanme.nmap.org") / TCP(dport=80)
    response = sr1(packet, timeout=1)
    response.show()


    target = "127.0.0.1"
    #I want to probe the known open port (I opened in separate terminal: nc -l 2222)
    open_packet = IP(dst=target) / TCP(dport=2222, flags="S")
    response_open = sr1(open_packet, timeout=1)
    print(f"Open port response flag: {response_open[TCP].flags}")

    #I want to probe a known closed port (BUT to an IP that is known to be reachable)
    closed_packet = IP(dst=target) / TCP(dport=3333, flags="S")
    closed_response = sr1(closed_packet, timeout=1)
    print(f"Closed port response flag: {closed_response[TCP].flags}")

    #Now I want to send a packet to this open port on my network
    """FIRST I WANT TO ESTABLISH A TCP CONNECTION (3-way handshake)"""
    #send SYN packet to server
    syn = IP(dst=target) / TCP(dport=2222, flags="S")
    syn_ack_resp = sr1(syn, timeout=1)
    if syn_ack_resp is None:
        raise RuntimeError("No listener at endpoint. Make sure they are listening!")
    #send back ACK packet to server
    seq_for_resp = syn_ack_resp[TCP].ack
    ack_for_resp = syn_ack_resp[TCP].seq + 1
    ack = IP(dst=target) / TCP(dport=2222, flags="A", seq=seq_for_resp, ack=ack_for_resp)
    send(ack) #no response is expected

    time.sleep(1)

    #Now I can send the payload to the server that I have now established a connection with
    payload = Raw(load="Hello World!")
    send_packet = IP(dst=target) / TCP(dport=2222, flags="PA", seq=ack[TCP].seq, ack=ack[TCP].ack) / payload
    send(send_packet)

    #try sending a packet over UDP
        #this works because UDP does not maintain connection state so raw packets will show
        #On the contrary:
            #TCP does maintain connection state, and from kernel's POV, NO VALID TCP session ever established on listening socket
                #"listening" socket that I started stays in "listening" state because handshake was never accepted by kernel's TCP SM
    packet_to_send = IP(dst=target) / UDP(dport=2222) / Raw(load="Hello World!\n")
    send(packet_to_send)

    udp_packet = IP(dst=target) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="notahost.example.invalid", 
                                                                  qtype=103))
        #this packet forces the server to either:
            #1) reply with a DNS formatted error
            #2) Send ICMP "port unreachable" if rejects at UDP layer
                #point to valid endpoint (IP) where port is really closed
            #3) Nothing if firewall drops packets
    reply = sr1(udp_packet)
    reply.show()


    #Part 3: Passive Sniffing
        #this is how you eavesdrop on a network and all communications on the network
    sniffed = sniff(count=100) #sniff returnns a Packet List

    #OR TO WRITE TO PCAP FILE FOR WIRESHARK LATER
    wrpcap("mini_lab.pcap", sniffed)
    pcap_file = rdpcap("mini_lab.pcap")
    #print(pcap_file)
    #for packets in sniffed:
        #packets.show()
    #sniffed.summary()
    

if __name__ == "__main__":
    main()