import time
import requests

from requests.exceptions import ConnectionError

SensorPins = { 13: 1 } # Keys are GPIO pin numbers, values are toilet IDs
ApiHeaders = { 'Content-Type': 'application/json', 'Accept': 'application/json' }

last_keepalive = time.time() - 61

def process_keepalive():
	global last_keepalive

	if time.time() - last_keepalive >= 5:
		try:
			# Send keepalive to all connected toilets.
			for toilet_id in SensorPins.values():
				r = requests.patch('http://tds.shovik.com/toilets/' + str(toilet_id) + '/keepalive', headers = ApiHeaders)
				print 'Sent keepalive for toilet ID ' + str(toilet_id) + '. Status: ' + str(r.status_code)

			last_keepalive = time.time()
		except ConnectionError as e:
			print e

def loop():
	print "Entering loop"

	while True:
		time.sleep(1)
		print "Looping..."
		process_keepalive()

if __name__ == '__main__':
	loop()
