import sys


class Parse():
    def __init__(self):
        self.notes = []
        self.bpm = 0
        self.title = ''

    def parse(self, song):
        f = open(song, 'r')
        self.title = f.readline().strip('\n')
        self.bpm = f.readline().strip('\n')

        beat = 0
        start = False
        for line in f:
                note = Note()
                
                for i in range(0, len(line)):
                        if (line[i] != ' ' and start == False): 
                                print line[i]
                                note.freq = line[i]
                                start = True
                        elif line[i] == ':':
                                beat = 0
                        # know we have started the song
                        elif (line[i] != ' ' and line[i] != '\n' and start):
                                beat += 1
                                action = Action(line[i], beat)
                                note.actions.append(action)
                        else: start = False

                self.notes.append(note)
        f.close()


class Note():
    def __init__(self):
        self.freq = ''
        self.actions = []

    def toDictionary(self):
        return {'freq': self.freq,
                'actions': [a.toDictionary() for a in self.actions]}


class Action():
    def __init__(self, action, beat):
        self.start = beat
        self.action = action

    def toDictionary(self):
        return {'start': self.start,
                'action': self.action}


# TODO: clean this up, and decide on some style rules?
def main():
    newSong = Parse()
    song = sys.argv[1]
    newSong.parse(song)
    print newSong.title
    print newSong.bpm
    for i in range(0, len(newSong.notes)):
            print 'freq: ' + newSong.notes[i].freq
            for j in range(0, len(newSong.notes[i].action)):
                    print newSong.notes[i].action[j].action + 'start' + str(newSong.notes[i].action[j].start)

    import os 
    def playsound(frequency, duration):
            os.system('beep -f %s -l %s' % (frequency,duration))

    playsound(100, 2)


if __name__ == '__main__':
    main()
