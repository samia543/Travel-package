import numpy as np
import cv2

import playsound
from threading import Thread
import argparse

face_cascade = cv2.CascadeClassifier('E:/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('E:/haarcascade_eye.xml')

ALARM_ON = False


ap =argparse.ArgumentParser()
ap.add_argument("-a","--alarm",type=str,default="alarm.wav",help="path alarm.WAV file")
args=vars(ap.parse_args())

def beep(path):
    print("detected it beep... ")
    playsound.playsound(path)



cam = cv2.VideoCapture(0)
count = 0
iters = 0
while(True):
      ret, cur = cam.read()
      gray = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.1, minNeighbors=1, minSize=(10,10))
      for (x,y,w,h) in faces:
      	#cv2.rectangle(cur,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_color = cur[y:y+h,x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) == 0:
          print("Eyes closed")
        else:
          print("Eyes open")
        count += len(eyes)
        iters += 1
        if iters == 2:
          iters = 0
          if count == 0:
            print("Drowsiness Detected!!!")
            if not ALARM_ON:
                ALARM_ON = True

                # check to see if an alarm file was supplied,
                # and if so, start a thread to have the alarm
                # sound played in the background
                if args["alarm"] != "":
                    t = Thread(target=beep,
                               args=(args["alarm"],))
                    t.deamon = True
                    t.start()
            cv2.putText(cur, "DROWSINESS ALERT!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
          else:
            count = 0
            ALARM_ON=False

        for (ex,ey,ew,eh) in eyes:
        	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh), (0,255,0),2)
      cv2.imshow('frame', cur)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break