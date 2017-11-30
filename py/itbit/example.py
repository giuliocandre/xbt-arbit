from api import ItBitApiConnection
import json

client_key = '< client key >'
secret_key = '< secret key >'
user_id = '< userId >'


itbit_api_conn = ItBitApiConnection(client_key=client_key, secret=secret_key, user_id=user_id)


wallets = itbit_api_conn.get_all_wallets().json()
walletId = next(wallet for wallet in wallets if wallet['name'] == 'Wallet')['id']
print(json.dumps(itbit_api_conn.get_wallet_trades(walletId).json(), indent=2))

