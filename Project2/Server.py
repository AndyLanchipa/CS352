import binascii
import socket
import sys
from typing import Counter



def send_udp_message(message, address, port):
    #message = message.replace(" ","").replace("\n","")
    server_address = (address, port)
    sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)

    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


    #we want to parse rd lenght to get the length of how many ip adresses were sent back and you do this by masking 
    

def convert_address(server_address):

    hexform = ""

    c = ""

    for i in range(len(server_address)):
        c = server_address[i]
        # if(c == '.'):
        #     c = server_address[i+1]
        #     break;
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



def rec_client_message():  #Assuming connection with client is TCP and connection with Google is UDP

    #lhost = "127.0.0.1"
    port = int(sys.argv[1])
    server_address = ('', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    print("Server port initiated: "+ str(port))
    header = "aaaa01000001000000000000"     #may need a different implementation for headers, but good for now
    #id = 'AA AA'
    #counter
    while True:
        #data = sock.recvfrom(4096)#does not reach here
        conn, address = sock.accept()
        print("Connection from: "+ str(address))
        while True:
            data = conn.recv(10240).decode()
            if not data:
                break
            print("The data is: " + data)
            # dataLedataLen = hex(len(data))[2:]
            # print("The length of the address is: " + dataLen)
            
            addressArr = data.split(".")
            countdomain =  str(hex(len(addressArr[0]))[2:]).zfill(2)
            countend = str(hex(len(addressArr[1]))[2:]).zfill(2)
            domain = convert_address(addressArr[0])
            end = convert_address(addressArr[1])
            end = end + "00"

            print("Length of domain: "+ countdomain + "\tDomain in hex: "+ domain)
            print("Length of end: "+ countend + "\tDomain in hex: "+ end)
            message = header + countdomain + domain + countend + end + "00010001"
            print("The message is: "+ message)
            response = send_udp_message(message, "8.8.8.8", 53)
            print("We get here")
            print("The response is: "+response)
            print("Formated hex response: "+format_hex(response))
            print("Type")
            print(type(response))
            print("Format int:")
            print(int(response, 16))
            num = int(response, 16)

            print("Converted")
            print(num & (pow(2, 32) -1))

            #maybe here we want to take the link address then convert it to hex, then send it via udp then we can send it back
            #may want to consider a data structure to hold the addresses and respective responses
        conn.close()

rec_client_message()
