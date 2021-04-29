import binascii
import socket
import sys
import select




port = int(sys.argv[1])

server_address = ('',port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(server_address)
sock.listen(1)

ts1port = int(sys.argv[3])
ts1hostname = sys.argv[2]
addy =(ts1hostname,ts1port)
ts1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts1socket.connect(addy)




ts1counter  = 0
ts2counter =0

#connecting server ls to ts2
ts2port = int(sys.argv[5])
ts2hostname = sys.argv[4]
addy2 =(ts2hostname,ts2port)
ts2socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ts2socket.connect(addy2)


while True:
    clientsocket,address = sock.accept()
    while True:
        data = clientsocket.recv(10240).decode()
        if not data: 
            break

        #hash queries so that they go to the same server and the load is balanced equally and same queries go 
        #go to the same servers
        #this splits the load evenly
        temp = hash(data)
        

        if temp % 2 == 0:
            

            print("hash function setting load to TS1 hash was even")
          


            #case 1: LS recieves response in the timeout window TS1

            #assuming successful connection we should send the host name to the server ts1
            #we connected to ts1 so we send the host name we got from the server and wait for a response

            ts1socket.sendall(data.encode('utf-8'))

            #i think this sets up the time out https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
            #ts1socket.setblocking(0)

            #timeout = select.select([ts1socket],[],[],5)
            ts1socket.settimeout(5)

            try:
                ts1counter+=1
                print("TS1 did not time out and ls is recieving data")
                servermessage = ts1socket.recv(10240).decode('utf-8')
                #we recieve the host name with the ip from ts now we want to send it back to client

                clientsocket.sendall(servermessage.encode('utf-8'))
            except socket.timeout:
                #case 2: LS doesnt recieve response in timeout window and goes to TS2 for query
                #TS1 does not respond in time so we try ts2
               
                print("TS1 failed to recieve feedback in time and now we will send the job over to TS2")
                ts2socket.sendall(data.encode('utf-8'))
                ts2socket.settimeout(5)
                
                try:
                    ts2counter+=1
                    print("TS2 did not timeout and ls is now recieving the data from TS2")
                    servermessage = ts2socket.recv(10240).decode('utf-8')
                    clientsocket.sendall(servermessage.encode('utf-8'))
                except socket.timeout:
                    #case 3:LS doesnt recieve response from any ts1 or ts2 so it sends erros back to client
                    #both ts1 and ts2 time out
                   
                    print("both TS1 and TS2 time out sending back error host not found to client")
                    servermessage = data +" - Error:HOST NOT FOUND"
                    clientsocket.sendall(servermessage.encode('utf-8'))
        
        elif temp % 2 == 1:
            print("sending load to TS2 because of hash was odd")

            ts2socket.sendall(data.encode('utf-8'))
            ts2socket.settimeout(5)
            

            try:
                ts2counter+=1
                print("TS2 did not time out and LS is now recieving")
                servermessage = ts2socket.recv(10240).decode('utf-8')
                clientsocket.sendall(servermessage.encode('utf-8'))
            except socket.timeout: 
                print("TS2 failed to send back before time out and now we are using TS1 to send data")
                ts1socket.sendall(data.encode('utf-8'))
                ts1socket.settimeout(5)

                try:
                    ts1counter+=1
                    print("TS1 sent back info before timeout so it ls recieves data")
                    servermessage = ts1socket.recv(10240).decode('utf-8')
                    clientsocket.sendall(servermessage.encode('utf-8'))
                except socket.timeout: #case 3 neither responded to LS
                    print("both TS1 and TS2 timedout")
                    servermessage = data + " - Error:HOST NOT FOUND"
                    clientsocket.sendall(servermessage.encode('utf-8'))

    print( ts1counter)
    print(ts2counter)
    clientsocket.close()

             

           
            
