#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
import time

LedPin = 11

ApiHeaders = { 'Content-Type': 'application/json', 'Accept': 'application/json' }

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.output(LedPin, GPIO.HIGH)

def loop():
	while True:
	    GPIO.output(LedPin, GPIO.LOW)
		time.sleep(0.5)
	    GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(0.5)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
