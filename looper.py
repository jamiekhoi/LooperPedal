"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import wave
from gpiozero import Button, LED, PWMLED
from picamera import PiCamera

# led = LED(21)
led = PWMLED(21)
led.off()
on_led = PWMLED(20)
#on_led.on
on_led.value = 1
camera = PiCamera()
button = Button(17)
BUTTON_HELD = False
LOOPING = False

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
                stream_callback=callback)

print(".-.", p.get_default_input_device_info())

stream.start_stream()

while True:
    if button.is_pressed:
        print("Button is pressed")
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
            else:
                led.off()

    else:
        print("Button is not pressed")
        if BUTTON_HELD:
            BUTTON_HELD = False
            # Do stuff here (button is released)
            # led.off

    #on_led.on
    on_led.value = 1
    print(LOOPING)

# while stream.is_active():
#    time.sleep(0.1)
# time.sleep(5)

# Close everything
stream.stop_stream()
stream.close()
p.terminate()

# Save loop
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(WIDTH)))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
