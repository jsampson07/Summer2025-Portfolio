from scapy.all import IP, TCP, Raw, sr, sr1, sniff, send, AsyncSniffer
import pprint
import netifaces

def banner_grabber():
    my_network = "127.0.0.1"
    for port in [22, 8000, 443]:
        syn_pckt = IP(dst=my_network) / TCP(dport=port, flags="S")
        sa_resp = sr1(syn_pckt, timeout=2)
        if not sa_resp or sa_resp[TCP].flags & 0x12 != 0x12:
            print(f"Port {port} closed or filtered; skipping")
            continue
        seq = sa_resp[TCP].ack
        ack = sa_resp[TCP].seq + 1
        a_pckt = IP(dst=my_network) / TCP(dport=port, flags="A", seq=seq, ack=ack)
    
        #sniffer = AsyncSniffer(filter=f"tcp and src host {my_network} and src port {port}", iface="lo", count=1)
        #sniffer.start()
        #send(a_pckt)
        #banner_req = sr1(IP(dst=my_network) / TCP(dport=port, seq=seq, ack=ack), timeout=2)
        
        banner_req = sr1(a_pckt, timeout=2)
        #pckts = sniffer.join(timeout=5)
        """ PAIRED WITH sniffer - pckts CODE
        if pckts:
            packet = pckts[0]
            if packet.haslayer(Raw):
                print("OH MY GOD WE DID IT !!!!!!")
            if packet[TCP].payload:
                print("WE ALSO DID IT!")
        """
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