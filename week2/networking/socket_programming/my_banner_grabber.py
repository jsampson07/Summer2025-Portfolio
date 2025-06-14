import socket
import ssl

def banner_grabber():
    #- `banner_grabber.py` (TCP SYN+ACK to ports [22,80,443], print first bytes of response)
    HOST = "127.0.0.1"
    for port in [22, 8000, 443]:
        try:
            with socket.create_connection((HOST, port)) as s: #makes me "my" client-side socket
                s.settimeout(3) #set timeout for all recv and send calls to 3 seconds
                if port == 443:
                    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                    context.load_verify_locations(cafile="../../../cert.pem")
                    with context.wrap_socket(s, server_hostname=HOST) as w_sock:
                        #must send a valid request to get a response from HTTPS too !!!
                        request = w_sock.sendall(b"GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n")
                        #Here: -www handler when starting openssl s_server is extrememly minimal and only responds to GET requests in this case
                        tls_banner = w_sock.recv(1024)
                        if tls_banner:
                            final_banner = tls_banner.decode("utf-8").strip()
                            print(f"++ {HOST}:{port} -> {final_banner}")
                            continue
                        else:
                            print(f"-- There was no banner sent from Host: {HOST}, Port: {port}")
                            continue
                #because HTTP servers do NOT send data until send a valid req...
                elif port == 8000:
                    request = s.sendall(b"HEAD / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n")
                banner = s.recv(1024)
                if banner:
                    final_banner = banner.decode("utf-8").strip()
                    """ JUST FOR FUN to see output all on "one" line
                    final_text = banner.decode("utf-8").strip().split("\n")
                    new_str = []
                    for part in final_text:
                        new_str.append(part.strip())
                    final_text = " ".join(new_str)
                    """
                    print(f"++ {HOST}:{port} -> {final_banner}")
                else:
                    print(f"-- There was no banner sent from Host: {HOST}, Port: {port}")
        except (socket.timeout, ConnectionRefusedError):
            print(f"{HOST}:{port} is closed or unreachable")
        except Exception as e:
            print(f"{HOST}:{port} → error: {e}")

if __name__ == "__main__":
    banner_grabber()