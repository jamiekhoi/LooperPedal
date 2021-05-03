"""

"""
from copy import copy

import numpy as np
import pyaudio
import wave
import time
import sys

dtype = 'int16'

wf = wave.open('../AudioFiles/demolition.wav', 'rb')
wf2 = wave.open('../AudioFiles/watchtower.wav', 'rb')

p = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()


def dummyMixFaster():
    """
    0.003111600875854492 not looping
    3.5762786865234375e-06 looping
    """
    decodeddata1 = copy(np.frombuffer(bytes(6124), dtype=dtype))
    decodeddata2 = copy(np.frombuffer(bytes(6124), dtype=dtype))
    len(bytes(6124))
    len(decodeddata1)
    # This opperation is too slow making the noise garbage
    # (decodeddata1 * 0.8).astype(int).tobytes()
    # trying new method
    for byte in bytes(33000):
        (byte)
        (bytes([int(byte * 0.8)]))


def changeVolume(in_data, percent=0.9):
    decodeddata1 = copy(np.frombuffer(in_data, dtype=dtype))

    return (decodeddata1 * percent).astype(int).tobytes()


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    #print(type(in_data))
    print(frame_count)
    print()
    start = time.time()
    # dummyMixFaster()
    # changeVolume(data, 0.95)
    # time.sleep(0.00946) # 0.010182619094848633 #1000 bytes in dummy
    end = time.time()
    #print(end - start)

    silence = bytes(
        [0 for i in range(frame_count * (wf.getsampwidth()) * wf.getnchannels())]
    )
    assert len(data) == len(silence)
    assert type(data) == type(silence)
    return silence, pyaudio.paContinue


def callback2(in_data, frame_count, time_info, status):
    data = wf2.readframes(frame_count)

    start = time.time()
    # dummyMixFaster()
    # changeVolume(data, 0.95)
    # time.sleep(0.00946) # 0.010182619094848633 #1000 bytes in dummy
    end = time.time()
    print(end - start)

    return data, pyaudio.paContinue

print(p.get_format_from_width(wf.getsampwidth()))

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                start=False,
                stream_callback=callback)

stream2 = p2.open(format=p2.get_format_from_width(wf2.getsampwidth()),
                  channels=wf2.getnchannels(),
                  rate=wf2.getframerate(),
                  output=True,
                  start=False,
                  stream_callback=callback2)

stream.start_stream()
time.sleep(2)
stream.stop_stream()
wf.rewind()
time.sleep(1)
stream.start_stream()
#stream2.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()
