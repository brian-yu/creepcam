import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
green = 7
red = 11
yellow = 15
GPIO.setup([green, red, yellow], GPIO.OUT, initial=GPIO.LOW)

locked = True
while True:
    GPIO.output(red, locked)
    GPIO.output(green, not locked)
    GPIO.output(yellow, not locked)
    time.sleep(1)
    locked = not locked



try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
