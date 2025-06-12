from scapy.all import IP, TCP, Raw, sr, sr1, sniff, send
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
        banner_req = sr1(a_pckt, timeout=2)
        if banner_req:
            print(f"Port {port}, Banner: {banner_req}")
        else:
            print("There is no banner")
        if banner_req.haslayer(Raw):
            print("WE HAVE IT!!!!")
        if banner_req[TCP].payload:
            print("WE HAVE A PAYLOAD!!!!!!!!")
        """
        pckt = sniff(count=1, filter=f"tcp and src host {my_network} and src port {port}", timeout=2)
        for p in pckt:
            if p.haslayer(Raw):
                print(p[Raw].load)
        """
        #ans, unans = sr(a_pckt, timeout=2)
        #for send, rec in ans:
            #if rec.haslayer(Raw):
                #print("YES!")

if __name__ == "__main__":
    banner_grabber()