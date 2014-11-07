import argparse
import json
import socket

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory


class Musician(Protocol):
    def dataReceived(self, data):
        print data

    def connectionMade(self):
        self.transport.write(json.dumps({'hostname': socket.gethostname()}))


class MusicianClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Musician()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.'

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed.'


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='ip', default='localhost')
    parser.add_argument('-p', '--port', dest='port', type=int, default=8123)
    return parser.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    reactor.connectTCP(args.ip, args.port, MusicianClientFactory())
    reactor.run()
