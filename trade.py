import os
import hashlib
import hmac
import urllib.request
import urllib.error
import urllib.parse
import time
import json


#Before implementation, set environmental variables with the names API_KEY and API_SECRET.


def make_request(url, body=None):
    opener = urllib.request.build_opener()
    nonce = int(time.time() * 1e6)
    message = str(nonce) + url + ('' if body is None else body)
    signature = hmac.new(str.encode(os.environ['API_SECRET']), str.encode(message), hashlib.sha256).hexdigest()
    headers = {'ACCESS_KEY': os.environ['API_KEY'],
               'ACCESS_SIGNATURE': signature,
               'ACCESS_NONCE': nonce,
               'Accept': 'application/json'}

    if body:
        headers.update({'Content-Type': 'application/json'})
        req = urllib.request.Request(url, data=str.encode(body), headers=headers)

    else:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        return response.read()
    try:
        return opener.open(req)
    except urllib.error.HTTPError as e:
        print(e)
        return e



def query(id=None):
    balance = make_request('https://api.coinbase.com/v1/account/balance')
    balance = json.loads(balance.decode("utf-8"))
    print(balance['amount'], ' BTC')


def buy(amount, log, currency='BTC'):
    param = {
        'qty': amount,
        'commit': 'false',
        'currency': currency,
    }
    req = make_request('https://api.coinbase.com/v1/buys', body=json.dumps(param)).read()
    req = json.loads(req.decode("utf-8"))
    current_time = time.strftime("%m.%d.%y %H:%M ", time.localtime())
    log.write(current_time)
    log.write('Orders: ' + str(req['transfer']['description']) + ' , ')
    log.write('Status: ' + str(req['transfer']['status']) + ' , ')
    if req['success'] == False:
        log.write('Errors: ' + str(req['errors']) + ' ')
    log.write('\n')


def sell(amount, log, currency='BTC'):
    param = {
        'qty': amount,
        'commit': 'false',
        'currency': currency,
    }
    req = make_request('https://api.coinbase.com/v1/sells', body=json.dumps(param)).read()
    req = json.loads(req.decode("utf-8"))
    current_time = time.strftime("%m.%d.%y %H:%M ", time.localtime())
    log.write(current_time)
    log.write('Orders: ' + str(req['transfer']['description']) + ' , ')
    log.write('Status: ' + str(req['transfer']['status']) + ' , ')
    if req['success'] == False:
        log.write('Errors: ' + str(req['errors']) + ' ')
    log.write('\n')

def status():
    status = make_request('https://api.coinbase.com/v1/orders')
    status = json.loads(status.decode("utf-8"))
    print('Number of orders: ', status['total_count'])
    if status['total_count'] > 0:
        print('Orders: ', status['orders'])


if __name__ == '__main__':
    query()
    status()
    log = open('tradelogs', 'w')
    buy(1.5, log, currency='USD')
    sell(1.5, log, currency='USD')
