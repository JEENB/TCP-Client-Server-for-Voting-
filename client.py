import socket
import re
import getpass


def email_check(email):
	x = True
	while x == True:
		if not re.search(email_regex, email):
			print("Invalid Email!!\n")
			email = input("Email Address:\n")
		else: 
			x = False
	return email


email_regex = '[A-Za-z0-9._%+-]+@ashoka\.edu\.in'

port = 5545
server = "192.168.1.17"
server_address = (server,port)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(server_address)
connection = True

# initial_msg = client_socket.recv(1024).decode()
# print(initial_msg)

# valid_options = input()

# ###======================== Client authentication (start) =========================
# while valid_options not in ["l","s","3"]:
# 	print("Invalid option selected")
# 	valid_options = input()

# client_socket.send(valid_options.encode())
while connection == True:
	msg = client_socket.recv(1024).decode()

	if msg[0:4] == "Your" or msg[0:5] == "Thank" or msg[0:3] == "You" or msg[0:4] == "Vote" or msg[-1]=='-' or msg[0] == 'E' or msg[0] == "I" or msg[0] == 'A':
		'''Msgs that close connection'''
		print(msg)
		connection == False
		break
	

	if msg[0] == 'U' or msg[0:4] == 'Pass':
		'''Msgs for password'''
		print(msg)
		communication = input()  #replace input with getpass.getpass('') to not view password in terminal.
		client_socket.send(communication.encode())
	elif msg[0:10] =="Welcome! P":   # welcome msg for email
		print(msg)
		communication = input()
		email = email_check(communication)
		client_socket.send(email.encode())
	elif msg[0:10] =="Welcome! Y": #welcome msg for participation
		print(msg)
		valid_options = input()

		while valid_options not in ["1","2","3"]:
			print("Invalid option selected")
			valid_options = input()

		client_socket.send(valid_options.encode())
	elif msg[1] =="=": #validation for voting 
		print(msg)
		valid_options = input()

		while valid_options not in ["1","2","3","4","5"]:
			print("Invalid option selected\n\nEnter valid option!")
			valid_options = input()

		client_socket.send(valid_options.encode())

	else:
		print(msg)
		communication = input()
		client_socket.send(communication.encode())
	

client_socket.close()
