"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""
import time
import pyaudio
import wave
import os

WIDTH = 2
dtype = 'int' + str(8*WIDTH)  # 'int16'
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
#CHUNK = 1024

LOOPING = False
loop_frames = b''
loop_frame_index = 0

p_liveStream = pyaudio.PyAudio()
# FORMAT = p.get_format_from_width(WIDTH)
p_loopSectionStream = pyaudio.PyAudio()


def save_loop():  # Save loop
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(WIDTH)
    wf.setframerate(RATE)
    wf.writeframes(loop_frames)
    wf.close()


def live_bypass_callback(in_data, frame_count, time_info, status):
    return in_data, pyaudio.paContinue


def loop_section_callback(in_data, frame_count, time_info, status):
    global loop_frames, loop_frame_index
    loop_section_length = len(in_data)  # = frame_count * CHANNELS * WIDTH
    assert len(in_data) == frame_count * CHANNELS * WIDTH

    if LOOPING:
        loop_frames += in_data
        out_data = bytes([0 for _ in range(frame_count * WIDTH * CHANNELS)])
    else:
        if len(loop_frames) > 0:
            # Playback Loop
            if loop_frame_index + loop_section_length < len(loop_frames) - 1:
                loop_section = loop_frames[loop_frame_index:loop_frame_index + loop_section_length]
                loop_frame_index += loop_section_length
            else:
                new_loop_frame_index = loop_frame_index + loop_section_length - len(loop_frames)
                loop_section = loop_frames[loop_frame_index:] + loop_frames[:new_loop_frame_index]
                loop_frame_index = new_loop_frame_index

            out_data = loop_section

        else:
            out_data = bytes([0 for _ in range(frame_count * WIDTH * CHANNELS)])

    return out_data, pyaudio.paContinue


def live_bypass_callback2(in_data, frame_count, time_info, status):
    global loop_frames
    assert len(in_data) == frame_count * CHANNELS * WIDTH

    if LOOPING:
        loop_frames += in_data

    return in_data, pyaudio.paContinue


def loop_section_callback2(in_data, frame_count, time_info, status):
    global loop_frames, loop_frame_index
    loop_section_length = frame_count * CHANNELS * WIDTH

    if LOOPING:
        out_data = bytes([0 for _ in range(frame_count * WIDTH * CHANNELS)])
    else:
        if len(loop_frames) > 0:
            # Playback Loop
            if loop_frame_index + loop_section_length < len(loop_frames) - 1:
                loop_section = loop_frames[loop_frame_index:loop_frame_index + loop_section_length]
                loop_frame_index += loop_section_length
            else:
                new_loop_frame_index = loop_frame_index + loop_section_length - len(loop_frames)
                loop_section = loop_frames[loop_frame_index:] + loop_frames[:new_loop_frame_index]
                loop_frame_index = new_loop_frame_index

            assert len(loop_section) == loop_section_length
            out_data = loop_section

        else:
            out_data = bytes([0 for _ in range(frame_count * WIDTH * CHANNELS)])

    assert len(out_data) == frame_count * CHANNELS * WIDTH
    return out_data, pyaudio.paContinue


if os.uname().nodename.lower() == 'raspberrypi':
    # TODO(BUG): Loop playback not working on RaspberryPi
    print('Running on RaspberryPi')
    CHUNK = 1024*3  # Higher chunk stopped underrun

    input_device_index = None
    while input_device_index is None:
        time.sleep(1)
        info = p_loopSectionStream.get_host_api_info_by_index(0)
        numDevices = info.get('deviceCount')
        for i in range(0, numDevices):
            if (p_loopSectionStream.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ",
                      p_loopSectionStream.get_device_info_by_host_api_device_index(0, i).get('name'))
                if "irig hd 2" in p_loopSectionStream.get_device_info_by_host_api_device_index(0, i).get(
                        'name').lower():
                    input_device_index = i
                    print("My inpute device is: ", i)

    liveStream = p_liveStream.open(format=p_liveStream.get_format_from_width(WIDTH),
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   output=True,
                                   output_device_index=None,
                                   frames_per_buffer=CHUNK,  #
                                   stream_callback=live_bypass_callback2)

    loopSectionStream = p_loopSectionStream.open(format=p_loopSectionStream.get_format_from_width(WIDTH),
                                                 channels=CHANNELS,
                                                 rate=RATE,
                                                 # input=True,
                                                 output=True,
                                                 output_device_index=None,
                                                 frames_per_buffer=CHUNK,  #
                                                 stream_callback=loop_section_callback2)


else:
    print('Running on pc')
    liveStream = p_liveStream.open(format=p_liveStream.get_format_from_width(WIDTH),
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   output=True,
                                   # output_device_index=input_device_index,
                                   # frames_per_buffer=CHUNK,  #
                                   # start=False,  #
                                   stream_callback=live_bypass_callback2)

    loopSectionStream = p_loopSectionStream.open(format=p_loopSectionStream.get_format_from_width(WIDTH),
                                                 channels=CHANNELS,
                                                 rate=RATE,
                                                 #input=True,
                                                 output=True,
                                                 #output_device_index=input_device_index,
                                                 # frames_per_buffer=CHUNK,  #
                                                 # start=False, #
                                                 stream_callback=loop_section_callback2)


#liveStream.start_stream()
#loopSectionStream.start_stream()

while True:
    # pass
    useInput = input()

    if useInput == 'q':
        break
    LOOPING = not LOOPING
    print('Looping') if LOOPING else print('Playback')
    if LOOPING:
        loop_frames = b''
        loop_frame_index = 0
    else:
        if len(loop_frames) > 0:
            save_loop()


liveStream.stop_stream()
liveStream.close()
p_liveStream.terminate()

loopSectionStream.stop_stream()
loopSectionStream.close()
p_loopSectionStream.terminate()

save_loop()
