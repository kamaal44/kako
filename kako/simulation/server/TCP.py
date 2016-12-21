import logging
import SocketServer

from kako import messaging
from kako.simulation.server import Error


class RequestHandler(SocketServer.BaseRequestHandler):
    ''' Implements TCP handling for client connections. '''

    def __init__(self, request, client_address, server):
        ''' Bolt on a logger to push messages back to Kako. '''
        self.log = logging.getLogger()
        self.buffer = []
        self.record = []

        SocketServer.BaseRequestHandler.__init__(
            self, request, client_address, server
        )

    def write(self, message):
        ''' Writes to the socket. '''
        self.request.sendall(message)

    def read(self, length):
        ''' Reads from the socket into the record and build a byte-array. '''
        raw = self.request.recv(length)
        if raw == '':
            raise Error.ClientDisconnect()

        self.record.append(raw)
        self.buffer = map(ord, list(raw))

    def capture(self):
        ''' Implements 'capture' functionality for identified requests. '''
        msg = messaging.capture.Capture(
            capture=self.record,
            source_ip=self.client_address[0],
            source_port=self.client_address[1],
            simulation='x'
        )
        self.log.info(msg.toJSON())
        return True


class Server(SocketServer.ThreadingTCPServer):
    ''' Extends SocketServer ThreadingTCPServer to provide configuration. '''

    def __init__(self, server_address, RequestHandlerClass, configuration):
        SocketServer.ThreadingTCPServer.__init__(
            self, server_address, RequestHandlerClass
        )
        self.configuration = configuration
