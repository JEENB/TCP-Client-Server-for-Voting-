import socket
from _thread import *
from datetime import datetime, timedelta
import re
import random
import string
# import numpy as np

thread_count = 0
# voting end time set to 30 min after start of the server
voting_end_time = datetime.now() + timedelta(minutes=1)

#user_table: (email, pswd, ip, time) stores the signup credentials
#live_table: (Email,Client_IP,Live_Time,Port) keeps record of active connections
global user_table, live_table, user_dic, vote_count


# user_table = np.empty(shape=(0,4))
live_table = []

voted_table = []  # stores the ip of clients who have voted

vote_count = [0,0,0,0,0]

user_dic = dict()


candidates = {1: "Dorendra Odi", 2: "Adrusher Baideu", 3: "P.K. Iol", 4:"Andi Aul", 5: "Riden Oiden"}

login_msg = "Welcome! Please enter your ashoka email to continue!!\n\nEmail Address:"

welcome_msg = "Welcome! You can participant in the vote by presenting your password. Reply with a \033[34m\"1\"\033[0m if you want to participate now; with a \033[34m\"2\"\033[0m if you want to see the results; and with \033[34m\"3\"\033[0m other wise."

def random_password_generator(length=10):
	'''Func: random_password_generator
	args: Lenght: length of password. Defalult set to 10.
	returns:
		random passowrd of lenght 10'''
	alphabets = string.ascii_letters + string.digits + string.punctuation
	pswd = ''.join(random.choice(alphabets) for i in range(length))
	return pswd


def check_existing_user(email, password):
	'''Func: chek_existing_user
	args: email, password
	checks if email and password match with user_table,
	returns:
		True: if user exist
		Password Error: if user exist but wrong password given.
	'''
	if email in user_dic:
		buffer = user_dic[email]
		if password != buffer[0]:
			return "Password Error!\n"
		elif password == buffer[0]:
			return 'True'

def close_connections(client,msg,addr):
	client.send(msg.encode())
	live_table.remove(addr[0])
	client.close()

def check_password(email,password):
	pswd = user_dic[email][0]
	if pswd == password:
		return True
	else:
		return False

def get_password(client):
	'''function: get_password
	Gets the password from user if "Password Error encountered.'''
	# client.send("Email Address:".encode())
	# client_email = client.recv(1024).decode()
	client.send("\033[41mPassword Error!\033[0m\n".encode())
	client_password = client.recv(1024).decode()
	return client_password
	
def signup(client):
	'''
	function: signup()
	Initial Input: Client_Email
	IF email exist in user_table then asks for password and proceedes for login.
	IF email does not exis in user_table then generates a random password and signs the user up. 
	
	'''
	user = {}
	# client.send("Email Address:".encode())
	client_email = client.recv(1024).decode()
	if client_email in user_dic:
		client.send("User with email exist! \nPlease enter password to contunue!\n ".encode())
		client_password = client.recv(1024).decode()
		check =  check_existing_user(client_email, client_password) 
		pswd_count = 0
		while check[0] == "P":
			client_password = get_password(client)
			check =  check_existing_user(client_email, client_password) 
			pswd_count += 1
			if pswd_count == 3:
				msg = "Attempt Exceeded! \nPlease Connect to continue."
				close_connections(client,msg,addr)
		if check[0:4] == "True":
			# live_table.append(addr[0])	
			# print(live_table)
			pass
		return client_email
	else:
		client_password = random_password_generator()
		client.send("This is you password : {} \nYou  may require it to login!!\nPress Enter to continue...\n".format(client_password).encode())
		# user = np.array([[client_email, client_password, addr[0], datetime.now().strftime("%d/%m/%Y %H:%M:%S")]])
		user_info = [client_password,addr[0], datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
		user[client_email] = user_info
		user_dic.update(user)
		# live_table.append(addr[0])
		return client_email
	




def client_thread(client, addr):

	client.send(login_msg.encode())
	client_email = signup(client)
	client.send(welcome_msg.encode())

	vote_msg = client.recv(1024).decode()

	if vote_msg == "1" and datetime.now() <= voting_end_time:
		if addr[0] in voted_table:
			sorry_msg = "Vote already regestered for your IP, you cannot vote twice. "
			# client.send(sorry_msg.encode())
			# live_table.remove(addr[0])
			# client.close()
			close_connections(client,sorry_msg, addr)
		else:
			client.send("Password: ".encode())
			password = client.recv(1024).decode()
			pswd_check = check_password(client_email, password)
			if pswd_check == True:
				candidate_msg = "\n===============================\n      List of Candidates\n===============================\n1: Dorendra Odi\n2: Adrusher Baideu\n3: P.K. Iol,\n4: Andi Aul\n5: Riden Oidenn\n===============================\n\nEnter the corresponding number to vote!!"			
				client.send(candidate_msg.encode())
				vote = client.recv(1024).decode()
				vote_count[int(vote)-1] += 1
				voted_table.append(addr[0])
				# print(voted_table)
				closing_msg = "Thank you for participating. Your response is registered against your IP address - {}".format(addr[0])
				# client.send(closing_msg.encode())
				# live_table.remove(addr[0])
				# client.close()
				close_connections(client,closing_msg, addr)
			else:
				err_msg = "Your Password is incorrect!\nConnection Closed!"
				# client.send(err_msg.encode())
				# live_table.remove(addr[0])
				# client.close()
				close_connections(client,err_msg, addr)

	elif vote_msg == "2":
		if datetime.now() <= voting_end_time:
			vote_not_end_msg = "You cannot view the result, voting has not ended! Please check after {}".format(voting_end_time)
			close_connections(client,vote_not_end_msg, addr)

		else:
			client.send("Password: ".encode())
			password = client.recv(1024).decode()
			pswd_check = check_password(client_email, password)
			if pswd_check == True:
				election_result = "\n===============================\n      Voting Results\n===============================\n"
				for key in candidates:
					candidate_vote = vote_count[key-1]
					election_result = election_result + candidates[key] +": "+ str(candidate_vote) + "\n"
				election_result = election_result + "-------------------------------"
				# client.send(election_result.encode())
				# live_table.remove(addr[0])
				# client.close()
				close_connections(client,election_result, addr)
			else:
				err_msg = "Your Password is incorrect!\nConnection Closed!"
				# client.send(err_msg.encode())
				# live_table.remove(addr[0])
				# client.close()
				close_connections(client,err_msg, addr)


	elif vote_msg == "3":
		client.send("Your connection has been closed!!\nThank you for participating!!".encode())
		live_table.remove(addr[0])
		client.close()
	else: 
		client.send("You cannot vote now, voting has closed.".encode())
		live_table.remove(addr[0])
		client.close()



port = 5545
server_ip = "192.196.1.17"
server_ip = socket.gethostbyname(socket.gethostname())  #gethost name gets the local ip for the server
address = (server_ip, port)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(address)

print('Server is running! (IP Address: %s, Port: %s)' % (server_ip, port)) 

server.listen(4)




while True:
	client, addr = server.accept()
	print("Connection from: " + str(addr))
	if addr[0] in live_table:
		client.send("Error! Multiple Users with same IP".encode())
		client.close()
	else:
		live_table.append(addr[0])
		print(live_table)
		start_new_thread(client_thread, (client,addr))
		thread_count += 1
		print('Thread Number: ' + str(thread_count))






	








