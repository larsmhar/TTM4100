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
        self.messageParser = MessageParser()

        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))
        messageReceiver = MessageReceiver(self, self.connection)
        messageReceiver.start()

        request = ""



        print(">>", end="")
        while True:
            msg = input("")
            request = msg.split(" ")[0]
            if request == "help":
                self.send_help()
            elif request == "logout":
                self.send_logout()
                break
            elif request == "login":
                username = msg.split(" ")[1]
                self.send_login(username)
            elif request == "names":
                self.send_names()
            elif request == "msg":
                self.send_msg(msg)
            else:
                print("Not a valid command")

        self.disconnect()

    def get_input(self):
        while True:
            msg = input("\n>>")
            request = msg.split(" ")[0]
            if request == "help":
                self.send_help()
            elif request == "logout":
                self.send_logout()
                break
            elif request == "login":
                username = msg.split(" ")[1]
                self.send_login(username)
            elif request == "names":
                self.send_names()
            elif request == "msg":
                self.send_msg(msg)
            else:
                print("Not a valid command")

        self.disconnect()

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.shutdown(1)
        self.connection.close()
        print("Connection terminated")
        pass


    def receive_message(self, message):
        response = self.messageParser.parse(message)
        print("{}\n>>".format(response), end="")
        pass


    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(bytes(data, "UTF-8"))
        pass
        

    def send_login(self, username):
        request = self.make_request("login", username)
        self.send_payload(request)


    def send_logout(self):
        request = self.make_request("logout")
        self.send_payload(request)


    def send_msg(self, msg):
        request = self.make_request("msg", msg)
        self.send_payload(request)


    def send_help(self):
        request = self.make_request("help")
        self.send_payload(request)


    def send_names(self):
        request = self.make_request("names")
        self.send_payload(request)

    def send_messages(self):
        request = self.make_request("messages")
        self.send_payload(request)

    def make_request(self, request, content=""):
        return json.dumps({"request": request, "content": content})

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
