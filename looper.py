"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import wave
from gpiozero import Button, LED, PWMLED
# from picamera import PiCamera
import numpy as np
from copy import copy
import random

import pyximport; pyximport.install()
#import cytest
#pyximport.install(pyimport=True)

# led = LED(21)
led = PWMLED(21)
led.off()
on_led = PWMLED(20)
# on_led.on
on_led.value = 1
# camera = PiCamera()
button = Button(17)
BUTTON_HELD = False

LOOPING = False
loop_frames = b''
loop_frame_index = 0

dtype = 'int16'
WIDTH = 2
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
CHUNK = 1024#4096#2048#1024 #2048

p = pyaudio.PyAudio()
# FORMAT = p.get_format_from_width(WIDTH)


def save_loop(): # Save loop
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(WIDTH)))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(loop_frames))
    wf.close()

def mix(audio1, audio2):
    decodeddata1 = copy(np.frombuffer(audio1, dtype=dtype))
    decodeddata2 = copy(np.frombuffer(audio2, dtype=dtype))
    #print('audio1: ', len(audio1))
    #print('audio2: ', len(audio2))
    #print('decodedata1: ', len(decodeddata1))
    #print('decodedata2: ', len(decodeddata2))
    len(audio1)
    len(decodeddata1)
    #newdata = decodeddata2 * 0.5 + decodeddata2 * 0.5

    newdata = decodeddata1 * 0.5 + decodeddata2 * 0.5
    #print(len(newdata))
    #print()
    return newdata.astype(int).tobytes()
    #return (decodeddata1 *0.8).astype(int).tobytes()

def dummyMixNumpy():
    """
    3.337860107421875e-06 looping
    0.00529932975769043 not looping
    """
    CHUNK = 2500#1500 #6124
    decodeddata1 = copy(np.frombuffer(bytes(CHUNK), dtype=dtype))
    decodeddata2 = copy(np.frombuffer(bytes(CHUNK), dtype=dtype))
    len(bytes(CHUNK))
    len(decodeddata1)
    # This opperation is too slow making the noise garbage
    (decodeddata1 * 0.8)
    #(decodeddata1 * 0.8).astype(int).tobytes()


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
    #(decodeddata1 * 0.8).astype(int).tobytes()
    # trying new method
    for byte in bytes(1000):
        (byte)
        (bytes([int(byte * 0.8)]))


def aaacythonMix():
    decodeddata1 = copy(np.frombuffer(bytes(CHUNK), dtype=dtype))
    decodeddata2 = copy(np.frombuffer(bytes(CHUNK), dtype=dtype))
    len(bytes(CHUNK))
    len(decodeddata1)
    # This opperation is too slow making the noise garbage
    #(decodeddata1 * 0.8).astype(int).tobytes()
    # trying new method
    for byte in bytes(CHUNK):
        (bytes([int(byte * 0.8)]))


def testcallback(in_data, frame_count, time_info, status):
    if LOOPING:
        if random.random() > 0.99: print('len indata: ', len(in_data))
        start = time.time()
        end = time.time()
        if random.random() > 0.99: print(end - start, 'looping')
        pass
    else:
        start = time.time()
        dummyMixFaster()
        #cythonMix()
        end = time.time()
        if random.random() > 0.99: print(end-start, 'not looping')

    return in_data, pyaudio.paContinue


def callback(in_data, frame_count, time_info, status):
    global loop_frames, loop_frame_index
    loop_section_length = len(in_data)
    # assert frame_count == loop_section_length, 'frame_count: ' + str(frame_count) + '\tloop_section_length: ' + str(loop_section_length)

    if LOOPING:
        loop_frames += in_data # TODO NB: check if append is correct here
        out_data = in_data
    else:
        if len(loop_frames) > 0:
            # Loop playback
            # Add loop and live guitar into one audio to return it exists
            if loop_frame_index + loop_section_length < len(loop_frames) - 1:
                loop_section = loop_frames[loop_frame_index:loop_frame_index + loop_section_length]
                loop_frame_index += loop_section_length
                #print('if')
            else:
                #print('old frame_loop_index: ', loop_frame_index)
                new_loop_frame_index = loop_frame_index + loop_section_length - len(loop_frames)
                loop_section = loop_frames[loop_frame_index:] + loop_frames[:new_loop_frame_index]
                loop_frame_index = new_loop_frame_index
                #print('else')


            #print(loop_frame_index)
            #print('loop_section_length: ', loop_section_length)
            #print('in_data: ', len(in_data))
            #print('loop_section: ', len(loop_section))
            #print('loop_frames: ', len(loop_frames))
            #print(button)
            #print()
            #assert loop_frame_index <= len(loop_frames), 'loop_frame_index too large, index: ' + str(loop_frame_index) + '\tlen(loop_frames): ' + str(len(loop_frames))
            #assert loop_frame_index >= 0, 'loop_frame_index negative'
            #assert len(in_data) == len(loop_section), "loop and live data not equal length"

            #print(in_data)
            #out_data = mix(in_data, loop_section)
            #out_data = mix(loop_section, loop_section)
            start = time.time()
            #out_data = dummyMixNumpy()
            #out_data = in_data
            out_data = mix(in_data, loop_section)
            #out_data = cytest.cytestMix(in_data, loop_section)
            #out_data = in_data
            #print(in_data)
            #print()
            end = time.time()
            if random.random() > 0.99: print(end - start, 'not looping')

        else:
            out_data = in_data


    #return in_data * 2, pyaudio.paContinue
    return out_data, pyaudio.paContinue


info = p.get_host_api_info_by_index(0)
numDevices = info.get('deviceCount')
input_device_index = None
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
                # input_device_index=input_device_index,
                output_device_index=input_device_index,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

print(".-.", p.get_default_input_device_info())

stream.start_stream()

while True:
    if button.is_pressed:
        #print("Button is pressed")
        if BUTTON_HELD:
            pass  # do nothing
        else:
            BUTTON_HELD = True
            # Do stuff here (button is first pressed)

            # Toggle looping/looping light
            LOOPING = not LOOPING
            if LOOPING:
                # led.on()
                led.value = 0.5
                loop_frames = b''
                loop_frame_index = 0
            else:
                led.off()
                #save_loop()

    else:
        #print("Button is not pressed")
        if BUTTON_HELD:
            BUTTON_HELD = False
            # Do stuff here (button is released)
            # led.off

    #on_led.on
    on_led.value = 0.9
    #print(LOOPING)
    #print(len(loop_frames))


# while stream.is_active():
#    time.sleep(0.1)
# time.sleep(5)

# Close everything
stream.stop_stream()
stream.close()
p.terminate()
