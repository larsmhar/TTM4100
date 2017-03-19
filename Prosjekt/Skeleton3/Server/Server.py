# -*- coding: utf-8 -*-
import socketserver
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        username = ""

        print("Handle funker, for")

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).strip()

            deliverables = {'timestamp': '', 'sender': '', 'response': '', 'content': ''}
            deliverables['timestamp'] = time.strftime("%Y/%m/%d:%H/%M/&S", time.localtime())

            payload = received_string.decode("UTF-8")
            #print(type(payload))
            payload = json.loads(payload)
            #print(type(payload))


            deliverables["sender"] = "server"

            if (payload["request"] == "login") and (username == ""):
                # TODO NOT MULTIKPLE USERNAMES SAME
                username = payload['content']
                #deliverables["sender"] = "server"
                deliverables["response"] = "info"
                deliverables["content"] = "Success"
            elif payload["request"] == "help":
                #deliverables["sender"] = "server"
                deliverables["response"] = "info: login <username>\t"
            elif username == "":
                #payload["sender"] = "server"
                payload['response'] = "error"

            print(deliverables)
            self.connection.send(bytes(json.dumps(deliverables), "UTF-8"))

        """
        received_string2 = received_string.decode("UTF-8")
        print(received_string2)

        print(type(received_string2))
        print(json.loads(received_string.decode("UTF-8")))
        print(type(json.loads(received_string.decode("UTF-8"))))

        # TODO: Add handling of received payload from client

        jsonMessage = json.loads(received_string.decode('UTF-8'))

        response_1 = (received_string.decode("UTF-8"))
        response = json.dumps({'response': 'message', 'message': response_1})
        #response = json.loads(response)
        if "test" in jsonMessage.get("message"):
            print("Detter funker også!")
        self.connection.send(bytes(response, "UTF-8"))
        """
    def send_message(self):
        self.connection.send(bytes("nei"))



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()