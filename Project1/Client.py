from sys import argv
import socket
import argparse
import sys

#creating a two sockets one for rs and one for TS

#argparse package to parse the arguments
#parser = argparse.ArgumentParser(description="""This i s a client program to interact with two servers""")
#parser.add_argument('rsHostname', type=str, help='This is the domain name or ip address of the server', action='store')
#parser.add_argument('rsListenPort', type=int, help='This is the port to connect to the rs server', action='store')
#parser.add_argument('rsListenPort', type=int, help='This is the port to connect to the ts server', action='store')
#args = parser.parse_args(argv[1:])

rsHostname = socket.gethostbyname(argv[1])
print(rsHostname)
rsListenPort = 0
tsListenPort = 0

servers = []
#print(argv)
modArg = argv[2:]
for ports in modArg:
    ports = int(ports)
    host = (rsHostname, ports) 
    print(host)

    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("I get here")
        client_sock.connect(host)            #binding port needs to be >=100
        print("I do get here")
        client_sock.listen(4)
        servers.append(client_sock)
        print("Client created the socket")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

# rsHostname = socket.gethostbyname(argv[1])
# rsListenPort = int(argv[2])
# tsListenPort = int(argv[3])
# print(rsHostname)
# print(rsListenPort)
# rsServer_addr = (rsHostname, rsListenPort) #connect to rs listen port since we have the host name and port number
# print(rsServer_addr)
# client_sock.connect(rsServer_addr)

Disconnect = False #this will be true once we send a disconnect message to other sockets

while True:
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

