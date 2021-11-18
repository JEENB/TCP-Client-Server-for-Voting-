import socket
import threading
from threading import Thread
from numpy.core.arrayprint import ComplexFloatingFormat
from numpy.core.fromnumeric import shape

from datetime import datetime, timedelta
import re
import random
import string
# import numpy as np


# voting end time set to 30 min after start of the server
voting_end_time = datetime.now() + timedelta(minutes=1)

#user_table: (email, pswd, ip, time) stores the signup credentials
#live_table: (Email,Client_IP,Live_Time,Port) keeps record of active connections
global user_table, live_table, user_dic


# user_table = np.empty(shape=(0,4))
live_table = []

voted_table = []  # stores the ip of clients who have voted

user_dic = dict()

def random_password_generator():
	alphabets = string.ascii_letters + string.digits + string.punctuation
	pswd = ''.join(random.choice(alphabets) for i in range(10))
	return pswd


def check_existing_user(email, password):
	if email in user_dic:
		buffer = user_dic[email]
		if password != buffer[0]:
			return "Password Error!"
		elif password == buffer[0]:
			return 'True'
	else:
		return "User does not exist please sign up to continue"

# def check_existing_ip(client_ip):
# 	if email in user_dic:
# 		buffer = user_dic[email]
# 		if password != buffer[0]:
# 			return "Password Error!"
# 		elif password == buffer[0]:
# 			return True
# 	else:
# 		return "User does not exist please sign up to continue"

	# if email in user_table[:,0] and password in user_table[:,1]:
	# 	return True
	# elif email in user_table[:,0] and password not in user_table[:,1]:
	# 	return "Password Error!"
	# elif email not in user_table[:,0]:
	# 	return "User does not exist please sign up to continue"

def login(client):
	client.send("Email Address:".encode())
	client_email = client.recv(1024).decode()
	client.send("Password: ".encode())
	client_password = client.recv(1024).decode()
	return client_email, client_password
	
def signup(client):
	user = {}
	client.send("Email Address:".encode())
	client_email = client.recv(1024).decode()
	# if client_email in user_dic:
	# 	client.send("User with email exist! \nPlease enter password to contunue!\nPassword: ".encode())
	# 	client_password = client.recv(1024).decode()
	# 	check =  check_existing_user(client_email, client_password) 
	# 	while check[0] == "P":
	# 		client.send(check.encode())
	# 		client_email, client_password = login(client)
	# 		check =  check_existing_user(client_email, client_password) 
	# 	if check[0] == "T":
	# 		live_table.append(addr[0])	
	# 		print(live_table)
	# else:

	client_password = random_password_generator()
	client.send("This is you password : {} \nYou  may require it to login!!\n\n".format(client_password).encode())
	# user = np.array([[client_email, client_password, addr[0], datetime.now().strftime("%d/%m/%Y %H:%M:%S")]])
	user_info = [client_password,addr[0], datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
	user[client_email] = user_info
	return user
	


candidates = {1: "Dorendra Odi", 2: "Adrusher Baideu", 3: "P.K. Iol", 4:"Andi Aul", 5: "Riden Oiden"}


login_msg = "Welcome! Please login or signup to start the voting process (l/s) else 3 to quit!!"

welcome_msg = "Welcome! You can participant in the vote by presenting your password. Reply with a \"1\" if you want to participate now; with a ”2” if you want to see the results; and with ”3” other wise."


port = 5545
server_ip = "192.196.1.17"
server_ip = socket.gethostbyname(socket.gethostname())  #gethost name gets the local ip for the server
address = (server_ip, port)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(address)

print('Server is running! (IP Address: %s, Port: %s)' % (server_ip, port)) 

server.listen(4)


vote_count = [0,0,0,0,0]


while True:
	client, addr = server.accept()

	print("Connection from: " + str(addr))





	client.send(login_msg.encode())

	client_response = client.recv(1024).decode()

	if client_response == "l":
		client_email, client_password = login(client)
		check =  check_existing_user(client_email, client_password) 
		print(check)
		if check[0] == "U":
			client.send(check.encode())
			user = signup(client)
			# user_table = np.append(user_table,user, axis = 0)
			user_dic.update(user)
			print(user_dic)
		while check[0] == "P":
			client.send(check.encode())
			client_email, client_password = login(client)
			check =  check_existing_user(client_email, client_password) 
		if check[0] == "T":
			live_table.append(addr[0])	
			print(live_table)
	elif client_response == "s":
		user = signup(client)
		# user_table = np.append(user_table,user, axis = 0)
		user_dic.update(user)
		live_table.append(addr[0])
		print(user_dic)
	elif client_response == "3":
		client.send("Your connection has been closed!!".encode())
		client.close()


	client.send(welcome_msg.encode())

	vote_msg = client.recv(1024).decode()

	if vote_msg == "1" and datetime.now() <= voting_end_time:
		if addr[0] in voted_table:
			sorry_msg = "Vote already regestered for your IP, you cannot vote twice. "
			client.send(sorry_msg.encode())
			live_table.remove(addr[0])
			client.close()
		else:
			candidate_msg = "\n===============================\n      List of Candidates\n===============================\n1: Dorendra Odi\n2: Adrusher Baideu\n3: P.K. Iol,\n4: Andi Aul\n5: Riden Oidenn\n===============================\n\nEnter the corresponding number to vote!!"			
			client.send(candidate_msg.encode())
			vote = client.recv(1024).decode()
			vote_count[int(vote)-1] += 1
			voted_table.append(addr[0])
			# print(voted_table)
			closing_msg = "Thank you for participating. Your response is registered against your IP address - {}".format(addr[0])
			client.send(closing_msg.encode())
			live_table.remove(addr[0])
			client.close()
	elif vote_msg == "2":
		if datetime.now() <= voting_end_time:
			client.send("You cannot view the result, voting has not ended! Please check after {}".format(voting_end_time).encode()) 
		else:
			election_result = "\n===============================\n      Voting Results\n===============================\n"
			candidates_result = str()
			for key in candidates:
				candidate_vote = vote_count[key-1]
				election_result = election_result + candidates[key] +": "+ str(candidate_vote) + "\n"
			election_result = election_result + "-------------------------------"
			client.send(election_result.encode())

	elif vote_msg == "3":
		client.send("Your connection has been closed!!\nThank you for participating!!".encode())
		live_table.remove(addr[0])
		client.close()
	else: 
		client.send("You cannot vote now, voting has closed.".encode())
		live_table.remove(addr[0])
		client.close()
	print(live_table)









