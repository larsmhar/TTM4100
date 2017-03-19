# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

import time
from socket import *

# Get the server hostname and port as command line arguments                    
host = "localhost"  # FILL IN START	 	# FILL IN END
port = 12000    # FILL IN START		# FILL IN END
timeout = 1  # in seconds

# Create UDP client socket
# FILL IN START		

clientSocket = socket(AF_INET, SOCK_DGRAM)

# Note the second parameter is NOT SOCK_STREAM
# but the corresponding to UDP

# Set socket timeout as 1 second

clientSocket.settimeout(timeout)

# FILL IN END

# Sequence number of the ping message
ptime = 0

ptimes = []

serverAddress = ""
total = 0

# Ping for 10 times
while ptime < 10:
    ptime += 1
    # Format the message to be sent as in the Lab description	
    data = bytes(str(ptime), encoding="UTF-8")  # FILL IN START		# FILL IN END


    try:
        # FILL IN START

        # Record the "sent time"
        sentTime = time.time()
        message = bytes(("Ping {} {:.2f}".format(ptime, sentTime)), encoding="UTF-8")
        # Send the UDP packet with the ping message
        clientSocket.sendto(message, (host, port))
        # Receive the server response
        message, serverAddress = clientSocket.recvfrom(1024)
        # Record the "received time"
        recvTime = time.time()
        # Display the server response as an output
        #print(message.decode("UTF-8"), end="")
        # Round trip time is the difference between sent and received time
        theTime = (recvTime - sentTime) * 1000
        print(message.decode("UTF-8") + ". RTT: {:.2f}ms".format(theTime))
        ptimes.append(theTime)
        # FILL IN END
    except Exception as e:
        # Server does not response
        # Assume the packet is lost
        print("Request timed out.")
        continue

# Close the client socket
clientSocket.close()

for thing in ptimes:
    total += thing
average = total / ptime

try:
    print("\nPing statistics for {}:\n\tPackets: Sent {}, Recieved {}, Lost: {} ({:.2f}% loss),\nApproximate round trip times in milli-seconds:\n\tMinimum = {:.2f}ms, Maximum = {:.2f}ms, Average = {:.2f}ms"
      .format(str(serverAddress[0]), ptime, len(ptimes), ptime - len(ptimes), (ptime - len(ptimes)) / ptime * 100, min(ptimes), max(ptimes), average))
except:
    print("No information was logged")
