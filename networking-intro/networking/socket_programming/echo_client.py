import socket

def echo_client():
    HOST = "127.0.0.1" #servers IP addr
    PORT = 65432 #servers port # used
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(b"Hello, World")
        data = s.recv(1024)
    print(f"Received the echoed data: {data}")

if __name__ == "__main__":
    echo_client()