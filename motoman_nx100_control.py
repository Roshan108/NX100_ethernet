# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 13:18:08 2024

@author: yours
"""

import socket
import logging
import time
import numpy as np

# NX100 IP and port
nx100_ip = "192.168.100.10"
nx100_port = 80

def orient_for_alpha(alpha, theta_x):
    # This function will return the wrist angles theta_x, theta_y, and theta_z for 
    # achieving the desired angle alpha
    
    # Decide theta_y arbitrarily and then compute theta_x
    # theta_z can be kept at any suitable value
    
    #theta_x = np.arccos(np.tan(alpha) * np.tan(theta_y))
    
    theta_y = np.arctan(np.cos(theta_x) / np.tan(alpha))
    
    return theta_y

def zero_moment_trajectory(alpha, theta_xi):
    n = 30 # Number of points in the trajectory
    # theta_yi = np.pi/6
    theta_x = np.linspace(theta_xi,np.pi/2,n)
    # alpha = np.pi/3
    
    Thetas = np.zeros((n,2))
    
    Thetas[:,0] = theta_x
    
    for i in range(len(theta_x)):
        Thetas[i,1] = np.arctan(np.cos(theta_x[i]) / np.tan(alpha))
        
    return Thetas
        
def servo_on():
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
        
        client_socket.sendall(b"HOSTCTRL_REQUEST SVON 2\r")
        # Note here that Size of the data is given as 2. This includes '1' and a space. Carriage return \r should be given at the end
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        command_data = str(1) + ' ' + '\r' 
        client_socket.sendall(command_data.encode("utf-8"))
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
    finally:
        # Clean up
        client_socket.close()
    
def servo_off():
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
        
        client_socket.sendall(b"HOSTCTRL_REQUEST SVON 2\r")
        # Note here that Size of the data is given as 2. This includes '1' and a space. Carriage return \r should be given at the end
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        command_data = str(0) + ' ' + '\r' 
        client_socket.sendall(command_data.encode("utf-8"))
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
    finally:
        # Clean up
        client_socket.close()

def MOVL(x, y, z, speed='20.0', tx = '180', ty = '0'):
    # This MOVL is dedicated for changing the orientation of the end-effector. I will create another MOVL dedicated to 
    # Changing the position of the end-effector.
    
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
        
        
        data_str = '0,' + speed +',1,' + str(x) + ',' + str(y) + ',' + str(z) + ',' + tx + ',' + ty + ',' + '0,0,0,0,0,0,0,0,0 \r'
        
        h_ctrl_string = "HOSTCTRL_REQUEST MOVL " + str(len(data_str)) + "\r"
        client_socket.sendall(h_ctrl_string.encode())
        # Note here that Size of the data is given as 43. 
        # This can be obtained by len('0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 ')
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        #client_socket.sendall(b'0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 \r')
        client_socket.sendall(data_str.encode())
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
        

    finally:
        # Clean up
        client_socket.close()
    
    
def MOVL_orient(tx, ty, tz, speed = '9.0'):
    # This MOVL is dedicated for changing the orientation of the end-effector. I will create another MOVL dedicated to 
    # Changing the position of the end-effector.
    
    x = 380 
    y = -128
    z = 165
    
    data_str = '1,'+ speed + ',1,' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(tx) + ',' + str(ty) + ',' + '0,0,0,0,0,0,0,0,0 \r'
    # The first parameter says that I am specifying the posture speed.
    # The gives the posture speed. Something like 9 is a very very high speed. Try from 0.1 onwards
    print(data_str)
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
        
        
        h_ctrl_string = "HOSTCTRL_REQUEST MOVL " + str(len(data_str)) + "\r"
        # We create the strink separately because the number of bits have to be calculated.
        
        client_socket.sendall(h_ctrl_string.encode())
        # Note here that Size of the data is given as 43. 
        # This can be obtained by len('0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 ')
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        #client_socket.sendall(b'0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 \r')
        client_socket.sendall(data_str.encode())
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
        

    finally:
        # Clean up
        client_socket.close()


def close_gripper():
    # This I should execute using the START command that starts a job in the pendant memory.
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
        
        h_ctrl_string = "HOSTCTRL_REQUEST START\r"
        # We create the strink separately because the number of bits have to be calculated.
        
        client_socket.sendall(h_ctrl_string.encode())
        # Note here that Size of the data is given as 43. 
        # This can be obtained by len('0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 ')
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        #client_socket.sendall(b'0,9.0,1,440,-8,165,180,0,0,0,0,0,0,0,0,0,0 \r')
        client_socket.sendall(b"GRIP") # This is the program on the teach pendant we want to run.
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
    finally:
        # Clean up
        client_socket.close()


def read_status():
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
        
        client_socket.sendall(b"HOSTCTRL_REQUEST RSTATS 0\r")
        # Note here that Size of the data is given as 4. This includes '1' ',' '1' amd a space. Carriage return \r should be given at the end
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        #client_socket.sendall(b'\r')
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
        
    # If the string is 202 the previous command is still running. If it is 194, the previous command is not
    # running.
    # I will use this simple logic for checking the status. Changing to binary and checking every bit is not important
    
    finally:
        # Clean up
        client_socket.close()
    # Let me return the final value as a number.
    
    response_decoded = response1.decode()
    response_value = int(response_decoded[0:3])
    
    return response_value # Return the number 202 or 194


def gripper_open():
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
        
        client_socket.sendall(b"HOSTCTRL_REQUEST SVON 2\r")
        # Note here that Size of the data is given as 2. This includes '1' and a space. Carriage return \r should be given at the end
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        client_socket.sendall(b'1 \r')
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
        
        

    finally:
        # Clean up
        client_socket.close()


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
        
        # Note that the jopb name is TOOLOF and not TOOLOFF
        job_name = "TOOLOF \r"
        
        h_ctrl_string = "HOSTCTRL_REQUEST START " + str(len(job_name)) + "\r"
        
        client_socket.sendall(h_ctrl_string.encode())
        # Note here that Size of the data is given as 2. This includes '1' and a space. Carriage return \r should be given at the end
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        client_socket.sendall(job_name.encode())
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
         
        
        

    finally:
        # Clean up
        client_socket.close()


def gripper_close():

    servo_on()

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
        
        # Note that the jopb name is TOOLOF and not TOOLOFF
        job_name = "TOOLON \r"
        
        h_ctrl_string = "HOSTCTRL_REQUEST START " + str(len(job_name)) + "\r"
        
        client_socket.sendall(h_ctrl_string.encode())
        # Note here that Size of the data is given as 2. This includes '1' and a space. Carriage return \r should be given at the end
        
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", command_response)
        
        # send command data
        client_socket.sendall(job_name.encode())
        response1 = client_socket.recv(4096)
        command_response = repr(response1)
        print("Received:", response1.decode())
         
        
        

    finally:
        # Clean up
        client_socket.close()
