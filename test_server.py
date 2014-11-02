from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

NOTES = ['A', 'B', 'C', 'D', 'E']
INDEX = 0

class Chat(LineReceiver):
    INDEX = 0

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"
        self.notes = ['A', 'B', 'C', 'D', 'E']
        self.index = 0

    def connectionMade(self):
        print("GOT A CONNECTION")
        self.sendLine("You get {}".format(NOTES[INDEX]))
        Chat.INDEX += 1

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        #for name, protocol in self.users.iteritems():
        #    if protocol != self:
        #        protocol.sendLine("Welcome, %s!" % (name,))
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
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


reactor.listenTCP(8123, ChatFactory())
reactor.run()