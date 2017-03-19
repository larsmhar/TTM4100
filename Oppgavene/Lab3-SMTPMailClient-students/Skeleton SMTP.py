# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

from socket import *

# Message to send
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Our mail server is smtp.stud.ntnu.no
mailserver = 'smtp.stud.ntnu.no'

# Create socket called clientSocket and establish a TCP connection 
# (use the appropriate port) with mailserver
# Fill in start

serverPort = 25
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))

#clientSocket.ehlo()
#clientSocket.starttls()
#clientSocket.ehlo()


# Fill in end

recv = clientSocket.recv(1024)
print(recv.decode("UTF-8"))
if (recv[:3]).decode("UTF-8") != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(bytes(heloCommand, encoding="UTF-8"))
recv1 = clientSocket.recv(1024)
print(recv1.decode("UTF-8"))
if (recv1[:3]).decode("UTF-8") != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start



clientSocket.send(bytes("MAIL From: lars@ntnu.no\r\n", encoding="UTF-8"))
print("HYLLE?" + clientSocket.recv(1024).decode("UTF-8") + "MAILFROM")

# Fill in end

# Send RCPT TO command and print server response.
# Fill in start

clientSocket.send(bytes("RCPT To: larsmhar@stud.ntnu.no\r\n", encoding="UTF-8"))
print(clientSocket.recv(1024).decode("UTF-8") + "RCPTTO")

# Fill in end

# Send DATA command and print server response.
# Fill in start

clientSocket.send(bytes("DATA\r\n", encoding="UTF-8"))
print(clientSocket.recv(1024).decode("UTF-8"))

# Fill in end

# Send message data.
# Fill in start

clientSocket.send(bytes(msg, encoding="UTF-8"))
print(clientSocket.recv(1024).decode("UTF-8"))

# Fill in end

# Message ends with a single period.
# Fill in start

clientSocket.send(bytes(endmsg, encoding="UTF-8"))
print(clientSocket.recv(1024).decode("UTF-8"))

# Fill in end

# Send QUIT command and get server response.
# Fill in start

clientSocket.send(bytes("QUIT\n", encoding="UTF-8"))

print(clientSocket.recv(1024).decode("UTF-8"))
# Fill in end
