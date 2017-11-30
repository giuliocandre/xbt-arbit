# CoinBase API Py Wrapper
# @giuliocandre

import json
import urllib.request, urllib.parse, urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64
import requests


class CoinBaseAPI(object):

    def __init__ (self, key, secret, passphrase):
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.uri = 'https://api.gdax.com'

    def signature(self, request_path, body='', timestamp='', method='GET'):
        body = json.dumps(body) if type(body) == type(dict()) else body
        what = str(timestamp + method + request_path + body).encode('utf8')
        signature = hmac.new(base64.b64decode(self.secret), what, hashlib.sha256)
        return base64.b64encode(signature.digest())

    def query(self, method, url, data=''):
        timestamp = str(int(time.time()))
        postdata = json.dumps(data) if data else ''
        sign = self.signature(url, data, timestamp, method)
        auth_headers = {
            'User-Agent' : 'CoinBraze (X11; Ubuntu; Linux x86_64; rv:43.0)',
            'CB-ACCESS-KEY' : self.key,
            'CB-ACCESS-PASSPHRASE' : self.passphrase,
            'CB-ACCESS-TIMESTAMP' : timestamp,
            'CB-ACCESS-SIGN' : sign.decode('utf8'),
            'Content-type' : 'application/json'
        }
        #print (auth_headers)
        url = self.uri + url
        return requests.request(method, url, data=postdata, headers=auth_headers)

    def getPrice(self):
        resp = json.loads(self.query("GET", '/products/BTC-EUR/ticker').text)
        return resp['price']

