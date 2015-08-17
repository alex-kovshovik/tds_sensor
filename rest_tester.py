import requests
import json

headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }

print 'Attempting to update the status of the toilet...'
update_params = { 'toilet': { 'state' : 'occupied' } }
r = requests.patch('http://tds.shovik.com/toilets/1', json = update_params, headers = headers)
print 'Done. Status = ' + str(r.status_code)
print 'Response: ' + r.content

# print 'Getting the list of toilets...'
# r = requests.get('http://tds.shovik.com/toilets', headers = headers)
# print 'Done:'
# print r.content
