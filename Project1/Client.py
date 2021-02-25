import argparse
from sys import argv
import socket


#creating a two sockets one for rs and one for TS

#argparse package to parse the arguments
parser = argparse.ArgumentParser(description="""This i s a client program to interact with two servers""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='PROJI-HNS.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='RESOLVED.txt',action='store', dest='out_file')
parser.add_argument('rsHostname', type=str, help='This is the domain name or ip address of the server', action='store')
parser.add_argument('rsListenPort', type=int, help='This is the port to connect to the rs server', action='store')
parser.add_argument('tsListenPort', type=int, help='This is the port to connect to the ts server', action='store')
args = parser.parse_args(argv[1:])

# rsHostname = ""
# rsListenPort = 0
# tsListenPort = 0

#servers = []
#print(argv)
#modArg = argv[2:]
#for ports in modArg:
#    ports = int(ports)
#    host = (rsHostname, ports) 
#    print(host)

#Single socket to connect client to rs server
try:
    rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client created the socket for RS")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

#Connection being made
#hostname = 
server_addr = (args.rsHostname, args.rsListenPort)
rs_sock.connect(server_addr)
counter = 0
with open(args.out_file, 'w') as write_file:
	for line in open(args.in_file, 'r'):
		#trim the line to avoid weird new line things
		line = line.strip()
		#now we write whatever the server tells us to the out_file
		if line:            
			print("The line is: "+line)
			rs_sock.sendall(line.encode('utf-8'))
			answer = rs_sock.recv(512)
			#decode answer
			answer = answer.decode('utf-8')
			print("The rec is: "+ answer)
			#Checks if it ends with an A
			if(answer.endswith("A")):
				write_file.write(answer + '\n')
				print("We wrote it down!")
			# else:
			# 	#If RS didn't have the hostname
			# 	print("\nClient closed the socket for RS")
			# 	rs_sock.close()

			# 	#Preps socket for 
			# 	try:
			# 		ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# 		print("\nClient created the socket for TS")
			# 	except socket.error as err:
			# 		print('socket open error: {} \n'.format(err))
			# 		exit()
				
			# 	server_addr = (args.rsHostname, args.tsListenPort)
			# 	ts_sock.connect(server_addr)
			# 	print("The line again is: "+line)
			# 	ts_sock.sendall(line.encode('utf-8'))
			# 	answer = ts_sock.recv(512)
			# 	#decode answer
			# 	answer = answer.decode('utf-8')
			# 	write_file.write(answer + '\n')
			# 	print("The ts answer has been written: "+ answer)
			# 	ts_sock.close()
			# 	print("\nClient closed the socket for TS")

			# 	try:
			# 		rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# 		print("\nClient created the socket for RS")
			# 	except socket.error as err:
			# 		print('socket open error: {} \n'.format(err))
			# 		exit()
				
			# 	server_addr = (args.rsHostname, args.rsListenPort)
			# 	rs_sock.connect(server_addr)
		counter+=1
		print("The counter is at: "+str(counter))



#close the socket (note this will be visible to the other side)
# if(write_file.closed == False):
# 	print("File has not closed")
print("The socket will close")
rs_sock.close()

# while True:
#     print("here")
#     response = client_sock.recv(512)
#     response = response.decode('utf-8')
#     lastChar = response[-1]

#     if lastChar == "A":
#         response = response[:-1]
#         for line in response:
#             words = line.split(" ")
#             print(words)
#     #else:

