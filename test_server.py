from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import argparse
import json


NOTES = ['A', 'B', 'C', 'D', 'E']
INDEX = 0


class Chat(Protocol):

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
        self.transport.write(json.dumps({'note': note}))
        print self.state
        print self.users
        print self.notes

    def connectionLost(self, reason):
        if self.hostname is not None and self.hostname in self.users:
            note = self.users[self.hostname]['note']
            del self.users[self.hostname]
            self.notes.append(note)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users, NOTES)


def main():
    desc = 'Launch the conductor for the distributed music client/server system'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--port', '-p', dest='port', type=int,
                        default=8123, help='The port to listen on')
    args = parser.parse_args()

    print("Listening on port {}...".format(args.port))
    reactor.listenTCP(args.port, ChatFactory())
    reactor.run()


if __name__ == '__main__':
    main()
