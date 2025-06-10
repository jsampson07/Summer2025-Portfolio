from scapy.all import *
load_layer("tls")
from scapy.layers.tls.handshake import TLSClientHello
import pprint

def main():
    #i want to look at DNS lookups, TCP handhsakes and HTTPS request (443)
    #Resolve target hostname
    resolved = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="www.youtube.com"))
    resp = sr1(resolved)
    resolved_ips = []
    if resp and resp.haslayer(DNS) and resp[DNS].ancount > 0:
        for ans in resp[DNS].an:
            if ans.type == 1: #1 for A type (IPv4), 5 for CNAME type (encoded domain name), 23 for AAAA type (IPv6)
                resolved_ips.append(ans.rdata)
        print(resolved_ips)
    bpf_filter = f"(host {resolved_ips[0]} or host {resolved_ips[1]} or host {resolved_ips[3]}) and (tcp port 80 or tcp port 443 or udp port 53)"
    process_pckt(resp)
    sniff(filter=bpf_filter, iface="eth0", store=False, prn=process_pckt)

def process_pckt(pckt):
    ip_src, ip_dst = (None, None)
    sport, dport = (None, None)
    if pckt.haslayer(IP):
        ip_src, ip_dst = pckt[IP].src, pckt[IP].dst #IP header info
    if pckt.haslayer(TCP):
        sport, dport = pckt[TCP].sport, pckt[TCP].dport #TCP header info
    #this is if the packet was talking over TCP and had raw bytes sent with it
    if pckt.haslayer(Raw) and pckt.haslayer(TCP):
        data = pckt[Raw].load
        #if it was talking over HTTP
        if dport == 80:
            if data.startswith(b"GET ") or data.startswith(b"POST "):
                #get GET request or POST request line
                line = data.split(b"\r\n", 1)[0].decode()
                print(f"{ip_src}:{sport} is taklking with {ip_dst}:{dport} and said: {line}")
        if dport == 443:
            if data.startswith(b"\x16\x03"):
                #get the SNI field
                server_names = pckt[TLSClientHello].extensions.servernames
                names_list = []
                for type, names in server_names:
                    if type == 0:
                        names_list.append(names)
                print(f"{ip_src}:{sport} is taklking with {ip_dst}:{dport} and there was a TLS ClientHello exchange")
                print(f"These happened with the following server names:\n{names_list}")
    if pckt.haslayer(UDP):
        dns_info = pckt[DNS]
        if dport == 53:
            dname = dns_info.qd.qname
            rcode = dns_info.an.rcode
            print(f"Domain being queried is: {dname} and RCODE is: {rcode}")

        



if __name__ == "__main__":
    main()