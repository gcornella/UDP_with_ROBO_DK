# UDP_with_ROBO_DK
This project consists in the communication between a Python server and a ROBO_DK Simulation [link](https://robodk.com/) via the UDP protocol

Implementation of a UDP socket in Python to communicate between the user and the RoboDK interface. We have 2 Python scripts:
- **PC_UDP_socket**: It sends from the PC server to the RoboDK client the desired radius dimension as a byte object. The user chooses the data to be sent and then by using a UDP protocol, we are able to send this packet to the RoboDK interface.
- **RoboDK_UDP_socket**: First of all, the robot moves from its current location to Target1 and then it waits for the user to send the radius by using the “PC_UDP_socket.py” script. Then it receives the radius and it draws the polygon according to the sent radius. Finally, it replies back to the server to inform that the data has been properly received.

