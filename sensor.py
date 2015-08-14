#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LedPin = 11
BtnPin = 12
SenPin = 13

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(SenPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

	GPIO.output(LedPin, GPIO.HIGH)

# TO BE FINISHED!
def blinkLed():
	while True:
		GPIO.output(LedPin, GPIO.LOW)
		time.sleep(0.2)
		GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(0.2)

def loop():
	currentState = 0

	while True:
		time.sleep(0.01)
		if GPIO.input(SenPin) == GPIO.LOW:
			if currentState == 0:
				currentState = 1
				print 'DOOR CLOSED'
				GPIO.output(LedPin, GPIO.LOW)
		else:
			if currentState == 1:
				currentState = 0
				print 'DOOR OPEN'
				GPIO.output(LedPin, GPIO.HIGH)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
