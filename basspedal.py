"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""
import time
import pyaudio
import wave
import numpy as np
from scipy.io import wavfile
import os
from collections import deque
import random

WIDTH = 2
dtype = 'int' + str(8 * WIDTH)  # 'int16'
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "outputtemp.wav"
# CHUNK = 1024

LOOPING = False
loop_frames = b''
loop_frame_index = 0

# bass_sound_wf = wave.open("AudioFiles/Acoustic Drums-bounce-1.wav", 'rb')
bass_sound_wf = wave.open("AudioFiles/shortbass.wav", 'rb')

p_bass_output = pyaudio.PyAudio()

frames = []

pedal_was_pressed = False


def callback_bass_output(in_data, frame_count, time_info, status):
    data = bass_sound_wf.readframes(frame_count)
    # print('data lenght' + str(len(data)))
    # print(frame_count)
    # if pedal_was_pressed:
    # b'\x00'*frame_count*WIDTH*CHANNELS

    # This causes underruns
    #if len(data) < frame_count*WIDTH*CHANNELS:
        #silence = b'\x00' * (frame_count * WIDTH * CHANNELS - len(data))
        #data = data + silence
    return data, pyaudio.paContinue


stream_bass_output = p_bass_output.open(format=p_bass_output.get_format_from_width(bass_sound_wf.getsampwidth()),
                                        channels=bass_sound_wf.getnchannels(),
                                        rate=bass_sound_wf.getframerate(),
                                        start=False,
                                        output=True,
                                        frames_per_buffer=1024 * 8,
                                        stream_callback=callback_bass_output)

p_pedal_listener = pyaudio.PyAudio()


def callback_pedal_listener(in_data, frame_count, time_info, status):
    global pedal_was_pressed
    frame_size_in_bytes = WIDTH * CHANNELS
    assert len(in_data) % frame_size_in_bytes == 0
    if True:
        # if random.random() > 0.8:
        # print(len(in_data))
        frames.append(in_data)

    one_stereo_channel_values = b''
    for i in range(int(len(in_data) / frame_size_in_bytes)):
        one_stereo_channel_values += in_data[i * frame_size_in_bytes:i * frame_size_in_bytes + WIDTH]
    signal = np.frombuffer(one_stereo_channel_values, dtype='int16')
    # print(signal.__abs__().mean())
    if signal.__abs__().mean() > 50:  # account for some noise
        if not pedal_was_pressed:
            bass_sound_wf.rewind()
            stream_bass_output.stop_stream()
            stream_bass_output.start_stream()
            pedal_was_pressed = True
    else:
        if pedal_was_pressed:
            pedal_was_pressed = False
    return b'\x00' * (frame_count * WIDTH * CHANNELS), pyaudio.paContinue


stream_pedal_listener = p_pedal_listener.open(format=p_pedal_listener.get_format_from_width(WIDTH),
                                              channels=CHANNELS,
                                              rate=RATE,
                                              input=True,
                                              output=True,
                                              frames_per_buffer=1024*2,
                                              stream_callback=callback_pedal_listener)

stream_pedal_listener.start_stream()

# time.sleep(2)
# stream_bass_output.start_stream()


# while stream_bass_output.is_active():
#   time.sleep(0.1)
print("fdsalkfdjaklklfsddsa")

print("stream status")
print(stream_bass_output.is_active())
print(stream_bass_output.is_stopped())

# bass_sound_wf.rewind()
# stream_bass_output.stop_stream()
# stream_bass_output.start_stream()

time.sleep(5*60)
print("--------------------")
stream_pedal_listener.stop_stream()
stream_pedal_listener.close()

stream_bass_output.stop_stream()
stream_bass_output.close()

bass_sound_wf.close()

p_pedal_listener.terminate()
p_bass_output.terminate()

"""wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p_pedal_listener.get_sample_size(p_pedal_listener.get_format_from_width(WIDTH)))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()"""
