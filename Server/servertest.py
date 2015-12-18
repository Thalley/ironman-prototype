import httplib, urllib
import random


REQUESTTYPES = ['GET', 'POST']
ACTIONS = ['turnOff', 'turnOn']
BADACTIONS = ['potato', 'burger']
correct = 0

def send_request(type, expected_code, action):
    connection =  httplib.HTTPConnection("localhost:5000")

    if type == 'GET':
        connection.request('GET', '/devices')
    else: 
        params = urllib.urlencode({'id': random.randrange(0,5), 'action': action})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        connection.request('POST', '/', params, headers)

    response = connection.getresponse()
    if response.status == expected_code:
        return 1
    else:
        return 0

#correct requests
for x in xrange(5000): 
    randon_num = random.randrange(0,2)
    request_type = REQUESTTYPES[randon_num]
    action = ACTIONS[random.randrange(0,2)]
    correct += send_request(request_type, 200, action)

#bad requests:
for x in xrange(5000): 
    randon_num = random.randrange(0,2)
    request_type = REQUESTTYPES[randon_num]
    action = BADACTIONS[random.randrange(0,2)]
    correct += send_request('POST', 400, action)
    
print correct