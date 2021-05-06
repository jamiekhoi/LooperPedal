import time

from gpiozero import Button, LED, PWMLED

# led = LED(21)
led = PWMLED(21)
led.off()

on_led = PWMLED(20)
# on_led.on
on_led.value = 1

button = Button(17)
# BUTTON_HELD = False

LOOPING = False


def press_fun():
    global LOOPING
    print('press')
    LOOPING = not LOOPING
    print('Looping') if LOOPING else print('Playback')
    if LOOPING:
        led.on()
    else:
        led.off()


def release_fun():
    print('release')


button.when_pressed = press_fun
button.when_released = release_fun

while True:

    time.sleep(0.1)
