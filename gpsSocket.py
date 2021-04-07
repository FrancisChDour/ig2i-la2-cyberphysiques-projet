import socket

def main():
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    print(socket.gethostname())
    serversocket.bind((socket.gethostname(), 8080))
    # become a server socket
    serversocket.listen(5)

main()
