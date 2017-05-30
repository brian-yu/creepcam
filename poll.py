import requests
import time 
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
green = 7
red = 11
GPIO.setup([green, red], GPIO.OUT, initial=GPIO.LOW)
pwm = GPIO.PWM(12, 100)
pwm.start(5)

GPIO.output(red, True)
GPIO.output(green, False)

def unlock():
    print("Unlocked")
    GPIO.output(red, False)
    GPIO.output(green, True)
    pwm.ChangeDutyCycle(45)
    time.sleep(15)
    pwm.ChangeDutyCycle(5)
    GPIO.output(red, True)
    GPIO.output(green, False)

r = requests.get('http://remote.byu.io:5000/')

lastUnlock = r.text



while True:
    
    r = requests.get('http://remote.byu.io:5000/')
    
    #print(r.text)
    
    if lastUnlock != "" and lastUnlock != r.text:
        lastUnlock = r.text
        unlock()
        print(r.text)
    
    time.sleep(5)


try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
