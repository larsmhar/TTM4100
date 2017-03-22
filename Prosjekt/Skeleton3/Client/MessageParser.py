import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
            'help': self.parse_help
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return("Not valid response")# Response not valid

    def parse_error(self, payload):
        return("{} ERROR\t: {}".format(payload["timestamp"], payload['content']))


    def parse_info(self, payload):
        return("{} Info\t: {}".format(payload['timestamp'], payload['content']))


    def parse_message(self, payload):
        return("{} {}\t: {}".format(payload["timestamp"], payload["sender"], payload['content']))


    def parse_history(self, payload):
        #return str(type(payload)) + " " + payload["content"][0]
        outstr = ""
        for message in payload["content"]:
            message = json.loads(message)
            #message = json.loads(message)
            #return json.loads(message)["timestamp"], json.loads(message)["sender"], json.loads(message)["content"]
            outstr += "{} {}\t: {}\n".format((message)["timestamp"], (message)["sender"], (message)["content"])
        return outstr
        #return("{} History\t: {}".format(payload['timestamp'], payload['content']))


    def parse_help(self, payload):
        return("{} Help\t: {}".format(payload['timestamp'], payload["content"]))
