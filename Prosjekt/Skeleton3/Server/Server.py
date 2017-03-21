# -*- coding: utf-8 -*-
import socketserver
import json
import re
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_users = {}
message_history = {}

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

        self.username = ""

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).strip()

            deliverables = {'timestamp': '', 'sender': '', 'response': '', 'content': ''}
            deliverables['timestamp'] = time.strftime("%Y/%m/%d:%H/%M/%S", time.localtime())

            payload = received_string.decode("UTF-8")
            print(payload)
            payload = json.loads(payload)

            #TODO LEGG TIL Å SENDE MESSAGE TIL ALLE TILKNYTTET

            deliverables["sender"] = "server"
            print(message_history)
            print(connected_users)
            if (payload["request"] in connected_users and payload["request"] == "login"):
                    deliverables["response"] = "error"
                    deliverables["content"] = "Failure, duplicate username"
            elif payload["request"] == "login" and self.username == "" and self.accepted_username(payload["content"]):
                self.username = payload['content']
                print(payload["request"] + " " + self.username)
                connected_users[self.username] = self
                deliverables["response"] = "info"
                deliverables["content"] = "Success"
            elif payload["request"] == "help":
                deliverables["content"] = "Commands: login <username>, help, names, logout, msg <message>"
            elif self.username == "":
                payload['response'] = "error"
            elif  payload["request"] == "messages":
                deliverables["content"] = message_history

            if payload["request"] == "logout":
                connected_users.pop(self.username)
                self.username = ""
                break
            else:
                message = payload["content"]
                #TODO CREATE RESPONSE
                deliverables["sender"] = self.username
                deliverables["response"] = "message"
                deliverables["content"] = message
                self.broadcast_response(deliverables)

        self.connection.close()

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
    def send_message(self, message):
        self.connection.send(bytes(message, "UTF-8"))

    def accepted_username(self, username):
        # Finn ut r og f re
        if re.fullmatch("[a-zA-Z0-9]{1,16}", username) and (username not in connected_users.keys()):
            return True
        else:
            return False

    def broadcast_response(self, response):
        for connection in connected_users.items():
            json_response = json.dumps(response)
            print(connection, json_response)
            connection[1].send_message(json_response)



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
