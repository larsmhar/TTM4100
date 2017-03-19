# -*- coding: utf-8 -*-
import json
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messageReceiver = MessageReceiver(self, self.connection)
        self.messageParser = MessageParser()

        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))

        messageReceiver = MessageReceiver(self, self.connection)

        messageReceiver.start()

        print("her da")
        # Initiate the connection to the server

        #msg, request = "", ""


        #msgReciever = MessageReceiver(self, self.connection)
        print("dette problemet?")
        while 1 != "quit":
            request, msg = input("Message here pls: ").split(" ")
            #print("{}\t{}".format(request, msg))
            send_msg = {"request": "", "content": ""}
            #print(msg)
            send_msg["content"] = msg
            send_msg["request"] = request
            send_msg = json.dumps(send_msg)
            send_msg = json.loads(send_msg)
            #print(type(send_msg), send_msg)
            #self.send_payload(msg)
            self.send_payload(json.dumps(send_msg))
        #self.disconnect()


    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.shutdown(1)
        self.connection.close()
        print("Connection terminated")
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        print("{}\n{}".format(type(message), message))
        #messageParser = MessageParser()
        response = self.messageParser.parse(message)
        print(response)
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload

        self.connection.send(bytes(data, "UTF-8"))
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
