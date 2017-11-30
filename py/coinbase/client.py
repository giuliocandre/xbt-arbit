from api import CoinBaseAPI

API_KEY = ''
API_SECRET = ''
API_PASS = ''
client = CoinBaseAPI(API_KEY, API_SECRET, API_PASS)
print (client.getPrice())
