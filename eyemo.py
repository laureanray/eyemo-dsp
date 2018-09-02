import sys
import numpy as np
import math
import RPi.GPIO as GPIO
sys.path.append('/usr/local/lib/python3.4/site-packages')
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
GPIO.setmode(GPIO.BOARD)

MotorA1r = 12
MotorA2f = 11
MotorB3r = 15
MotorB4f = 13
Motor2E = 18
Motor1E = 22

GPIO.setwarnings(False)
GPIO.setup(MotorA1r,GPIO.OUT)
GPIO.setup(MotorA2f,GPIO.OUT)
GPIO.setup(MotorB3r,GPIO.OUT)
GPIO.setup(MotorB4f,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

speed1 = GPIO.PWM(Motor1E, 20)
speed2 = GPIO.PWM(Motor2E, 20)
speed1.start(40)
speed2.start(40)

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

while True:
	ret, im = cap.read()
	cv2.imwrite('img.jpg',im)
	img = cv2.imread('img.jpg')
	img2= cv2.imread('img.jpg',0)
	gry = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, th = cv2.threshold(gry,60,255,cv2.THRESH_BINARY_INV)
	ret, contours, hierarchy = cv2.findContours(th,1,2)
	cv2.drawContours(img2, contours, -1,(255,255,255),3)

	for cnt in contours:
		area = cv2.contourArea(cnt)
		approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(img2,[box],0,(255,255,255),2)
		moments = cv2.moments(cnt)
		areas = moments['m00']

		if len(approx)==7 and area > 8000 and area < 10000:
			leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
			rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
			topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
			bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

			lin1 = cv2.line(img2,leftmost,topmost,(0,128,0),5)
			lin2 = cv2.line(img2,topmost,rightmost,(0,128,0),5)
			lin3 = cv2.line(img2,rightmost,bottommost,(0,128,0),5)
			lin4 = cv2.line(img2,bottommost,leftmost,(0,128,0),5)
			(xl, yl) = leftmost
			(xr, yr) = rightmost
			(xt, yt) = bottommost
			dist1 = math.hypot(xl-xt,yl-yt)
			dist2 = math.hypot(xr-xt,yr-yt)
			print (len(approx), ':', area)
			if dist1 > dist2:
				cap = cv2.VideoCapture(1)
				print ('go right',area,':',len(approx))
				speed1.start(100)
				speed2.start(100)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.HIGH)
				speed1.ChangeDutyCycle(50)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.HIGH)
				speed2.ChangeDutyCycle(50)
				sleep(0.6)	
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.5)			
				GPIO.output(MotorA1r,GPIO.HIGH)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.HIGH)
				speed2.ChangeDutyCycle(100)
				sleep(0.43)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.8)	
				cap = cv2.VideoCapture(0)
				sleep(0.4)
				cap.set(3,320)
				cap.set(4,240)
			elif dist2 > dist1:
				cap = cv2.VideoCapture(1)
				print ('go left',area,':',len(approx))
				speed1.start(100)
				speed2.start(100)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.HIGH)
				speed1.ChangeDutyCycle(50)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.HIGH)
				speed2.ChangeDutyCycle(50)
				sleep(0.6)		
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.5)								
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.HIGH)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.HIGH)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.43)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.8)	
				cap = cv2.VideoCapture(0)
				sleep(0.4)
				cap.set(3,320)
				cap.set(4,240)

			elif len(approx) == 5 and area > 2500 and area < 7000:
				print ('UTURN' , area, ':',len(approx))
				cap.cv2.VideoCapture(1)
				speed1.start(40)
				speed2.start(40)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.5)							
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.HIGH)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.HIGH)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(0.9)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.LOW)
				speed1.ChangeDutyCycle(100)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.LOW)
				speed2.ChangeDutyCycle(100)
				sleep(1)
				GPIO.output(MotorA1r,GPIO.LOW)
				GPIO.output(MotorA2f,GPIO.HIGH)
				speed1.ChangeDutyCycle(20)
				GPIO.output(MotorB3r,GPIO.LOW)
				GPIO.output(MotorB4f,GPIO.HIGH)
				speed2.ChangeDutyCycle(20)
				sleep(.9)	
				cap = cv2.VideoCapture(0)
				cap.set(3,320)
				cap.set(4,240)


		else:
                        print ('forward' , area, ':',len(approx))
                        speed1.start(20)
                        speed2.start(20)	
                        GPIO.output(MotorA1r,GPIO.LOW)
                        GPIO.output(MotorA2f,GPIO.HIGH)
                        speed1.ChangeDutyCycle(29)
                        GPIO.output(MotorB3r,GPIO.LOW)
                        GPIO.output(MotorB4f,GPIO.HIGH)
                        speed2.ChangeDutyCycle(34)
	cv2.imshow('Video', img2) 	
	if cv2.waitKey(1) & 0xFF == ord('q'):
			GPIO.output(MotorA1r,GPIO.LOW)
			GPIO.output(MotorA2f,GPIO.HIGH)
			GPIO.output(MotorB3r,GPIO.LOW)
			GPIO.output(MotorB4f,GPIO.HIGH)
			break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
 