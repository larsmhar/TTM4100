import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    # More key:values pairs are needed
            'message': self.parse_message,
            'history': self.parse_history,
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return("Not valid response")# Response not valid

    def parse_error(self, payload):
        return("ERROR {}".format(payload['content']))


    def parse_info(self, payload):
        return("Info {} \n{}".format(payload['timestamp'], payload['content']))


    def parse_message(self, payload):
        return("Message {}".format(payload['content']))


    def parse_history(self, payload):
        return("History {} \n{}".format(payload['timestamp'], payload['content']))
    # Include more methods for handling the different responses...
