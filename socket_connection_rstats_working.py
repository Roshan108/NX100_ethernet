# -*- coding: utf-8 -*-
"""
Created on Sun May 26 10:03:55 2024

@author: yours
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
    
    client_socket.sendall(b"HOSTCTRL_REQUEST RSTATS 0\r\n")
    response1 = client_socket.recv(4096)
    command_response = repr(response1)
    print("Received:", command_response)
    
    # send command data
    client_socket.send(b'')
    response1 = client_socket.recv(4096)
    command_response = repr(response1)
    print("Received:", command_response)
    
    

finally:
    # Clean up
    client_socket.close()
