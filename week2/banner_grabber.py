from scapy.all import IP, TCP, Raw, sr, sr1, sniff, send, AsyncSniffer, RandShort
import pprint
import netifaces

def banner_grabber():
    my_network = "scanme.nmap.org"
    for port in [22, 80, 443]:
        my_sport = RandShort()
        syn_pckt = IP(dst=my_network) / TCP(sport=my_sport, dport=port, flags="S")
        print(syn_pckt[TCP].sport)
        syn_ack = sr1(syn_pckt, timeout=2)
        if not syn_ack or syn_ack[TCP].flags & 0x12 != 0x12:
            print(f"Port {port} closed or filtered; skipping")
            continue
        sequence = syn_ack[TCP].ack
        ackn = syn_ack[TCP].seq + 1
        client_port = syn_ack[TCP].dport # we need this bc Scapy will picks a new random source port for each request if not specified
        print(client_port)
        a_pckt = IP(dst=my_network) / TCP(sport=my_sport, dport=port, flags="A", seq=sequence, ack=ackn)
        
        banner_req = sr1(a_pckt, timeout=5)
        if banner_req:
            print(f"Port {port}, Banner: {banner_req}")
        else:
            print("There is no banner")
        if banner_req.haslayer(Raw):
            print("WE HAVE IT!!!!")
        if banner_req[TCP].payload:
            print("WE HAVE A PAYLOAD!!!!!!!!")

        #ans, unans = sr(a_pckt, timeout=2)
        #for send, rec in ans:
            #if rec.haslayer(Raw):
                #print("YES!")

if __name__ == "__main__":
    banner_grabber()