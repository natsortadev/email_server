from socket import *
import ssl
import base64

print('''
    \n
   ▄████████ ███    █▄     ▄███████▄  ▄█    ▄▄▄▄███▄▄▄▄      ▄███████▄    ▄████████ 
  ███    ███ ███    ███   ███    ███ ███  ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███ 
  ███    █▀  ███    ███   ███    ███ ███▌ ███   ███   ███   ███    ███   ███    ███ 
  ███        ███    ███   ███    ███ ███▌ ███   ███   ███   ███    ███   ███    ███ 
▀███████████ ███    ███ ▀█████████▀  ███▌ ███   ███   ███ ▀█████████▀  ▀███████████ 
         ███ ███    ███   ███        ███  ███   ███   ███   ███          ███    ███ 
   ▄█    ███ ███    ███   ███        ███  ███   ███   ███   ███          ███    ███ 
 ▄████████▀  ████████▀   ▄████▀      █▀    ▀█   ███   █▀   ▄████▀        ███    █▀  
	\n
      ''')
print("Bem-vindo(a) ao serviço de emails Sumpimpa.net!")

# Credentials
sender = username = input("Digite seu email:\n> ")
password = input("Insira a senha de app associada ao email inserido previamente:\n> ") 

receiver = input("Digite o email do destinatário:\n> ")
subject = input("Assunto:\n> ")
body = input("Texto do email:\n> ")

# Message to send
msg = (
	f"From: {sender}\r\n"
    f"To: {receiver}\r\n"
    f"Subject: {subject}\r\n"
    "\r\n"
    f"{body}\r\n"
)
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)

# Port number may change according to the mail server
clientSocket.connect((mailserver, 587))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
	print('220 reply not received from server.') ##

# Send HELO command and print server response.
heloCommand = "HELO gmail.com\r\n"
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
	print('250 reply not received from server.')

# Send email
starttlsCommand = "STARTTLS\r\n"
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received from server.')

context = ssl.create_default_context()
secureSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

secureSocket.send(heloCommand.encode())
recv1b = secureSocket.recv(1024).decode()
print(recv1b)
if recv1[:3] != '250':
	print('250 reply not received from server.')

authCommand = "AUTH LOGIN\r\n"
secureSocket.send(authCommand.encode())
recv3 = secureSocket.recv(1024).decode()
print(recv3)

encoded_username = base64.b64encode(username.encode()).decode()
secureSocket.send((encoded_username + '\r\n').encode())
recv3b = secureSocket.recv(1024).decode()
print(recv3b)

encoded_password = base64.b64encode(password.encode()).decode()
secureSocket.send((encoded_password + '\r\n').encode())
recv3c = secureSocket.recv(1024).decode()
print(recv3c)

mailfrom = f"MAIL FROM: <{sender}>\r\n"
secureSocket.send(mailfrom.encode())
recv3d = secureSocket.recv(1024).decode()
print(recv3d)
if recv3d[:3] != '250':
    print('250 reply not received from server.')
    
rcptto = f"RCPT TO: <{receiver}>\r\n"
secureSocket.send(rcptto.encode())
recv3e = secureSocket.recv(1024).decode()
print(recv3e)
if recv3e[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response. 
data = 'DATA\r\n'
secureSocket.send(data.encode())
recv4 = secureSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
	print('354 reply not received from server.') ##

# Send message data
secureSocket.send(msg.encode())
secureSocket.send(endmsg.encode())

recv5 = secureSocket.recv(1024).decode(errors='replace')
print(recv5) # Cannot Decode response
if recv5[:3] != '250':
	print('250 reply not received from server.')

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
secureSocket.send(quitcommand.encode())
recv6 = secureSocket.recv(1024).decode()
print(recv6) # Unrecognized command
if recv6[:3] != '221':
	print('221 reply not received from server.') ##

secureSocket.close()
