import argparse
import json
import parse
import socket
import audio
import note_to_freq

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory


class Musician(Protocol):
    def dataReceived(self, data):
        loaded_data = json.loads(data)
        if 'freq' in loaded_data.keys() and 'actions' in loaded_data.keys():
            self.note = parse.Note()
            self.note.freq = loaded_data['freq']
            self.freq = note_to_freq.get_freq(self.note.freq)
            for a in loaded_data['actions']:
                self.note.actions.append(parse.Action(a['action'], a['start']))
            print 'GOT A LETTER: {}'.format(self.note.freq)
            self.play_notes()
        else:
            print loaded_data

    def connectionMade(self):
        self.transport.write(json.dumps({'hostname': socket.gethostname()}))

    def play_notes(self):
        a = audio.Audio()
        i = 0
        while i < len(self.note.actions):
            #TODO: FIX TIME
            hold = 0
            if self.note.actions[i].action != '-':
                if self.note.actions[i].action != 'h':
                    # playing a number of times in one beat
                    times_played = int(self.note.actions[i].action)
                    for j in range(times_played):
                        duration = note_to_freq.get_duration(60, self.note.actions[i].action, hold)
                        reactor.callLater(self.note.actions[i].start + j/times_played, a.play, self.freq, duration)     
                else:
                    # playing a note held over multiple beats
                    while i < len(self.note.actions) and self.note.actions[i].action == 'h':
                        hold += 1
                        i += 1
                    i -= hold
                    duration = note_to_freq.get_duration(60, self.note.actions[i].action, hold)
                    reactor.callLater(self.note.actions[i].start, a.play, self.freq, duration)
                    i += hold
            i += 1

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
