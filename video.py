# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Servo Control
import wiringpi
 
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
 
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
 
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)


# load XML classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.rotation = 90
camera.resolution = (640, 480)
camera.framerate = 32
camera.hflip = True
rawCapture = PiRGBArray(camera, size=camera.resolution)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
    
    faceCoords = None
    facex = None
    facew = None
    faceArea = 0
    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if w*h > faceArea:
            faceArea = w*h
            faceCoords = (x+w/2, y+h/2)
            facex = x+w/2
            facew = w
        '''roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)'''
    lastSeen = 0
    center = 300
    
    if facex:
        error = facew+20
        if facex > center + error:
            wiringpi.pwmWrite(18, 154)
            print("turning right")
        elif facex < center - error:
            wiringpi.pwmWrite(18, 151)
            print("turning left")
        else:
            wiringpi.pwmWrite(18, 0)
        lastSeen = time.clock()
        print("yes face {} {}".format(time.clock(), facex))
    else:
        print("no face {}".format(time.clock()))
        if time.clock() - lastSeen > 1:
            wiringpi.pwmWrite(18, 0)
    
    #cv2.putText(image, "Hello World!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
