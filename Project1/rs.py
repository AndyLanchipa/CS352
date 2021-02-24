import socket
import sys

class node:
    def __init__(self, host, IP, Flag):
        self.host = host
        self.IP = IP
        self.Flag = Flag
        self.next = None
class linked_list:
    def __init__(self):
        self.head = None



#populate linked list with DNS table
def populate_DNS():
    
    f = open('PROJI-DNSRS.txt' , 'r')
    byte = f.read(1)

    word = ""
    
    hostname = ""
    Ip = ""
    flag = ""
    DNSlist = linked_list()
    DNSlist.head  = None


    #disect words

    while True:
        byte = f.read(1)
        print("byte -> " + byte)
        word += byte
        if(byte == ''):
            break
          
        if(byte == " "):
             print("here ")

             if(hostname == ""):
                 hostname = word
                 word = ""
                 continue
             if(Ip == ""):
                 Ip = word
                 word = ""
                 continue
             if(flag == ""):
                 flag = word
                 word = ""
                 continue
        if(byte == "\n"):
            #make a new linked list node and reset the holding values

            if(flag == ""):
                flag = word
                word = ""

            if(DNSlist.head == None):
                #this means that the list is empty then we set the head of the list first
                DNSlist.head  = node(hostname,Ip,flag)
                temphead  = DNSlist.head
                #reset the values
                hostname = ""
                Ip = ""
                flag = ""
                continue
                
            
        
            temphead.next = node(hostname,Ip,flag)
            temphead =temphead.next #moving the pointer to the newly added node

            print(temphead.host + " " + temphead.IP + " " + temphead.Flag + "\n\n\n\n\n")
            #reset values 
            hostname = ""
            Ip = ""
            flag = ""

    return DNSlist #return DNS list 


            



     #searches for host name that was sent in by the client 
     # if it is found it send back a string of the host with hostname,ip,flag or hostname,NS if not found      
def searchDNS(self, name ):

    info = ""
    ptr = self.head
    while self.head is not None:

        if(ptr.host == name):
            #host is found now we make the string to return
            return info + ptr.host + " " + ptr.IP + " " + ptr.Flag 

        ptr =ptr.next #moving ptr to next val
 
    #if it goes out of the while loop the match isnt found 
    
    return name + " " + "-" + " " + "NS"




DNSList = linked_list()

DNSList.head = populate_DNS() #this will populate the linked list with all the dns things

print("list has been made - > " )






#creation of socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = int(sys.argv[1])

s.bind(('',port_number ))
DNSList = linked_list()

DNSList.head = populate_DNS #this will populate the linked list with all the dns things
s.listen(1)


print("waiting.....")


while True:
    print("here")
    clientsocket,address =  s.accept()
    while True:
        data = clientsocket.recv(200).decode
        Info = searchDNS(data) #returns string to send back to client 
        #sending back data to client
        clientsocket.send(Info.encode())
        break
    clientsocket.close()
