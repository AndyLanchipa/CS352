import binascii
import socket
import sys



def send_udp_message(message, address, port):
    message = message.replace(" ","").replace("\n","")
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
        #converting to ascii
        hold = ord(c)
        #convert hex and take off 0x from hex to soley get the number and put it into the hexform string
        temp = hex(hold).lstrip("0x")

        hexform += temp

    return hexform


def rec_client_message():  #Assuming connection with client is TCP and connection with Google is UDP

    #lhost = "127.0.0.1"
    port = int(sys.argv[1])
    server_address = ('', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    print("Server port initiated: "+ str(port))

    while True:
        #data = sock.recvfrom(4096)#does not reach here
        conn, address = sock.accept()
        print("Connection from: "+ str(address))
        while True:
            data = conn.recv(10240).decode()
            if( not data):
                break

            #maybe here we want to take the link address then convert it to hex, then send it via udp then we can send it back
            #may want to consider a data structure to hold the addresses and respective responses

rec_client_message()
