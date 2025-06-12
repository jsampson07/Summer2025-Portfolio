from scapy.all import wrpcap, rdpcap, sr, send, srp, sr1, ICMP, IP, TCP, UDP, DNS, Raw, Ether, sniff, DNSQR
import pprint

def main():
    create_connection()
    srp_test()

def create_connection():
    syn = TCP(dport=80, flags="S") #used to make a SYN request
    total_packet = IP(dst="23.0.162.200") / syn
    total_packet.show()
    talk = sr1(IP(dst="23.0.162.200") / syn)
    #talk.show()
    #print(talk[TCP].flags)

    ack_num = talk[TCP].seq + 1 #we need this bc in order to finish three-way handshake...
        #we need to send packet back with SEQ+1 and A flag
    seq_num = talk[TCP].ack
    sport_mine = talk[TCP].dport #same as syn.sport in above code when its still "my" packet
    #confirmed it responded with a SYN-ACK, now... craft ACK packet to send back to server
    ack_pckt= IP(dst="23.0.162.200") / TCP(sport=sport_mine, seq=ack_num, dport=80, ack=seq_num, flags="A")
    list_packets = [total_packet, talk, ack_pckt]
    wrpcap("test.pcap", list_packets)
    pcap_contents = ("test.pcap")
    talk = send(ack_pckt)

    #sniff(filter=f"tcp and src host 23.0.162.200 and port 80", count=1) ==> used to check handshake=complete


    #p = sr1(IP(dst = "8.8.8.8") / UDP() / DNS())
        #here src is autofilled w/ my machines IP address
            #dst is to specify where to deliver the UDP packet that contains the DNS query
                #AND identifies WHICH recursive DNS server we are asking to do the "name-resolution" resolving
        #UDP sport is random (from my pc)m dport = 53 for DNS protocol
            #dport indicates what kind of service
        #DNS autofills with "www.example.com" for "question"
            #DNS asks ==> "please resolve www.example.com into an IPv4 address"

    #pprint.pp(p[DNS].show()) #answer from the query???

    #tcp = TCP(dport=80) #HTTP connection

    #packet_to_send = sr1(IP(dst="8.8.4.4")/UDP()/DNS(), timeout=2)
    #pprint.pp(packet_to_send[DNS].an) #answer from the query???

    #right now this hangs because:
    """
    1. Layer-2 transmission NEEDS a dest MAC (sr1() is the thing that transmits)
    2. ARP request times out as a result (when ARP lookup) and then broadbasts the msg
        --> unlikely anyone on my network will answer
    """
def resolved_name(): # for specific
    packet = IP(dst="8.8.8.8") / UDP(dport=53) / DNS()
    response = sr1(packet)
    response.show()

def srp_test():
    #ans, unans = srp(Ether() / IP(dst="8.8.8.8", ttl=(5,10)) / UDP() / DNS())
    #pprint.pp(ans.show())

    ans, unans = sr(IP(dst="8.8.8.8", ttl=(5,10))/UDP(dport=33434), timeout=3, verbose=False)
   #pprint.pp(ans[0])
    pcap_test(ans)

def pcap_test(ans):
    wrpcap("scapy.pcap", ans) #write packets to a pcap file but here we have a list of tuples
        #so it iterates the list, sees tuples (another iterable type), iterates through that and sees Packet objects and gets its raw bytes
            #and writes to pcap file (pcap stored in bytes)
    test_pcap = rdpcap("scapy.pcap") #when we read the contents we get this back
    for packet in test_pcap: #for each packet in the test_pcap
        pprint.pp(packet)  




if __name__ == "__main__":
    main()