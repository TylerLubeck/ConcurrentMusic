# Based on C = middle C (C4)
# Obtained from http://www.phy.mtu.edu/~suits/notefreqs.html
FREQUENCIES = {'C': 261.63,
               'C#': 277.18, 'Db': 277.18,
               'D': 293.66,
               'D#': 311.13, 'Eb': 311.13,
               'E': 329.63,
               'F': 349.23,
               'F#': 369.99, 'Gb': 369.99,
               'G': 392.00,
               'G#': 415.30, 'Ab': 415.30,
               'A': 440.00,
               'A#': 466.16, 'Bb': 466.16,
               'B': 493.88}
BASE_OCTAVE = 4
SCALE_FACTOR = 0.9

class NoSuchNoteError(Exception):
    """Error for signaling that the "note" is not valid."""
    pass


def get_freq(note):
    """Returns the frequency in Hz of the given letter note.
    
    Raises NoSuchNoteError if the given note is badly formed.
    """
    if not (len(note) == 2 or len(note) == 3):
        raise NoSuchNoteError('Badly formed: %s' % note)
    letter = note[0:-1]
    try:
        octave = int(note[-1])
    except ValueError:
        raise NoSuchNoteError('Badly formed: %s' % note)
    if octave < 0 or octave > 8:
        raise NoSuchNoteError('Octave %d not between 0 and 8; got %s' % octave)
    try:
        base_freq = FREQUENCIES[letter]
    except KeyError:
        raise NoSuchNoteError('Note does not exist: %s' % note)
    # Have valid letter and octave; scale frequency and return
    if octave == BASE_OCTAVE:
        return base_freq
    elif octave < BASE_OCTAVE:
        return get_lower_freq(base_freq, octave)
    else:
        return get_higher_freq(base_freq, octave)


def get_lower_freq(freq, octave):
    """Scales the given frequency to a lower octave."""
    for _ in range(BASE_OCTAVE - octave):
        freq = freq / 2.0
    return freq


def get_higher_freq(freq, octave):
    """Scales the given frequency to a higher octave."""
    for _ in range(octave - BASE_OCTAVE):
        freq = freq * 2.0
    return freq


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

