#!/usr/bin/python3

#Name: Matthew Pessolano and Nicholas Campola
#Date: March 21st 2019
#Description: The client code for our Connect 4 solution. The client will be in charge of sending an acknowledgement when receiving the rules from the server, sending its choice of col, and receiving the board until a winner is decided. This will allow the user to play the game against an AI.
#I pledge that we have not received any unauthorized help on this assignment.

import socket
import matplotlib.pyplot as plt

#host and port information to connect to
HOST = "35.229.113.201"
PORT = 4040

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to server with socket
sock.connect((HOST, PORT))

# Protocol: expecting rules to be sent, send a "1" as an ACK
# Board state will be sent before each turn.
# Client will send their selected col and expect a "0" if this is not valid (column is full) or "1" if it succeeded.
# Repeat cycle until the client gets a "2" from the server (client has won) or "3" (AI has won) before disconnecting.

# Receive rules from server and print them
data = sock.recv(1027)
mesg = data.decode()
print(mesg)

		

# Allow user to read rules before continuing
input("\n\nPress enter to continue...")

# Send an "ACK" back
mesg = "1"
data = mesg.encode()
sock.sendall(data)

# Boolean
winstate = False
state = "0"

while(winstate == False):
	# Expect board state to be sent and printed out
	data = sock.recv(1024)
	mesg = data.decode()
	print(mesg)
	
	# Now, start the input loop until a valid response can be sent
	valid = False
	
	while(valid == False):
		col_choice = int(input('Player, please choose a column for your next checker. 0 refers to the first possible slot and 5 refers to the last possible slot: '))
		
		# check for invalid column
		if(col_choice < 0 or col_choice > 5):
			print("You have not selected a valid column.")
		# send response and wait for reply until a non-"1" response is received
		else:
			#Sending Choice
			data = str(col_choice).encode()
			sock.sendall(data)
			
			# receive reply
			data = sock.recv(1024)
			state = data.decode()
			
			# check that response received is not a fail state
			if(state == "1"):
				print("You have picked a column that is full. Please try again with a new column.")
			# otherwise break from loop
			else:
				valid = True
				
	#Checking if there is a winner
	data = sock.recv(1024)
	check = data.decode()
	
	# check that a winstate has not been achieved
	if(check == "2" or check == "3"):
		winstate = True;
		
		
# both while loop have been exited, meaning a winner has been determined
if(check == "2"):
	print("You have won Connect 4!")
else:
	print("The AI has won Connect 4 (somehow)!")
sock.close()
