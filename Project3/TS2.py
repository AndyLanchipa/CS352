import binascii
import socket
import sys
import time
class node:
    def __init__(self, Host, IP):
        self.Host = Host
        self.IP = IP
        self.next = None
class linked_list:
    def __init__(self):
        self.head = None



def add_DNS(self,data,IP):
    
    tempHead = self
    print("here")
    #adding to end of DNStable list
    Node = node(data,IP)
    if self.head is None:
        self.head = Node
        return 
    ptr = self.head

    while ptr.next:
        ptr= ptr.next

    ptr.next =Node


def searchDNS(self, name):


    temp = self.head
    print("here before loop of dns")
    while temp is not None:
        print("searching dns:" + temp.Host)

        if temp.Host.lower() == name.lower():
            print(temp.IP)
            return temp.IP
        temp = temp.next

    return None    



#this send_udp_message method was found on https://routley.io/posts/hand-writing-dns-messages/ and used by us for the sending and recieving to the udp
def send_udp_message(message, address, port):
    #message = message.replace(" ","").replace("\n","")

    print(address)
    print(port)
    server_address = (address, port)
    sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    

    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
        print("inside of udp socket adn reciving")
    finally:
        sock.close()
    
    return binascii.hexlify(data).decode("utf-8")


    #we want to parse rd lenght to get the length of how many ip adresses were sent back and you do this by masking 
    

def convert_address(server_address):

    hexform = ""

    c = ""

    for i in range(len(server_address)):
        c = server_address[i]
        #converting to ascii
        hold = ord(c)
        #convert hex and take off 0x from hex to soley get the number and put it into the hexform string
        temp = hex(hold).lstrip("0x")
        hexform += temp
        
    return hexform

def format_hex(hex):
    """format_hex returns a pretty version of a hex string"""
    octets = [hex[i:i+2] for i in range (0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)

def format_to_ip(hexval):     #currently works for only one IP
    ip = ""         #ip array for values

    while hexval:
        temp = str(int(hexval[:2], 16))
        hexval = hexval[2:]
        ip = ip + temp + "."

    ip = ip[:-1]
    return ip


def get_IP(data):
    temp =data
    addressArr = data.split(".")
    header = "aaaa01000001000000000000"
    fulldomain = ""
    count = 0
    while count < len(addressArr):
        fulldomain = fulldomain + str(hex(len(addressArr[count]))[2:]).zfill(2) + convert_address(addressArr[count])
        count += 1
    message = header + fulldomain + "0000010001"
    msgSize = len(message)
    #we are asking google for TS1 and for TS2 we are going to use cloudflare
    print("calling udp message function")
    response = send_udp_message(message,"1.1.1.1", 53)
    print("post udp message function")
    print("The response is:\t"+response)
            
    print("Formated hex response:\n"+format_hex(response))  
    resData = response[msgSize:]
    finIP = ""
    counter = int(msgSize)   

    while counter < len(response):
        resData = resData[20:]
        counter += 20
        size = int(resData[:4],16)*2

        counter += 4
        resData = resData[4:]
        data = resData[:size]
        resData = resData[size:]
        counter = counter + size

        if(size != 8):
            theIP = temp + " - " + "Error:HOST NOT FOUND"
        else: 
            theIP = format_to_ip(data)
        finIP = finIP + theIP +","
        
        
    finIP = finIP[:-1]
    return finIP


          

port = int(sys.argv[1])
server_address =('', port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)


DNSList = linked_list()

DNSList.head = None



#make server run forever until the socket is closed
while True:


    lssocket,address = sock.accept()
    while True:

        

        #this will recieve the host name and check the ts dns table if it contains it if not contact domain name server
        #to get the ip addresses
        data = lssocket.recv(10240).decode()
        if not data:
            break
        print("data: " + data)
        

        if DNSList.head is None:
        #need to ask the dns server for its ip 
            finIP = get_IP(data)

            #store host and ip in dns table
            

            DNSList.head =  node(data,finIP)
            print("here setting head")
            

            
        if DNSList.head is not None:

            temp = searchDNS(DNSList, data)

            if temp is None:
                print("temp is not found so we will ask DNS")
                #host is not found in local dns table call up the domain name server to get ip
                print("here before get ip")
                finIP = get_IP(data)
                print("here past")

                DNSList.head = add_DNS(DNSList,data,finIP)
                #got the ip adress send over ip to ls

                message = finIP
                print("got IP from DNS sending: " + message)
                
                lssocket.sendall(message.encode())
            else: 
                print( temp)
                #send over ip to ls
                message =temp
                
                lssocket.sendall(message.encode())

    lssocket.close()