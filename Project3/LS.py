import binascii
import socket
import sys




port = int(sys.argv[1])

server_address = ('',port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(server_address)
sock.listen(1)

while True:
    while True:
        clientsocket,address = sock.accept()

        data = clientsocket.recv(10240).decode()
        if not data: 
            break

        #hash queries so that they go to the same server and the load is balanced equally and same queries go 
        #go to the same servers
        #this splits the load evenly
        temp = hash(data) % 2

        if temp % 2 == 0:
            #connecting server ls to ts2
            ts1port = int(sys.argv[3])
            ts1hostname = int(sys.argv[2])
            addy =(ts1hostname,ts1port)
            ts1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ts1socket.connect()


            




        elif temp % 2 == 1:

           #connecting server ls to ts2
            ts2port = int(sys.argv[5])
            ts2hostname = int(sys.argv[4])
            addy =(ts2hostname,ts2port)
            ts2socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            ts2socket.connect()
