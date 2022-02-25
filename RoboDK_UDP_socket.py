# Draw a hexagon around the current robot position
# First, the robot is moved to the target and then it waits for a udp packet that will contain the radius of the polygon

from robolink import *    # RoboDK's API
from robodk import *      # Math toolbox for robots
import socket                                                           # import the Python library regarding sockets

# Start the RoboDK API:
RDK = Robolink()
 
# Get the robot (first robot found):
robot = RDK.Item('', ITEM_TYPE_ROBOT)
 
# Get the reference target by name:
target = RDK.Item('Target 1')
target_pose = target.Pose()
robot.MoveJ(target)


target_pose = robot.Pose()
xyz_ref = target_pose.Pos()
 
# Redundant --> Move the robot to the reference point (current position/redundant):
# robot.MoveJ(target_pose)

################################################
########### UDP communication socket ###########
################################################

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          
sock_server = sock                                                      # create a UDP server socket
sock_client = sock                                                      # create a UDP client socket

client_address_PC = ('localhost', 10000)                                # Bind the server socket to the port
server_address_RoboDK = ('127.0.0.1', 65432)                            # Bind the client socket to the port

print('Starting up on {} port {}'.format(*server_address_RoboDK))
sock_server.bind(server_address_RoboDK)                                 # Bind the server socket to the port - associate a connector 'localhost' with a port '10000'

# while True:                                                           # Comment if you just want the code to runonce
########### RECEIVING ###########
print('\nWaiting to receive message from PC...')
data, address = sock_server.recvfrom(4096)                              # The UDP server uses recvfrom() to receive the message from the client in a given address that will be incrementing.
print('RoboDK has received data {} with {} bytes from PC address {}'.format(data,len(data), address))       

if data:    
    ########### SENDING VALIDATION ###########                                     # If receiving data from the client...
    data_back = b'RoboDK has Received properly'
    sent = sock_client.sendto(data_back, client_address_PC)                 # Use sendto() to deliver its message back to the client using the client address 65432
    print('Send data {} with {} bytes back to {}'.format(data_back, sent, client_address_PC))  # The client address should be 54000
    
    # DRAWING HEXAGON
    for i in range(7):
        ang = i*2*pi/6 # Angle = 0,60,120,...,360
        R = int(data)        # Polygon radius

        # Calculate the new position around the reference:
        x = xyz_ref[0] + R*cos(ang) # new X coordinate
        y = xyz_ref[1] + R*sin(ang) # new Y coordinate
        z = xyz_ref[2]              # new Z coordinate    
        target_pose.setPos([x,y,z])
        
        # Move to the new target:
        robot.MoveL(target_pose)

# Trigger a program call at the end of the movement
robot.RunInstruction('Program_Done')

# Move back to the reference target:
robot.MoveL(target)
##################### END SOCKET ###########################