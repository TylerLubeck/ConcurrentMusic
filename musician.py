import argparse
import json
import socket
import time
import os

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
    def __init__(self, *args, **kwargs):
        self.attempts = 10
        # super(MusicianFactory, self).__init__(*args, **kwargs)
        # super(MusicianFactory, self).__init__()
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        self.attempts = 10
        return Musician()

    def clientConnectionLost(self, connector, reason):
        self.attempts -= 1
        if self.attempts > 0:
            time.sleep(1)
            connector.connect()
        else:
            print 'Lost connection.'
            reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        self.attempts -= 1
        if self.attempts > 0:
            time.sleep(1)
            connector.connect()
        else:
            print 'Connection failed.'
            reactor.stop()


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='ip', default='localhost')
    parser.add_argument('-p', '--port', dest='port', type=int, default=8123)
    return parser.parse_args()


if __name__ == '__main__':
    os.system('clear')
    print('\033[40m')
    os.system('clear')
    args = parseArgs()
    reactor.connectTCP(args.ip, args.port, MusicianFactory())
    reactor.run()
    print('\033[47m')
    os.system('clear')
