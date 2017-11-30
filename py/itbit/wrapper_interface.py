from abc import ABCMeta
import abc

class WrapperBase(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def get_ticker(self, ticker_symbol):
        """Returns ticker information for a specific symbol"""
        return

    @abc.abstractmethod
    def get_order_book(self, tickerSymbol):
        """returns order book information for a specific ticker symbol"""
        return

    @abc.abstractmethod
    def create_wallet(self, walletName):
        """creates a new wallet"""
        return

    @abc.abstractmethod
    def get_wallet(self, walletId):
        """returns a specific wallet by wallet id"""
        return

    @abc.abstractmethod
    def get_wallet_balance(self, walletId, currency):
        """returns the balance of a specific currency within a wallet"""
        return

    @abc.abstractmethod
    def get_wallet_trades(self, walletId, filters={}):
        """returns a list of trades for a specific wallet
           results are paginated and limited to a maximum of 50 per request"""
        return

    @abc.abstractmethod
    def get_wallet_orders(self, walletId, filters={}):
        """returns a list of orders for a wallet
           response will be paginated and limited to 50 items per response
           orders can be filtered by status (ex: open, filled, etc) """
        return

    @abc.abstractmethod
    def create_order(self, walletId, side, currency, amount, price, instrument):
        """creates a new limit order"""
        return

    @abc.abstractmethod
    def create_order_with_display(self, walletId, side, currency, amount, price, display, instrument):
        """creates a new limit order with a specific display amount (iceberg order)"""
        return

    @abc.abstractmethod
    def get_order(self, walletId, orderId):
        """returns a specific order by order id"""
        return

    @abc.abstractmethod
    def cancel_order(self, walletId, orderId):
        """cancels an order by order id"""
        return

    @abc.abstractmethod
    def cryptocurrency_withdrawal_request(self, walletId, currency, amount, address):
        """requests a withdrawal to a bitcoin address"""
        return

    @abc.abstractmethod
    def cryptocurrency_deposit_request(self, walletId, currency):
        """returns a new bitcoin address for deposits to a wallet"""
        return

    @abc.abstractmethod
    def create_wallet_transfer(self, sourceWalletId, destinationWalletId, amount, currencyCode):
        """transfers funds of a single currency between two wallets"""
        return
