#Audio.py
#defines play

import sys

class Audio():

    def __init__(self):
        self.play = self.get_play()

    def get_play(self):
        import math
        import struct
        amplitude = 0.5
        fs = 48000
        try:
            # use pyaudio for osx
            import pyaudio
            def real_play(freq, duration):
                p = pyaudio.PyAudio()
                # todo: maybe don't do every time??????????????????????????????????????
                stream = p.open(format=pyaudio.paFloat32, channels=1,
                                rate=fs, output=True)
                N = int(fs / freq)
                T = int(freq * duration)  # repeat for T cycles
                dt = 1.0 / fs
                # 1 cycle
                tone = (amplitude * math.sin(2 * math.pi * freq * n * dt)
                        for n in xrange(N))
                # todo: get the format from the stream; this assumes Float32
                data = ''.join(struct.pack('f', samp) for samp in tone)
                for n in xrange(T):
                    stream.write(data)
                stream.close()
                print('Play!')

            return real_play

        except ImportError, e1:
            try:
                # use winsound for windows
                import winsound
                def real_play(freq, duration):
                    raise e1
                    winsound.Beep(freq, duration)

                return real_play

            except ImportError, e2:
                # use system calls for lab machines
                def real_play(freq, duration):
                	sample = 8000
                    half_period = int(sample/frequency/2)
                    beep = chr(amplitude)*half_period+chr(0)*half_period
                    beep *= int(duration*frequency)
                    audio = file('/dev/audio', 'wb')
                    audio.write(beep)
                    audio.close()

                return real_play


if __name__ == '__main__':
    a = Audio()
    a.play(10, 10)


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


