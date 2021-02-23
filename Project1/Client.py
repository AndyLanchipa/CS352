from sys import argv
import socket

#creating a two sockets one for rs and one for TS

try:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("client created the socket")
except socket.error as err:
    print("socket error: ")
    exit()
server_addr = (argv[1],argv[2]) #connect to rs listen port since we have the host name and port number
client_sock.connect(server_addr)

message = input(" -> ")

Disconnect = False #this will be true once we send a disconnect message to other sockets

while message:
    print("here")
    response = client_sock.recv(512)
    response = response.decode('utf-8')
    lastChar = response[-1]

    if lastChar == "A":
        response = response[:-1]
        for line in response:
            words = line.split(" ")
            print(words)
    #else:

