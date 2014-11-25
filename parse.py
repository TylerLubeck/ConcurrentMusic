import sys
import threading

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
    mutex = threading.Lock()
    threads = [threading.Thread(target=parse_line,
                                args=(line, bpm, parsed_song['song_notes'],
                                      mutex))
               for line in f]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    f.close()
    return parsed_song


def parse_line(line, bpm, note_list, mutex):
    """Parse a particular note in the song. Meant to be used concurrently."""
    note = {'frequency': 0,
            'actions': []}
    line_parts = line.split(':')
    if len(line_parts) != 2:
        return
    # part of line before colon has letter; need to get frequency
    note['frequency'] = note_to_freq.get_freq(line_parts[0])
    line = line_parts[1].strip()
    i = 0
    # build list of actions for note
    while i < len(line):
        holds = 0
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
            start_time = note_to_freq.get_start_time(bpm, i)
            note['actions'].append({'duration': duration,
                                    'start_time': start_time})
            i += holds
        else:
            # playing some number of times in one beat
            times_played = int(action)
            duration = note_to_freq.get_duration(bpm, times_played)
            beat_start_time = note_to_freq.get_start_time(bpm, i)
            for j in range(times_played):
                start_time = beat_start_time + j / float(times_played)
                note['actions'].append({'duration': duration,
                                        'start_time': start_time})
            i += 1
    mutex.acquire()
    note_list.append(note)
    mutex.release()


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
