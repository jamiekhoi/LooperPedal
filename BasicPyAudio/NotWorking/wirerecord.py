"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""

"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

"""
TODO: fix underrun occurred error alsa on pc. records correctly though
"""

import pyaudio
import wave

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "../../output.wav"

p = pyaudio.PyAudio()

FORMAT = p.get_format_from_width(WIDTH)
FORMAT = pyaudio.paInt24

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    stream.write(data, CHUNK)
    frames.append(data)

print("* done")

stream.stop_stream()
stream.close()

p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
