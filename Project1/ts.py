from os import link
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

def populate_DNS(self):


    f = open('PROJI-DNSTS.txt' , 'r')
    byte = f.read(1)

    word = ""
    
    hostname = ""
    Ip = ""
    flag = ""
    


    #disect words

    while True:
        byte = f.read(1)

        if(byte != "\n"or byte!= " "):
            word+=byte
        print("byte -> " + byte)
        
        if(byte == ''):
            break
     
        if(byte == " "):

             if(hostname == ""):
                 hostname = word.strip()
                 word = ""
                 continue
             if(Ip == ""):
                 Ip = word.strip()
                 word = ""
                 continue
             if(flag == ""):
                 flag = word.strip()
                 word = ""
                 continue
        if(byte == "\n"):
            #make a new linked list node and reset the holding values
            if(flag == ""):
                    flag = word.strip()
                    word = ""
            if(self.head == None):
                #this means that the list is empty then we set the head of the list first
                self.head  = node(hostname,Ip,flag)
                append(self,hostname,Ip,flag)
                #reset the values
                hostname = ""
                Ip = ""
                flag = ""
                continue
                
         

            append(self , hostname,Ip, flag)
            #reset values 
            hostname = ""
            Ip = ""
            flag = ""
    f.close()
    return self.head #return DNS list 
def searchDNS(self, name ):

    info = ""
    temp = self.head
    while temp is not None:
        print(temp.host + " ->>>> " + name)
        if(temp.host.lower() == name.lower()):
            #host is found now we make the string to return
            print("made it in here")

            
            return info + temp.host + " " + temp.IP + " " + temp.Flag 

        temp = temp.next #moving ptr to next val
 
    #if it goes out of the while loop the match isnt found and return that match isnt found

    return name + " - Error:HOST NOT FOUND" 

def append(self , host, ip , flag):
    Node = node(host , ip ,flag)

    if self.head is None:
        self.head = Node
        return
    
    ptr = self.head

    while (ptr.next):
        ptr = ptr.next

    ptr.next = Node
#creation of socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = int(sys.argv[1])

s.bind(('',port_number ))
DNSList = linked_list()

DNSList.head = populate_DNS(DNSList) #this will populate the linked list with all the dns things

s.listen(1)


print("waiting.....")




#running server

while True:
    print ("here")
    clientsocket,address = s.accept()

    while True:
        data = clientsocket.recv(512).decode('utf-8')
        if not data:
            break
        
     
        Info  = searchDNS(DNSList,data)
        print("info_>>>>   "+ Info)
        clientsocket.send(Info.encode())
        
    clientsocket.close()