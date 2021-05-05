"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import os

WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    return in_data, pyaudio.paContinue


if os.uname().nodename.lower() == 'raspberrypi':
    print('Running on RaspberryPi')

    CHUNK = 2048*2  # Higher chunk stopped underrun

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

    # TODO(Examine): If running on Pi, needs either frame_per_buffer or output_device_index \
    #  Why does either work? What's the difference?
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    #frames_per_buffer=CHUNK,
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

stream.start_stream()

# while stream.is_active():
#    time.sleep(0.1)
time.sleep(5)
stream.stop_stream()
stream.close()

p.terminate()
