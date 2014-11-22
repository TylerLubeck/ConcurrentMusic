
FREQUENCIES = {'A': 440.0, 'B': 493.9, 'C': 261.6, 'D': 293.7, 
               'E': 329.6, 'F': 349.2, 'G': 392.0};

def get_freq(note):
	return FREQUENCIES[note]

def get_duration(bpm, length, hold):
	#pass in number of holds?
	if length != 'h':
		duration = 1.0/float(int(length))
	else:
		duration = hold

	return float((60 / bpm) * duration)

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