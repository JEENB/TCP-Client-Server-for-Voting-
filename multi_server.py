'''
Global Variables:
	1> user_dict: Dictionary to store user info while signup()
		{email: password, ip, time}
	2> live_table: array to store active ip addresses
		if connection is closed the ip address gets removed from live_table.
	3> vote_count: Array to keep track of vote. 
		Indices arranged w.r.t candidate list.
	4> voted_table: Array to keep track of IP addresses that have voted.
	5> voting_end_time: 5 mins after the server starts (can be changed from line 49)

Program Flow 
_________________________________________________________________________________________________
Multiple client from same IP check -> Authentication -> Voting / Voting Reult -> Connection Close 
=================================================================================================


Assuming Client is connected, first checks if the client's IP is in live_table (if there exist more than one connection from same IP).
If extra connection exists them the latest connected client disconnects. 

Authentication
1> Enter Ashoka Email address:
	NOTE: vALID EMAIL ENDING WITH "@ASHOKA.EDU.IN" NEEDS TO BE SUPPLIED ELSE EMAIL ERROR. Email Validation is done using regex in client side. 

	- If ashoka_email not in user_info (signup) then generate random password and send to client.
	- If ashoka_email is present in user_info (login) then enter password to login.
			* If password matches with the saved password during signup then step 2
			else client is shown error msg and given 3 extra attempts to login. If client fails to give correct password in the three attempts the clent disconnects.

Voting/ See result
2>  Shows the welcome msg with 1/2/3 options.
	
	Option 1
		- Given voting is live and client IP not in voted_table(client has not voted), allows the client to vote. Else disconnects with voting ended msg or client has already voted msg.
		Note: The client has to give password to vote. If password does not match the session ends else vote gets recored.
	
	Option 2
		- If voting is still live, connection closes. else client can give the password and see voting result given password matches.

	Option 3
		- Session Ends. 
'''



import socket
from _thread import *
from datetime import datetime, timedelta
import re
import random
import string


thread_count = 0
# voting end time set to 5 min after start of the server
voting_end_time = datetime.now() + timedelta(minutes=5)   #================ Change timedelta Here ========================

#user_table: (email, pswd, ip, time) stores the signup credentials
#live_table: (Email,Client_IP,Live_Time,Port) keeps record of active connections
global user_table, live_table, user_dic, vote_count, voted_table


# user_table = np.empty(shape=(0,4))
live_table = []

voted_table = []  # stores the ip of clients who have voted

vote_count = [0,0,0,0,0]

user_dic = dict()


candidates = {1: "Dorendra Odi", 2: "Adrusher Baideu", 3: "P.K. Iol", 4:"Andi Aul", 5: "Riden Oiden"}

login_msg = "Welcome! Please enter your ashoka email to continue!!\n\nEmail Address:"

welcome_msg = "Welcome! You can participant in the vote by presenting your password. Reply with a \"1\" if you want to participate now; with a \"2\" if you want to see the results; and with \"3\" other wise."

def random_password_generator(length=10):
	'''Func: random_password_generator
	args: Lenght: length of password. Defalult set to 10.
	returns:
		random passowrd of lenght 10'''
	alphabets = string.ascii_letters + string.digits
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
	'''
	function: close_connections
	args: msg, addr
	Closes the client socket. 
	Sends closing msg to client and removes client from live_table. 
	'''
	client.send(msg.encode())
	live_table.remove(addr[0])
	client.close()

def check_password(email,password):
	'''
	function: check_password
	args: email, password
	Indexes user_dic with key = email and checks if password in user_dic == password entered
	returns: True if password matches else False
	
	'''
	pswd = user_dic[email][0]
	if pswd == password:
		return True
	else:
		return False

def get_password(client,n):
	'''function: get_password
	args: n -> Total attempts for password 
	Gets the password from user if "Password Error" encountered.
	Only runs when user tries to login.
	'''
	# client.send("Email Address:".encode())
	# client_email = client.recv(1024).decode()
	client.send("Password Error! {} attempts remaining\nPassword: ".format(n).encode())
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
		client.send("User with email exist! \nPlease enter password to contunue!\nPassword:".encode())
		client_password = client.recv(1024).decode()
		check =  check_existing_user(client_email, client_password) 
		pswd_count = 0
		n = 3
		while check[0] == "P":
			client_password = get_password(client,n)
			n -= 1
			check =  check_existing_user(client_email, client_password) 
			pswd_count += 1
			if pswd_count == 3:
				msg = "Attempt for Password Exceeded! \nDisconnecting..."
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