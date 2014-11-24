import argparse
import json

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

import parse


class Conductor(Protocol):
    def __init__(self, users, song):
        self.users = users
        self.state = "GETNAME"
        self.song = song
        self.hostname = None

    def connectionMade(self):
        print("GOT A CONNECTION")

    def dataReceived(self, data):
        if self.state == 'GETNAME':
            hostname = json.loads(data)['hostname']
            if hostname in self.users:
                self.transport.write(json.dumps({'error': 'Name in use'}))
                return
            self.hostname = hostname
            note = self.song['song_notes'].pop(0)
            self.users[self.hostname] = {'user': self,
                                         'note': note}
            self.state = 'SENDLETTERS'
        self.transport.write(json.dumps({'note': note}))
        print self.state
        print self.users
        print self.song['song_notes']

    def connectionLost(self, reason):
        if self.hostname is not None and self.hostname in self.users:
            note = self.users[self.hostname]['note']
            del self.users[self.hostname]
            self.song['song_notes'].append(note)


class ConductorFactory(Factory):

    def __init__(self, song):
        self.users = {}     # maps user names to Musician instances
        self.song = song    # object returned by parser

    def buildProtocol(self, addr):
        return Conductor(self.users, self.song)


def main():
    desc = 'Launch the conductor for the distributed music client/server system'
    arg_parser = argparse.ArgumentParser(description=desc)
    arg_parser.add_argument('--port', '-p', dest='port', type=int,
                            default=8123, help='The port to listen on')
    arg_parser.add_argument('--song', '-s', dest='song',
                            help='The file containing the song to play')
    args = arg_parser.parse_args()
    
    parsed_song = parse.parse(args.song)

    print("Listening on port {}...".format(args.port))
    reactor.listenTCP(args.port, ConductorFactory(parsed_song))
    reactor.run()


if __name__ == '__main__':
    main()
