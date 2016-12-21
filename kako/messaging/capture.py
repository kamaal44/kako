import json
import base64


class Capture(object):
    ''' Defines a capture message for submission of results from Kako. '''

    def __init__(self, source_ip, source_port, simulation, capture):
        ''' Generates an object for this capture. '''
        self.source_ip = source_ip
        self.source_port = source_port
        self.simulation = simulation
        self.capture = base64.b64encode('\r\n'.join(str(x) for x in capture))

    def toJSON(self):
        ''' Provide a JSON serializer for this Object. '''
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )