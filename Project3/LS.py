import binascii
import socket
import sys
import select




port = int(sys.argv[1])

server_address = ('',port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(server_address)
sock.listen(1)


 #connecting server ls to ts2

ts1port = int(sys.argv[3])
ts1hostname = int(sys.argv[2])
addy =(ts1hostname,ts1port)
ts1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts1socket.connect()






#connecting server ls to ts2
ts2port = int(sys.argv[5])
ts2hostname = int(sys.argv[4])
addy =(ts2hostname,ts2port)
ts2socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ts2socket.connect()

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
          


            #case 1: LS recieves response in the timeout window TS1

            #assuming successful connection we should send the host name to the server ts1
            #we connected to ts1 so we send the host name we got from the server and wait for a response

            ts1socket.sendall(data.encode('utf-8'))

            #i think this sets up the time out https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
            ts1socket.setblocking(0)

            timeout = select.select([ts1socket],[],[],5)

            if timeout[0]:
                servermessage = ts1socket.recv(10240).decode('utf-8')
                #we recieve the host name with the ip from ts now we want to send it back to client

                clientsocket.sendall(servermessage.encode('utf-8'))
            else:#case 2: LS doesnt recieve response in timeout window and goes to TS2 for query
                #TS1 does not respond in time so we try ts2
                ts2socket.sendall(data.encode('utf-8'))
                ts2socket.setblocking(0)
                timeout = select.select([ts2socket],[],[],5)

                if timeout[0]:
                    servermessage = ts2socket.recv(10240).decode('utf-8')
                    clientsocket.sendall(servermessage.encode('utf-8'))
                else: #case 3:LS doesnt recieve response from any ts1 or ts2 so it sends erros back to client
                    #both ts1 and ts2 time out
                    servermessage = data +" - Error:HOST NOT FOUND"
                    clientsocket.sendall(servermessage.encode('utf-8'))



            





        elif temp % 2 == 1:

            ts2socket.sendall(data.encode('utf-8'))
            ts2socket.setblocking(0)
            timeout = select.select([ts2socket],[],[],5)

            if timeout[0]:
                servermessage = ts2socket.recv(10240).decode('utf-8')
                clientsocket.sendall(servermessage.encode('utf-8'))
            else: 
                ts1socket.sendall(data.encode('utf-8'))
                ts1socket.setblocking(0)
                timeout = select.select([ts2socket],[],[],5)

                if timeout[0]:
                    servermessage = ts1socket.recv(10240).decode('utf-8')
                    clientsocket.sendall(servermessage.encode('utf-8'))
                else: #case 3 neither responded to LS
                    servermessage = data + " - Error:HOST NOT FOUND"
                    clientsocket.sendall(servermessage.encode('utf-8'))



             

           
            
