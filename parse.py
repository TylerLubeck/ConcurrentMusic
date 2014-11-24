import sys

import note_to_freq


def parse(song):
    """Parses a song given in a text file into a set of notes and when to play.

    The structure returned by this method is as follows:
        {'title': string,
         'bpm': int,
         'song_notes': [{'frequency': float,
                         'actions': [{'duration': float,
                                      'start_time': float}]}]}

    The duration of an action is in seconds, and the start_time is in seconds
    from the beginning of the song.
    """
    f = open(song, 'r')
    title = f.readline().strip('\n'),
    bpm = int(f.readline().strip('\n'))
    parsed_song = {'title': title,
                   'bpm': bpm,
                   'song_notes': []}
    beat = 0
    start = False
    for line in f:
        note = {'frequency': 0,
                'actions': []}
        i = 0
        while i < len(line):
            holds = 0
            if (line[i] != ' ' and start == False):
                # found new note ('A', 'B', etc.)
                note['frequency'] = note_to_freq.get_freq(line[i])
                start = True
                i += 1
            elif line[i] == ':':
                beat = 0
                i += 1
            elif (line[i] != ' ' and line[i] != '\n' and start):
                # know we have started the song
                beat += 1
                action = line[i]
                if action == '-':
                    # not playing, do nothing
                    i += 1
                elif action == 'h':
                    # playing note held over multiple beats
                    while i < len(line) and line[i] == 'h':
                        holds += 1
                        i += 1
                    i -= holds
                    duration = note_to_freq.get_held_duration(bpm, holds)
                    start_time = note_to_freq.get_start_time(bpm, beat)
                    note['actions'].append({'duration': duration,
                                            'start_time': start_time})
                    i += holds
                else:
                    # playing some number of times in one beat
                    times_played = int(action)
                    duration = note_to_freq.get_duration(bpm, times_played)
                    beat_start_time = note_to_freq.get_start_time(bpm, beat)
                    for j in range(times_played):
                        start_time = beat_start_time + j / float(times_played)
                        note['actions'].append({'duration': duration,
                                                'start_time': start_time})
                    i += 1
            else:
                start = False
                i += 1
        parsed_song['song_notes'].append(note)
    f.close()
    return parsed_song


def main():
    parsed_song = parse(sys.argv[1])
    print 'title: %s' % parsed_song['title']
    print 'bpm: %d' % parsed_song['bpm']
    print 'song notes:'
    for note in parsed_song['song_notes']:
        print '\tfrequency: %.1f' % note['frequency']
        print '\tactions:'
        for action in note['actions']:
            print ('\t\tstart time: %.1f\tduration: %.1f' %
                   (action['start_time'], action['duration']))


if __name__ == '__main__':
    main()
