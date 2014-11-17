# Audio.py
# defines play


class Audio():

    def __init__(self):
        self.play = self.get_play()

    def get_play(self):
        import math
        # amplitude = 0.5
        bit_rate = 16000
        try:
            # use pyaudio for osx
            import pyaudio

            def real_play(freq, duration):
                p = pyaudio.PyAudio()
                # TODO: maybe don't do every time?
                stream = p.open(format=p.get_format_from_width(1),
                                channels=1,
                                rate=bit_rate,
                                output=True)
                number_of_frames = int(bit_rate * duration)
                rest_frames = number_of_frames % bit_rate
                wavedata = ''
                for x in xrange(number_of_frames):
                    wavedata += chr(int(math.sin(x/((bit_rate/freq)/math.pi))*127+128))

                for x in xrange(rest_frames):
                    wavedata += chr(128)

                stream.write(wavedata)
                stream.stop_stream()
                stream.close()
                p.terminate()
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
    a.play(261.63, 1.2232)
    a.play(277.2, 1.2232)
    a.play(293.7, 1.2232)
    a.play(311.1, 1.2232)
    a.play(329.6, 1.2232)


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
