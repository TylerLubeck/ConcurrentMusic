from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import argparse


NOTES = ['A', 'B', 'C', 'D', 'E']
INDEX = 0


class Chat(LineReceiver):
    INDEX = 0

    def __init__(self, users):
        # TODO: Link connection to connected computers hostname
        self.users = users
        self.name = None
        self.state = "GETNAME"
        self.notes = ['A', 'B', 'C', 'D', 'E']
        self.index = 0

    def connectionMade(self):
        print("GOT A CONNECTION")
        self.sendLine("You get {}".format(NOTES[Chat.INDEX]))
        Chat.INDEX += 1
        self.state = "CHAT"
        self.name = 'jon'
        self.users[self.name] = self

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]
            # TODO: Link connection to letter rather than assume that
            #       most recent connection is the one that drops off.
            Chat.INDEX -= 1

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        # for name, protocol in self.users.iteritems():
        #     if protocol != self:
        #         protocol.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


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
