"""PyAudio Example: Play a wave file (callback version)"""

import pyaudio
import wave
import time
import sys
import os

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return data, pyaudio.paContinue


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

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    frames_per_buffer=CHUNK,
                    output_device_index=input_device_index,
                    stream_callback=callback)


else:
    print('Running on pc')

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()
