# TCP-Client-Server-for-Voting-
TCP-Client-Server for Voting  with user authentication.

`multi_server.py`: Voting registered w.r.t ip.    
`multi_server_email.py`: Vote registered w.r.t email. 

### Server 
`port = 5545`  
`ip = 192.168.1.17`

_________________________________________________________________________________________________


# Program Flow 

Global Variables:   
	1. `user_dict = {email: password, ip, time}`: Dictionary to store user info while signup()  
	2. `live_table`: array to store active ip addresses `if connection is closed the ip address gets removed from live_table.`   
	3. `vote_count`: Array to keep track of vote.  
	4. `voted_table`: Array to keep track of IP addresses that have voted.  
	5. `voting_end_time`: 5 mins after the server starts (can be changed from line 49)  

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
