"""

"""
import os
import pyaudio
import wave
import time


dtype = 'int16'

wf = wave.open('AudioFiles/demolition.wav', 'rb')
wf2 = wave.open('AudioFiles/watchtower.wav', 'rb')

p = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)

    silence = bytes(
        [0 for i in range(frame_count * (wf.getsampwidth()) * wf.getnchannels())]
    )
    assert len(data) == len(silence)
    assert type(data) == type(silence)
    return data, pyaudio.paContinue


def callback2(in_data, frame_count, time_info, status):
    data = wf2.readframes(frame_count)

    return data, pyaudio.paContinue

print(p.get_format_from_width(wf.getsampwidth()))


if os.uname().nodename.lower() == 'raspberrypi':
    print('Running on RaspberryPi')

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

    CHUNK = 2048*2  # Higher chunk stopped underrun

    # TODO(BUG): OSError: [Errno -9985] Device unavailable when opening 2 streams and setting output_device_index
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    start=False,
                    frames_per_buffer=CHUNK,
                    #output_device_index=input_device_index,
                    stream_callback=callback)

    stream2 = p2.open(format=p2.get_format_from_width(wf2.getsampwidth()),
                      channels=wf2.getnchannels(),
                      rate=wf2.getframerate(),
                      output=True,
                      start=False,
                      frames_per_buffer=CHUNK,
                      #output_device_index=input_device_index,
                      stream_callback=callback2)


else:
    print('Running on pc')
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
#stream.stop_stream()
#wf.rewind()
#time.sleep(1)
#stream.start_stream()
stream2.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()
p.terminate()

stream2.stop_stream()
stream2.close()
wf2.close()
p2.terminate()
