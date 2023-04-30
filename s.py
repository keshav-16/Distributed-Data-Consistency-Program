import socket
import subprocess
import os

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the IP address and port number of the server
#server_address = ('127.0.0.1', 9090)
host = '127.0.0.1'
port = 9099

# Bind the socket to the server address
server_socket.bind((host,port))

# Listen for incoming connections
server_socket.listen(1)
print("Roadways server has started and is ready to receive")

# Accept the client connection
client_socket, client_address = server_socket.accept()
print("connected ",client_address[0],client_address[1])

# Receive the file contents from the client
print('File started receiving ...')

# Receive the file name and size from the client
file_name, file_size = client_socket.recv(1024).decode().split(',')

# Convert the file size to an integer
file_size = int(file_size)

# Receive the file contents from the client
received_size = 0
with open('file_name.txt', 'wb+') as file:
    while received_size < file_size:
        data = client_socket.recv(1024)
        received_size += len(data)
        file.write(data)
print('File received ...')

# Execute Python code with the file sent
process = os.popen('python3 main.py file_name.txt').read()

# Get the output from the executed Python code
#output, error = process.communicate()

# Send the processed output back to the client
client_socket.send(process.encode())
print('Data Sent ..')
print('\n')
print('----TABLE----')
print('\n')
process = os.system('python3 new.py file_name.txt')
print('\n')

# Close the socket connections
client_socket.close()
server_socket.close()
