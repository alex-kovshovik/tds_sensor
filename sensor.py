#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import RPiMock.GPIO as GPIO
import time
import requests
import json

from requests.exceptions import ConnectionError

# NOTE: override this to add more toilets!
SensorPins = { 13: 1 } # Keys are GPIO pin numbers, values are toilet IDs
LedPin = 11

ApiHeaders = { 'Content-Type': 'application/json', 'Accept': 'application/json' }

last_keepalive = time.time() - 61

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.output(LedPin, GPIO.HIGH)

	for pin in SensorPins.keys():
		GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def update_toilet_state(toilet_id, is_closed):
	new_state = 'occupied' if is_closed else 'available'

	try:
		update_params = { 'toilet': { 'state' : new_state } }
		r = requests.patch('http://tds.shovik.com/toilets/' + str(toilet_id), data = json.dumps(update_params), headers = ApiHeaders)

		print 'Updated toilet ID ' + str(toilet_id) + ' to "' + new_state + '". Status: ' + str(r.status_code)
	except ConnectionError as e:
		print e

def update_state(pin, was_closed, is_closed):
	toilet_id = SensorPins[pin]

	if not was_closed and is_closed:
		GPIO.output(LedPin, GPIO.LOW)
		update_toilet_state(toilet_id, is_closed)

	if was_closed and not is_closed:
		GPIO.output(LedPin, GPIO.HIGH)
		update_toilet_state(toilet_id, is_closed)

	return is_closed

def process_keepalive():
	global last_keepalive

	if time.time() - last_keepalive >= 60:
		try:
			# Send keepalive to all connected toilets.
			for toilet_id in SensorPins.values():
				r = requests.patch('http://tds.shovik.com/toilets/' + str(toilet_id) + '/keepalive', headers = ApiHeaders)
				print 'Sent keepalive for toilet ID ' + str(toilet_id) + '. Status: ' + str(r.status_code)

			last_keepalive = time.time()
		except ConnectionError as e:
			print e

def loop():
	was_closed = {} # Keys are GPIO pin numbers, values are boolean previous state.
	for pin in SensorPins.keys():
		was_closed[pin] = False

	while True:
		time.sleep(0.2)
		process_keepalive()

		for pin in SensorPins.keys():
			was_closed[pin] = update_state(pin, was_closed[pin], GPIO.input(pin) == GPIO.LOW)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
