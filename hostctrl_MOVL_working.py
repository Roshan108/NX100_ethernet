# -*- coding: utf-8 -*-
"""
Created on Sun May 26 10:03:55 2024

@author: yours

Working code for MOVL
Look at the documentation for more details.
"""

import socket
import logging

# NX100 IP and port
nx100_ip = "192.168.100.10"
nx100_port = 80

# Create a socket (client)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to NX100
    client_socket.connect((nx100_ip, nx100_port))
    print("Connected to NX100")

    # Send data (e.g., a command)
    client_socket.sendall(b"CONNECT Robot_access \r\n")
    

    # Receive response
    response = client_socket.recv(1024)
    print("Received:", response.decode())
    
    client_socket.sendall(b"HOSTCTRL_REQUEST MOVL 43\r")
    # Note here that Size of the data is given as 43. 
    # This can be obtained by len('0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 ')
    
    response1 = client_socket.recv(4096)
    command_response = repr(response1)
    print("Received:", command_response)
    
    # send command data
    client_socket.sendall(b'0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 \r')
    response1 = client_socket.recv(4096)
    command_response = repr(response1)
    print("Received:", response1.decode())
    
    

finally:
    # Clean up
    client_socket.close()
