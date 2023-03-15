"""
This program uses the Circuit Playground to handle the timer functionality of the StudyBox.
"""

import board
import pwmio
from adafruit_circuitplayground import cp
import adafruit_motor.servo
import time

timer = 0
defBright = 10
pwm = pwmio.PWMOut(board.A1, frequency=50)
servo = adafruit_motor.servo.Servo(pwm, min_pulse=750, max_pulse=2600)

# indicate timer was increased
def indicateIncrease(timer, defBright):
    ratio = defBright / 10
    if timer == 300:
        cp.pixels[4] = (defBright,0,0)
    elif timer == 600:
        cp.pixels[3] = (defBright - ratio,ratio,0)
    elif timer == 900:
        cp.pixels[2] = (defBright - 2*ratio,2*ratio,0)
    elif timer == 1200:
        cp.pixels[1] = (defBright - 3*ratio,3*ratio,0)
    elif timer == 1500:
        cp.pixels[0] = (defBright - 4*ratio,4*ratio,0)
    elif timer == 1800:
        cp.pixels[9] = (defBright - 5*ratio,5*ratio,0)
    elif timer == 2100:
        cp.pixels[8] = (defBright - 6*ratio,6*ratio,0)
    elif timer == 2400:
        cp.pixels[7] = (defBright - 7*ratio,7*ratio,0)
    elif timer == 2700:
        cp.pixels[6] = (defBright - 8*ratio,8*ratio,0)
    elif timer == 3000:
        cp.pixels[5] = (defBright - 9*ratio,9*ratio,0)

# indicate that a timer reset occurred
def indicateReset(defBright):
    cp.pixels.fill((defBright,0,0))
    cp.play_tone(300, 0.3)
    cp.play_tone(200, 0.3)
    cp.pixels.fill((0,0,0))

# cool light show
def lightShow(defBright):
    high = defBright
    medium = defBright / 2
    low = defBright / 10

    cp.pixels[0] = (high,0,medium)
    time.sleep(0.1)
    cp.pixels[8] = (high,0,medium)
    time.sleep(0.1)
    cp.pixels[9] = (high,0,0)
    time.sleep(0.1)
    cp.pixels[1] = (high,0,0)
    time.sleep(0.1)
    cp.pixels[2] = (0,high,0)
    time.sleep(0.1)
    cp.pixels[6] = (0,high,0)
    time.sleep(0.1)
    cp.pixels[7] = (0,0,high)
    time.sleep(0.1)
    cp.pixels[3] = (0,0,high)
    time.sleep(0.1)
    cp.pixels[4] = (high,medium,low)
    time.sleep(0.1)
    cp.pixels[5] = (high,medium,low)
    time.sleep(0.1)

# turn off the lights
def finishLightShow():
    for i in range(0,9 + 1):
        cp.pixels[i] = (0,0,0)
        time.sleep(0.1)

# cancel timer if any button is pressed/held
def checkCancel(defBright):
    if cp.button_a or cp.button_b:
        lightShow(defBright)
        finishLightShow()
        return True
    return False

# start the timer countdown
def startCoutdown(timer, defBright):
    # if user did not set timer, just play the jam
    if timer == 0:
        finish()
        return

    # countdown indicated by lights (start green, then gradually become yellow, then red)
    ratio = defBright / timer
    red,green = 0, defBright
    while timer > 0:
        cp.pixels.fill((red,green,0))
        red += ratio
        green -= ratio
        if checkCancel(defBright): return
        time.sleep(1) # change this to change how fast the timer countsdown
        if checkCancel(defBright): return
        timer -= 1
    finish()
    return

# activate song and servo motor
def finish():
    servo.angle = 70
    lightShow(defBright)
    if cp.switch: cp.play_file("Comedy-by-Gen-Hoshino.wav")
    finishLightShow()

while True:
    # Increase timer by 300 sec (5 min) with every button_a press
    if cp.button_a:
        time.sleep(0.3)
        timer += 300

        # If timer exceeds 3000 sec (50 min) reset it back to 0 sec
        if timer > 3000:
            timer = 0
            indicateReset(defBright)
        else:
            indicateIncrease(timer, defBright)

    # Start the timer then activate song and servo motor when expires
    if cp.button_b:
        time.sleep(0.3)
        servo.angle = 180
        startCoutdown(timer, defBright)
        timer = 0
