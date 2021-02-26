import argparse
from sys import argv
import socket

#argparse package to parse the arguments
parser = argparse.ArgumentParser(description="""This is a client program to interact with two servers""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='PROJI-HNS.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='RESOLVED.txt',action='store', dest='out_file')
parser.add_argument('rsHostname', type=str, help='This is the domain name or ip address of the rs server', action='store')
parser.add_argument('rsListenPort', type=int, help='This is the port to connect to the rs server', action='store')
parser.add_argument('tsListenPort', type=int, help='This is the port to connect to the ts server', action='store')
args = parser.parse_args(argv[1:])

#Single socket to connect client to rs server
try:
    rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client created the socket for RS")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

#Connection being made
server_addr = (args.rsHostname, args.rsListenPort)
rs_sock.connect(server_addr)

with open(args.out_file, 'w') as write_file:
	for line in open(args.in_file, 'r'):
		#trim the line to avoid weird new line things
		line = line.strip()

		#now we write whatever the server tells us to the out_file
		if line:            
			rs_sock.sendall(line.encode('utf-8'))
			answer = rs_sock.recv(512)
			#decode answer
			answer = answer.decode('utf-8')

			#Checks if it ends with an A
			if(answer.endswith("A")):
				write_file.write(answer + '\n')
			else:
				#If RS didn't have the hostname

				#closes rs socket
				rs_sock.close()
				print("\nClient closed the socket for RS")

				#Preps ts socket 
				try:
					ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					print("\nClient created the socket for TS")
				except socket.error as err:
					print('socket open error: {} \n'.format(err))
					exit()
				
				#establishes ts connection
				ts_loc = answer.split(' ', 1)[0]
				server_addr = (ts_loc, args.tsListenPort)
				ts_sock.connect(server_addr)

				ts_sock.sendall(line.encode('utf-8'))
				answer = ts_sock.recv(512)
				#decode answer
				answer = answer.decode('utf-8')
				write_file.write(answer + '\n')

				#closes ts socket
				ts_sock.close()
				print("\nClient closed the socket for TS")

				#preps rs socket again
				try:
					rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					print("\nClient created the socket for RS")
				except socket.error as err:
					print('socket open error: {} \n'.format(err))
					exit()
				
				#connects rs socket
				server_addr = (args.rsHostname, args.rsListenPort)
				rs_sock.connect(server_addr)

rs_sock.close()
print("\nClient closed the socket for TS")