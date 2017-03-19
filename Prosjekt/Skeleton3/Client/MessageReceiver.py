# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        # TODO: Finish initialization of MessageReceiver
        super(MessageReceiver, self).__init__()
        self.client = client
        self.connection = connection
        self.daemon = True


    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads

        while True:
            message = self.connection.recv(4094)
            if message:
                self.client.receive_message(message.decode("UTF-8"))
        pass
