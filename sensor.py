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

def update_toilet_state(is_closed):
	new_state = 'occupied' if is_closed else 'available'

	update_params = { 'toilet': { 'state' : new_state } }
	r = requests.patch('http://tds.shovik.com/toilets/1', json = update_params, headers = ApiHeaders)

	print 'Updated to "' + new_state + '". Status: ' + str(r.status_code) + ', Response: ' + r.content

def update_state(was_closed, is_closed):
	if not was_closed and is_closed:
		GPIO.output(LedPin, GPIO.LOW)
		update_toilet_state(is_closed)

	if was_closed and not is_closed:
		GPIO.output(LedPin, GPIO.HIGH)
		update_toilet_state(is_closed)

	return is_closed

def loop():
	was_closed = False

	while True:
		time.sleep(0.1)
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
