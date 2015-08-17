#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import requests
import json

LedPin = 11
SenPin = 13

ApiHeaders = { 'Content-Type': 'application/json', 'Accept': 'application/json' }

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.setup(SenPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

	GPIO.output(LedPin, GPIO.HIGH)

# TODO: TO BE FINISHED!
def blinkLed():
	while True:
		GPIO.output(LedPin, GPIO.LOW)
		time.sleep(0.2)
		GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(0.2)

def update_state(was_closed, is_closed):
	if !was_closed && is_closed:
		print 'DOOR JUST CLOSED'
		GPIO.output(LedPin, GPIO.LOW)

	if was_closed && !is_closed:
		print 'DOOR JUST OPENED'
		GPIO.output(LedPin, GPIO.HIGH)

	return is_closed

def loop():
	was_closed = False

	while True:
		time.sleep(0.01)
		was_closed = update_state(was_closed, GPIO.input(SenPin) == GPIO.LOW)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
