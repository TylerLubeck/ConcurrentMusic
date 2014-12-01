# Audio.py
# defines play
import threading
import os
from suppress_errors import noalsaerr


class Audio():

    def __init__(self):
        self.play_func = self.get_play()
        self.mutex = threading.Lock()

    def play(self, freq, duration):
        self.mutex.acquire()
        self.play_func(freq, duration)
        self.mutex.release()

    def get_play(self):
        import math
        # amplitude = 0.5
        bit_rate = 16000
        try:
            # use pyaudio for osx
            import pyaudio
            with noalsaerr():
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(1),
                                channels=1,
                                rate=bit_rate,
                                output=True)

            def real_play(freq, duration):
                # p = pyaudio.PyAudio()
                #  TODO: maybe don't do every time?
                # stream = p.open(format=p.get_format_from_width(1),
                #                 channels=1,
                #                 rate=bit_rate,
                #                 output=True)
                os.system('clear')
                rows, columns = os.popen('stty size', 'r').read().split()
                rows = int(rows)
                columns = int(columns)
                for _ in xrange(rows/4): print '\n'
                print "{}".format(freq).center(columns)
                number_of_frames = int(bit_rate * duration)
                rest_frames = number_of_frames % bit_rate
                wavedata = ''
                for x in xrange(number_of_frames):
                    wavedata += chr(int(math.sin(x/((bit_rate/freq)/math.pi))*127+128))

                # for x in xrange(rest_frames):
                #     wavedata += chr(128)

                with noalsaerr():
                    stream.write(wavedata)
            return real_play

        except ImportError, e1:
            try:
                # use winsound for windows
                import winsound

                def real_play(freq, duration):
                    raise e1
                winsound.Beep(freq, duration)

                return real_play

            except ImportError:
                # use system calls for lab machines
                # def real_play(freq, duration):
                #     sample = 8000
                #     half_period = int(sample/freq/2)
                #     beep = chr(amplitude)*half_period+chr(0)*half_period
                #     beep *= int(duration*freq)
                #     audio = file('/dev/audio', 'wb')
                #     audio.write(beep)
                #     audio.close()
                def real_play(freq, duration):
                    print 'CANNOT PLAY ON THIS MACHINE.'

                return real_play


if __name__ == '__main__':
    a = Audio()
    a.play(261.63, 1.2232)
    a.play(261.63, 1.2232)
    a.play(261.63, 1.2232)
    a.play(277.2, 1.2232)
    a.play(293.7, 1.2232)
    a.play(311.1, 1.2232)
    a.play(329.6, 1.2232)
