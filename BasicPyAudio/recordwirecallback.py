"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import wave
import os

WIDTH = 3
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

frames = []

p = pyaudio.PyAudio()
# FORMAT = p.get_format_from_width(WIDTH)


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return in_data, pyaudio.paContinue


if os.uname().nodename.lower() == 'raspberrypi':
    print('Running on RaspberryPi')

    #CHUNK = 2048*2  # Higher chunk stopped underrun

    input_device_index = None
    while input_device_index is None:
        time.sleep(0.5)
        info = p.get_host_api_info_by_index(0)
        numDevices = info.get('deviceCount')
        for i in range(0, numDevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                if "irig hd 2" in p.get_device_info_by_host_api_device_index(0, i).get('name').lower():
                    input_device_index = i
                    print("My inpute device is: ", i)

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    output_device_index=input_device_index,
                    stream_callback=callback)
else:
    print('Running on pc')
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)
print(".-.", p.get_default_input_device_info())

stream.start_stream()
print(".-.", p.get_default_input_device_info())

# while stream.is_active():
#    time.sleep(0.1)
time.sleep(5)
stream.stop_stream()
stream.close()

p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(WIDTH)))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
