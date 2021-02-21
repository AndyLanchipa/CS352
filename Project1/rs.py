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
        self.head = node()



#populate linked list with DNS table
def populate_DNS():
    f = open('PROJI-DNSRS.txt , r')
    byte = f.read(1)

    word = ""
    
    hostname = ""
    Ip = ""
    flag = ""
    DNSlist = linked_list()
    DNSlist.head  = None


    #disect words

    while True:
        word += byte
        if(byte == ''):
            break;
     
        if(byte == " "):

             if(hostname == ""):
                 hostname = word
                 word = "";
                 continue
             if(ip == ""):
                 ip = word;
                 word = "";
                 continue
             if(flag == ""):
                 flag = word
                 word = ""
                 continue
        if(byte == "\n"):
            #make a new linked list node and reset the holding values
            if(DNSlist.head == None):
                #this means that the list is empty then we set the head of the list first
                DNSlist.head  = node(hostname,ip,flag)
                temphead  = DNSlist.head
                #reset the values
                hostname = ""
                ip = ""
                flag = ""
                continue
                
         

            temphead.next = node(hostname,ip,flag)
            temphead =temphead.next #moving the pointer to the newly added node
            #reset values 
            hostname = ""
            ip = ""
            flag = ""

    return DNSlist #return DNS list 


            



            
def searchDNS(self, name ):

    ptr = self.head
    while self.head is not None:

        if(ptr.data == name):
            print("here")












#creation of socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = int(sys.argv[1])

s.bind(('',port_number ))

s.listen(1)


print("waiting.....")

DNSList = populate_DNS #this will populate the linked list with all the dns things

while True:
    print("here")
    clientsocket,address =  s.accept()
    while True:
        data = clientsocket.recv(200).decode