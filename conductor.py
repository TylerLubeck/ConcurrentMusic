from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import argparse
import json
import parse


class Conductor(Protocol):

    def __init__(self, users, notes=[]):
        self.users = users
        self.state = "GETNAME"
        self.notes = notes
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
            note = self.notes.pop(0)
            self.users[self.hostname] = {'user': self,
                                         'note': note}
            self.state = 'SENDLETTERS'
        self.transport.write(json.dumps(note.toDictionary()))
        print self.state
        print self.users
        print self.notes

    def connectionLost(self, reason):
        if self.hostname is not None and self.hostname in self.users:
            note = self.users[self.hostname]['note']
            del self.users[self.hostname]
            self.notes.append(note)


class ConductorFactory(Factory):

    def __init__(self, notes):
        self.users = {}     # maps user names to Conductor instances
        self.notes = notes  # list of Note objects from parser

    def buildProtocol(self, addr):
        return Conductor(self.users, self.notes)


def main():
    desc = 'Launch the conductor for the distributed music client/server system'
    arg_parser = argparse.ArgumentParser(description=desc)
    arg_parser.add_argument('--port', '-p', dest='port', type=int,
                            default=8123, help='The port to listen on')
    arg_parser.add_argument('--song', '-s', dest='song',
                            help='The file containing the song to play')
    args = arg_parser.parse_args()
    
    song_parser = parse.Parse()
    song_parser.parse(args.song)

    print("Listening on port {}...".format(args.port))
    reactor.listenTCP(args.port, ConductorFactory(song_parser.notes))
    reactor.run()


if __name__ == '__main__':
    main()
