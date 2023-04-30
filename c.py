import socket
import subprocess
import os
import sys

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP address and port number of the server
server_address = ('127.0.0.1', 9090)
host = '127.0.0.1'
port = 9099

# Connect to the server
client_socket.connect((host,port))

# Specify the file to be sent
file_name = sys.argv[1]

# Get the size of the file
file_size = os.path.getsize(file_name)

# Send the file name and size to the server
client_socket.send(f"{file_name},{file_size}".encode())

# Send the file contents to the server
with open(file_name, 'rb') as file:
    data = file.read(1024)
    while data:
        client_socket.send(data)
        data = file.read(1024)
print('File sent ...')

# Receive the processed output from the server
received_data = client_socket.recv(1024).decode()
print('Data Received...')

# Decode the received data and print it to the console
print(received_data)
print('\n')
print('----TABLE----')
print('\n')
process = os.system('python3 new.py file_name.txt')
print('\n')

# Close the socket connection
client_socket.close()
