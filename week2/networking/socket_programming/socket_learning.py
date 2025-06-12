import socket
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
    print(sock)


if __name__ == "__main__":
    main()
