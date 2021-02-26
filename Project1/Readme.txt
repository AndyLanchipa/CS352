0. Andy Lanchipa - aal155 and Benjamin Rocco - bwr29

-------------------------------------------------------

1. We implemented our recursive client functionality by having the program communicate first with the root server to see if the list of hostnames were accessible from the server, one hostname at a time, if it was
then the socket would close after the result was written in the RESOLVED.txt file. If not, then it would close the socket with the root server after the root server provided the hostname for the top-level server, 
and establish a connection with the top-level server and obtain the information from that server. If no information was able to be obtained, the hostname would be labeled with "Error:HOST NOT FOUND" and written in
the RESOLVED.txt file.

--------------------------------------------------------

2. There are no known issues with the code.

--------------------------------------------------------

3. Skimming through the directions, and not fully understanding it during the approach. Struggling to understand how to properly send and receive data over sockets. Bwr29's laptop developed a unique error with the 
.write() functionality of argparse, causing him to abandon working on his laptop and soley working on the ilabs. Understanding the syntax of python and dealing with null pointers. 

---------------------------------------------------------

4. We learned the importance of testing on ilabs. Starting early because ideas may be scrapped or proven to be harder to implement than at first thought. To fully think and debug thoroughly. The fragility of sockets.