"""

"""

import pyaudio
import wave


WIDTH = 2
dtype = 'int' + str(8*WIDTH)  # 'int16'
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
CHUNK = 1024

LOOPING = False
loop_frames = b''
loop_frame_index = 0

wf_file = wave.open('demolition.wav', 'rb')

p_liveStream = pyaudio.PyAudio()
p_fileStream = pyaudio.PyAudio()
p_loopSectionStream = pyaudio.PyAudio()

# FORMAT = p.get_format_from_width(WIDTH)


def save_loop():  # Save loop
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(WIDTH)
    wf.setframerate(RATE)
    wf.writeframes(loop_frames)
    wf.close()


def live_bypass_callback(in_data, frame_count, time_info, status):
    return in_data, pyaudio.paContinue


def file_callback(in_data, frame_count, time_info, status):
    data = wf_file.readframes(frame_count)
    return data, pyaudio.paContinue


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


liveStream = p_liveStream.open(format=p_liveStream.get_format_from_width(WIDTH),
                               channels=CHANNELS,
                               rate=RATE,
                               input=True,
                               output=True,
                               frames_per_buffer=CHUNK,
                               start=False,
                               stream_callback=live_bypass_callback)

fileStream = p_fileStream.open(format=p_fileStream.get_format_from_width(wf_file.getsampwidth()),
                               channels=wf_file.getnchannels(),
                               rate=wf_file.getframerate(),
                               output=True,
                               start=False,
                               stream_callback=file_callback)

loopSectionStream = p_loopSectionStream.open(format=p_loopSectionStream.get_format_from_width(WIDTH),
                                             channels=CHANNELS,
                                             rate=RATE,
                                             input=True,
                                             output=True,
                                             # input_device_index=input_device_index,
                                             # output_device_index=input_device_index,
                                             frames_per_buffer=CHUNK,
                                             start=False,
                                             stream_callback=loop_section_callback)

# stream.start_stream()
liveStream.start_stream()
# fileStream.start_stream()
loopSectionStream.start_stream()

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

fileStream.stop_stream()
fileStream.close()
p_fileStream.terminate()

loopSectionStream.stop_stream()
loopSectionStream.close()
p_loopSectionStream.terminate()

save_loop()
