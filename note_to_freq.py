FREQUENCIES = {'A': 440.0, 'B': 493.9, 'C': 261.6, 'D': 293.7, 
               'E': 329.6, 'F': 349.2, 'G': 392.0};
SCALE_FACTOR = 0.9

def get_freq(note):
    """Returns the frequency in Hz of the given letter note."""
    return FREQUENCIES[note]


def get_duration(bpm, plays_in_beat):
    """Returns the duration of a quarter, eighth, etc. note in seconds."""
    duration = 1.0 / float(plays_in_beat) 
    return SCALE_FACTOR * duration * (60.0 / bpm)


def get_held_duration(bpm, beats_held):
    """Returns the duration of a half, whole, etc. note in seconds."""
    return SCALE_FACTOR * beats_held * (60.0 / bpm)


def get_start_time(bpm, beat_number):
    """Returns the offset from the beginning of the song to play in seconds."""
    return beat_number * (60.0 / bpm)

#C         261.6
#C#        277.2
#D         293.7
#D#        311.1
#E         329.6
#F         349.2
#F#        370.0
#G         392.0
#G#        415.3
#A         440.0
#A#        466.2
#B         493.9
#C         523.2
