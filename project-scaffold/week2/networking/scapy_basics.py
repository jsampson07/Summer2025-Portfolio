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