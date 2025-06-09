from scapy.all import sr1, ICMP, IP, TCP, sniff

def main():
    result = sniff(count = 10)
    print(result)

if __name__ == "__main__":
    main()