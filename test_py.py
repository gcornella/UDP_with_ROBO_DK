################################################
########### UDP communication socket ###########
################################################

from robolink import *    # RoboDK's API
from robodk import *      # Math toolbox for robots
import socket # import the Python library regarding sockets
from scipy.interpolate import interp1d
import time

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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_server = sock # create aUDP server socket
sock_client = sock # create aUDP client socket


server_address = ('localhost', 10000) # Bind the server socket to the port
client_address = ('127.0.0.1', 65432) # Bind the client socket to the port

print('starting up on {} port {}'.format(*server_address))
sock_server.bind(server_address) # Bind theserver socket to the port - associate a connector 'localhost' with a port '10000'

# The UDP client is similar to the server but it does not use bind() to join itsconnector to an andress, it uses sendto()
while True:
    #time.sleep(1)
    # RECEIVE MESSAGE
    print('\nWaiting to receive message...')
    data, address = sock_server.recvfrom(4096) # The UDPserver uses recvfrom() to receive the message from the client in a given address that will be incrementing.
    print('Received {} bytes from {}'.format(len(data), address))
    print(' Received data is: {}'.format(data))

    if data: # If receiving data from the client...
        p_str = str(robot.Pose())
        p_str = p_str[5:30]
        p = bytes(p_str, 'utf-8')

        # SEND POSE OF ROBOT BACK
        sent = sock_client.sendto(p, client_address)                 # Use sendto() to deliver its message back to the client using the client address 65432
        print('Sent {} bytes back to {}'.format(sent, client_address))  # The client address should be 54000

        data_str = data.decode("utf-8")
        data_str = data_str.split(",")
        print(data_str)
        
        data_x = data_str[0]
        data_x = float(data_x)
        print(data_x)
        
        data_y = data_str[1]
        data_y = float(data_y)
        print(data_y)
        
        data_z = data_str[2].replace('\x00', '')
        data_z = float(data_z)
        print(data_z)

        # Calculate the new position around the reference:
        x = data_x  # new X coordinate
        y = data_y  # new Y coordinate
        z = data_z  # new Z coordinate

        if (x<-0.13 or y<-0.13 or z<-0.13):
            x=-0.1
            y=-0.1
            z=-0.1
        if (x>0.13 or y>0.13 or z>0.13):
            x=0.1
            y=0.1
            z=0.1
        
        m = interp1d([-0.13,0.13],[100.0,300.0])
        x_new = m(x)
        y_new = m(y)
        z_new = m(z)
        x_new = float(x_new)
        y_new = float(y_new)
        z_new = float(z_new)
        
        print(x_new)
        print(y_new)
        print(z_new)

        # Change the velocity of the robot to visualize the delay
        speed_lin = 5
        speed_joints = 5
        robot.setSpeed(speed_lin, speed_joints)
        target_pose.setPos([x_new,y_new,z_new])

        # result = program.Update()
        # Move to the new target:
        robot.MoveJ(target_pose)

    
# Trigger a program call at the end of the movement
robot.RunInstruction('Program_Done')

# Move back to the reference target:
##################### END SOCKET ###########################
