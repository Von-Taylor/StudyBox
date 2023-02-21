import time
from adafruit_circuitplayground import cp

# indicate timer was increased
def indicateIncrease():
    cp.pixels.fill((0,0,1))
    time.sleep(0.1)
    cp.pixels.fill((0,0,0))

# indicate that a timer reset occurred
def indicateReset():
    cp.pixels.fill((5,0,0))
    cp.play_tone(300, 0.3)
    cp.play_tone(200, 0.3)
    cp.pixels.fill((0,0,0))

# cool light show
def lightShow():
    high = 5
    medium = 2.5
    low = 0.5
    
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

# cancel timer if any button is pressed
def checkCancel():
    if cp.button_a or cp.button_b:
        lightShow()
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
        if checkCancel(): return
        time.sleep(1)
        if checkCancel(): return
        timer -= 1
    finish()
    return

# activate song and servo motor
def finish():
    # activate servo motor here
    lightShow()
    if cp.switch: cp.play_file("Comedy-by-Gen-Hoshino.wav")
    finishLightShow()

timer = 0
defBright = 5

while True:
    # Increase timer by 300 sec (5 min) with every button_a press
    if cp.button_a:
        time.sleep(0.3)
        timer += 300
        
        # If timer exceeds 3600 sec (1 hour) reset it back to 0 sec
        if timer > 3600:
            timer = 0
            indicateReset()
        else:
            indicateIncrease()
    
    # Start the timer then activate song and servo motor when expires 
    if cp.button_b:
        time.sleep(0.3)
        startCoutdown(timer, defBright)