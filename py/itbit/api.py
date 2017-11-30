import abc
import base64
import hashlib
import hmac
import json
import requests
import time
import urllib as urlparse

from wrapper_interface import WrapperBase

api_address = 'https://api.itbit.com/v1'


class MessageSigner(object):

    def make_message(self, verb, url, body, nonce, timestamp):
        return json.dumps([verb, url, body, str(nonce), str(timestamp)], separators=(',', ':'))

    def sign_message(self, secret, verb, url, body, nonce, timestamp):
        message = self.make_message(verb, url, body, nonce, timestamp)
        sha256_hash = hashlib.sha256()
        nonced_message = str(nonce) + message
        sha256_hash.update(nonced_message.encode('utf8'))
        hash_digest = sha256_hash.digest()
        hmac_digest = hmac.new(secret, url.encode('utf8') + hash_digest, hashlib.sha512).digest()
        return base64.b64encode(hmac_digest)


class ItBitApiConnection(WrapperBase):

    def __init__(self, client_key, secret, user_id):
        self.client_key = client_key
        self.secret = secret.encode('utf-8')
        self.user_id = user_id
        self.nonce = 0

    def get_ticker(self, ticker_symbol):
        path = "/markets/%s/ticker" % (ticker_symbol)
        response = self.make_request("GET", path, {})
        return response

    def get_order_book(self, tickerSymbol):
        path = "/markets/%s/order_book" % (tickerSymbol)
        response = self.make_request("GET", path, {})
        return response

    def get_all_wallets(self, filters={}):
        filters['user_id'] = self.user_id
        queryString = self._generate_query_string(filters)
        path = "/wallets%s" % (queryString)
        response = self.make_request("GET", path, {})
        return response

    def create_wallet(self, walletName):
        path = "/wallets"
        response = self.make_request("POST", path, {'userId': self.userId, 'name': walletName})
        return response

    def get_wallet(self, walletId):
        path = "/wallets/%s" % (walletId)
        response = self.make_request("GET", path, {})
        return response

    def get_wallet_balance(self, walletId, currency):
        path = "/wallets/%s/balances/%s" % (walletId, currency)
        response = self.make_request("GET", path, {})
        return response

    def get_wallet_trades(self, walletId, filters={}):
        queryString = self._generate_query_string(filters)
        path = "/wallets/%s/trades%s" % (walletId, queryString)
        response = self.make_request("GET", path, {})
        return response

    def get_wallet_orders(self, walletId, filters={}):
        queryString = self._generate_query_string(filters)
        path = "/wallets/%s/orders%s" % (walletId, queryString)
        response = self.make_request("GET", path, {})
        return response

    def create_order(self, walletId, side, currency, amount, price, instrument):
        path = "/wallets/%s/orders/" % (walletId)
        response = self.make_request("POST", path, {'type': 'limit', 'currency': currency, 'side': side, 'amount': amount, 'price': price, 'instrument': instrument})
        return response

    def create_order_with_display(self, walletId, side, currency, amount, price, display ,instrument):
        path = "/wallets/%s/orders/" % (walletId)
        response = self.make_request("POST", path, {'type': 'limit', 'currency': currency, 'side': side, 'amount': amount, 'price': price, 'display': display, 'instrument': instrument})
        return response 

    def get_order(self, walletId, orderId):
        path = "/wallets/%s/orders/%s" % (walletId, orderId)
        response = self.make_request("GET", path, {})
        return response

    def cancel_order(self, walletId, orderId):
        path = "/wallets/%s/orders/%s" % (walletId, orderId)
        response = self.make_request("DELETE", path, {})
        return response

    def cryptocurrency_withdrawal_request(self, walletId, currency, amount, address):
        path = "/wallets/%s/cryptocurrency_withdrawals" % (walletId)
        response = self.make_request("POST", path, {'currency': currency, 'amount': amount, 'address': address})
        return response

    def cryptocurrency_deposit_request(self, walletId, currency):
        path = "/wallets/%s/cryptocurrency_deposits" % (walletId)
        response = self.make_request("POST", path, {'currency': currency})
        return response

    def create_wallet_transfer(self, sourceWalletId, destinationWalletId, amount, currencyCode):
        path = "/wallet_transfers"
        response = self.make_request("POST", path, {'sourceWalletId': sourceWalletId, 'destinationWalletId': destinationWalletId, 'amount': amount, 'currencyCode': currencyCode})
        return response

    def make_request(self, verb, url, body_dict):
        url = api_address + url
        nonce = self._get_next_nonce()
        timestamp = self._get_timestamp()

        if verb in ("PUT", "POST"):
            json_body = json.dumps(body_dict)
        else:
            json_body = ""

        signer = MessageSigner()
        signature = signer.sign_message(self.secret, verb, url, json_body, nonce, timestamp)

        auth_headers = {
            'Authorization': self.client_key + ':' + signature.decode('utf8'),
            'X-Auth-Timestamp': timestamp,
            'X-Auth-Nonce': nonce,
            'Content-Type': 'application/json'
        }

        return requests.request(verb, url, data=json_body, headers=auth_headers)

    def _get_next_nonce(self):
        self.nonce += 1
        return self.nonce

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _generate_query_string(self, filters):
        if filters:
            return '?' + urlparse.urlencode(filters)
        else:
            return ''
