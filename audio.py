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
                    raise e2
                    pass

                return real_play


if __name__ == '__main__':
    a = Audio()
    a.play(10, 10)
