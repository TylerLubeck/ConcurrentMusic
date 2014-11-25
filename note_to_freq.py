# Based on C = middle C
# Obtained from http://www.phy.mtu.edu/~suits/notefreqs.html
FREQUENCIES = {'C': 261.63,
               'C#': 277.18, 'Db': 277.18,
               'E': 329.63,
               'F': 349.23,
               'F#': 369.99, 'Gb': 369.99,
               'G': 392.00,
               'G#': 415.30, 'Ab': 415.30,
               'A': 440.00,
               'A#': 466.16, 'Bb': 466.16,
               'B': 493.88}

SCALE_FACTOR = 0.9

class NoSuchNoteError(Exception):
    """Error for signaling that the "note" is not valid."""
    pass


def get_freq(note):
    """Returns the frequency in Hz of the given letter note.
    
    Raises NoSuchNoteError if the given note is badly formed.
    """
    try:
        return FREQUENCIES[note]
    except KeyError:
        raise NoSuchNoteError('Note does not exist: %s' % note)


def get_duration(bpm, plays_in_beat):
    """Returns the duration of a quarter, eighth, etc. note in seconds."""
    duration = 1.0 / float(plays_in_beat) 
    return SCALE_FACTOR * duration * (60.0 / float(bpm))


def get_held_duration(bpm, beats_held):
    """Returns the duration of a half, whole, etc. note in seconds."""
    return SCALE_FACTOR * beats_held * (60.0 / float(bpm))


def get_start_time(bpm, beat_number):
    """Returns the offset from the beginning of the song to play in seconds."""
    return beat_number * (60.0 / float(bpm))

