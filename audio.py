#Audio.py
#defines play

import sys

class Audio():

	#def __init__(self, freq, duration):
	#	self.freq = freq
	#	self.duration = duration

	def get_play():
		amplitude = 20
		fs = 48000
		try:
			# use pyaudio for osx
			import pyaudio
			def real_play(freq, duration):
				p = pyaudio.PyAudio
				# todo: maybe don't do every time??????????????????????????????????????
				stream = p.open(format=pyaudio.paFloat32, channels=1, 
								rate=fs, output=True)
				N = int(fs / frequency)
				T = int(frequency * duration)  # repeat for T cycles
				dt = 1.0 / fs
				# 1 cycle
				tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
						for n in xrange(N))
				# todo: get the format from the stream; this assumes Float32
				data = ''.join(struct.pack('f', samp) for samp in tone)
				for n in xrange(T):
					stream.write(data)
				stream.close()

			return real_play

		except ImportError:
			try:
				# use winsound for windows
				import winsound
				def real_play(freq, duration):
					winsound.Beep(freq, duration)

				return real_play

			except ImportError:
				# use system calls for lab machines
				def real_play(freq, duration):
					pass

				return real_play 






