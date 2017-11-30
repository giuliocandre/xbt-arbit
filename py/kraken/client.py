from api import KrakenAPI


client_key = ''
secret_key = ''


#create the api connection
kraken = KrakenAPI(client_key, secret_key)

print (kraken.query_public('Ticker', {'pair' : 'XXBTZEUR'}))

print (kraken.query_private('AddOrder', {
    'pair' : 'XXBTZEUR', 
    'type' : 'sell', 
    'ordertype' : 'limit', 
    'price' : '120', 
    'volume' : '1.123'
}))
print (kraken.query_private('Balance'))

print (kraken.query_public('Depth', {'pair' : 'XXBTZEUR'}))
