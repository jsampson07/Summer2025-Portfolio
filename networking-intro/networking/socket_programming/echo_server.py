import socket

def echo_server():
    HOST = "127.0.0.1"
    PORT = 65432 #this is the port to listen on (server-side)
    #what does with do??
        #enters the runtime context related to the object
        #exits the runtime context related to the object when execution is done (w/in the with statements)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #using "with" means no need to call close() @ the end
        s.bind((HOST, PORT)) #associate the socket created with a specific network iface and port # to make socket even usable
        s.listen()
        conn, addr = s.accept() #accept a conncetion from a client
            #returns a new socket obj ("CONN") which is now used to communicate with the client
        with conn: #because conn is a new socket obj, use with to auto close the socket when at the end of the with block
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data: #no data was received (no more data to receive)
                    break
                conn.sendall(data) #send all the data back to the client


if __name__ == "__main__":
    echo_server()