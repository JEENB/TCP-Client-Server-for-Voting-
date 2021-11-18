import socket
import re
import getpass


def email_check(email):
	x = True
	while x == True:
		if not re.search(email_regex, email):
			print("Invalid Email!!")
			email = input("Email Address:")
		else: 
			x = False


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
	if msg[0:4] == "Your" or msg[0:5] == "Thank" or msg[0:3] == "You" or msg[0:4] == "Vote" or msg[-1]=='-':
		print('\033[91m' + msg + '\033[0m')
		connection == False
		break
	if msg[0] == 'U' or msg[9:13] == 'Pass':
		print(msg)
		communication = getpass.getpass()
		client_socket.send(communication.encode())
	else:
		print(msg)
		communication = input()
		client_socket.send(communication.encode())
	

client_socket.close()
# if valid_options == "l":
# 	login_msg = client_socket.recv(1024).decode()
# 	print(login_msg)

# 	# authentication using email and password
# 	email = input()
# 	email_check(email)
	
# 	client_socket.send(email.encode())
# 	password_msg = client_socket.recv(1024).decode()

# 	password = getpass.getpass()
# 	client_socket.send(password.encode())

# elif valid_options == "s":
# 	login_msg = client_socket.recv(1024).decode()
# 	print(login_msg)

# 	# authentication using email and password
# 	email = input()
# 	email_check(email)
	
# 	client_socket.send(email.encode())
# 	password_msg = client_socket.recv(1024).decode()
# 	print(password_msg)
###======================== Client authentication (end) =========================



##======================== Voting / results (start) =========================
# welcome_msg = client_socket.recv(1024).decode()
# print(welcome_msg)
# options = input()


# while options not in ["1","2","3"]:
# 	print("Invalid option selected")
# 	options = input()

# client_socket.send(options.encode())

# incoming_msg = client_socket.recv(1024).decode()

# print(incoming_msg)

# if incoming_msg[-6] == "v":
# 	candidate = input()
# 	while candidate not in ["1","2","3","4","5"]:
# 		print("Invalid candidate selected")
# 		candidate = input()
# 	client_socket.send(candidate.encode())
# else:
# 	print(client_socket.recv(1024).decode())

# client_socket.close()

