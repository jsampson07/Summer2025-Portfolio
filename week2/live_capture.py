from scapy.all import IP, TCP, UDP, DNS, DNSQR, DNSRR, Raw, sniff, sr1, load_layer, conf
load_layer("tls")
from scapy.layers.tls.handshake import TLSClientHello
import pprint


def resolve_sniff():
    #i want to look at DNS lookups, TCP handhsakes and HTTPS request (443)
    #Resolve target hostname
    
    resolved = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="www.youtube.com"))
    resp = sr1(resolved, timeout=5)
    resolved_ips = []
    if resp and resp.haslayer(DNS) and resp[DNS].ancount > 0:
        for rr in resp[DNS].an:
            if rr.type == 1: #1 for A type (IPv4), 5 for CNAME type (encoded domain name), 23 for AAAA type (IPv6)
                resolved_ips.append(rr.rdata)
        print(resolved_ips)
    host_names = " or ".join(f"host {ip}" for ip in resolved_ips)
    bpf_filter = f"({host_names}) and (tcp port 80 or tcp port 443 or udp port 53)"
    print(f"We are using the filter: {bpf_filter}") #just make sure that it formats correctly
    sniff(filter=bpf_filter, iface=conf.iface, store=False, prn=process_pckt)

def process_pckt(pckt):
    ip_src, ip_dst = (None, None)
    sport, dport = (None, None)
    if pckt.haslayer(IP):
        ip_src, ip_dst = pckt[IP].src, pckt[IP].dst #IP header info
    else:
        return
    if pckt.haslayer(TCP):
        sport, dport = pckt[TCP].sport, pckt[TCP].dport #TCP header info
    elif pckt.haslayer(UDP):
        sport, dport = pckt[UDP].sport, pckt[UDP].dport #UDP header info
    else:
        sport, dport = None, None


    if pckt.haslayer(TCP):
        flags = pckt[TCP].flags
        # Scapy prints flags as a string, e.g. 'S' for SYN, 'SA' for SYN+ACK, 'A' for ACK
        if flags == 'S':
            print(f"[SYN]    {ip_src}:{sport} → {ip_dst}:{dport}")
        elif flags == 'SA':
            print(f"[SYN+ACK]{ip_src}:{sport} → {ip_dst}:{dport}")
        elif flags == 'A':
            print(f"[ACK]    {ip_src}:{sport} → {ip_dst}:{dport}")
    
    #this is if the packet was talking over TCP and had raw bytes sent with it
    if pckt.haslayer(Raw) and pckt.haslayer(TCP):
        data = pckt[Raw].load
        #if it was talking over HTTP
        if dport == 80:
            if data.startswith(b"GET ") or data.startswith(b"POST "):
                #get GET request or POST request line
                line = data.split(b"\r\n", 1)[0].decode(errors="ignore")
                print(f"HTTP REQUEST: {ip_src}:{sport} is taklking with {ip_dst}:{dport} and said: {line}")
    if pckt.haslayer(Raw) and pckt.haslayer(TCP):
        #elif dport == 443:
        data = pckt[Raw].load
        if dport == 443:
            if data.startswith(b"\x16\x03") and pckt.haslayer(TLSClientHello):
                #get the SNI field
                server_names = pckt[TLSClientHello].extensions.servernames
                names_list = []
                for type, names in server_names:
                    if type == 0:
                        names_list.append(names)
                print(f"TLS INFO: {ip_src}:{sport} is taklking with {ip_dst}:{dport} and there was a TLS ClientHello exchange")
                print(f"These happened with the following server names:\n{names_list}")
    if pckt.haslayer(UDP) and pckt.haslayer(DNS):
        dns_info = pckt[DNS]
        if dport == 53 and dns_info.qd:
            dname = dns_info.qd.qname.decode(errors="ignore")
            rcode = dns_info.rcode #why not .an.rcode???? ==> LOOK AT A DNS RECORD OUTPUT
            print(f"Domain being queried is: {dname} and RCODE is: {rcode}")

    if pckt.haslayer(UDP) and (sport == 443 or dport == 443):
        if pckt.haslayer(Raw):
            length = len(pckt[Raw].load)
        else:
            length = 0
        print(f"QUIC {ip_src}:{sport} → {ip_dst}:{dport}  {length} bytes")

def main():
    """
    bpf = "port 53 or port 80 or port 443"
    i_face = conf.iface
    sniff(filter=bpf, iface=i_face, store=False, prn=process_pckt)
    """
    resolve_sniff()


if __name__ == "__main__":
    main()