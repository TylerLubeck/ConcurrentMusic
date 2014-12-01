import argparse
import json
import socket

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from datetime import datetime, timedelta

import audio
import note_to_freq
import parse



class Musician(Protocol):
    def __init__(self):
        self.state = 'GETNOTE'
        self.time = datetime.now()
        self.note = None

    def dataReceived(self, data):
        if self.state == 'GETNOTE':
            loaded_data = json.loads(data)
            if 'note' in loaded_data.keys():
                self.note = loaded_data['note']
                print 'GOT A NOTE: {}'.format(self.note['frequency'])
                self.state = 'READY'
                self.transport.write('ready')
        elif data == 'start':
            self.play_notes()

    def connectionMade(self):
        self.transport.write(json.dumps({'hostname': socket.gethostname()}))

    def play_notes(self):
        a = audio.Audio()
        for action in self.note['actions']:
            reactor.callLater(action['start_time'], a.play,
                              self.note['frequency'], action['duration'])     
            

class MusicianFactory(ClientFactory):
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
    reactor.connectTCP(args.ip, args.port, MusicianFactory())
    reactor.run()
