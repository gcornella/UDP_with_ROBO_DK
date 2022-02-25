################################################
########### UDP communication socket ###########
################################################

import socket  # import the Python library regarding sockets

# AF_INET is the domain, to designate the type of directions with whom the socket can communicate (in this case with Internet Protocol v4).
# SOCK_DGRAM is the type, UDP messages must be within 1 datagram (for IPv4, ethey can just contain 65,507 bytes). Sockets for communications in 'no-connected' mode
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_server = sock  # create a UDP server socket
sock_client = sock  # create a UDP client socket

server_address_PC = ('localhost', 10000)        # Bind the server socket to the port
client_address_RoboDK = ('127.0.0.1', 65432)    # Bind the client socket to the port

# print('starting up on {} port {}'.format(*server_address))
sock_server.bind(server_address_PC)             # Bind the server socket to the port - associate a connector 'localhost' with a port '10000'

# while True:                                   # Comment if you just want to send the data once
########### SENDING ###########
# Data to be sent to RoboDK, in this case the Polygon radius
data = b'150'                                           # The polygon radius to be sent
sent = sock_client.sendto(data,client_address_RoboDK)   # Use sendto() to deliver its message to the client
print('\nSend message {} with {} bytes from PC to RoboDK address {}'.format(data, sent, client_address_RoboDK))

########### RECEIVING ###########
# Data to be received from RoboDK (Message feedback or reply)
print('Waiting to receive message from RoboDK...')
data, address = sock_server.recvfrom(4096)               # The UDP server uses recvfrom() to receive the message reply from the client.
print('PC has received data {} with {} bytes from {}'.format(data, len(data), address))

##################### END PC SOCKET ###########################
