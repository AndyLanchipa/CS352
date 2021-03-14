import binascii
import socket



def send_udp_message(message, address, port):
    message = message.replace(""," ").replace("\n","")
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




