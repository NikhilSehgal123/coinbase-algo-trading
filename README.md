# Coinbase Algo Trading (based on Elon's thoughts..haha)

## Description
- A simple to use repo to automate trading crypto on Coinbase
- It listens to Elon Musk's related accounts (@elonmusk, @tesla, @spacex) in real-time to see if either account is posting anything related to bitcoin
- Each tweet's polarity (sentiment) is analyzed and if the polarity is greater than a specific threshold, the algorithm sends a BUY market order to coinbase

## Under Development
- Advanced algorithm to minimize execution slippage
- Additional statistics to improve execution performance
- Portfolio management to analyze open positions
- VWAP execution algorithm
- PAIRS execution algorithm based on statistical arbitrage vs other crypto pairs

## Getting Started
- Clone this repository
- Sign up for a Coinbase Account
- Generate API credentials for the Coinbase Sandbox Account (https://public.sandbox.pro.coinbase.com/), so you don't run a real P&L initially!!
- Enter your API credentials in the script coinbase_creds.py like the following:
```python
api_secret = "SOME_STRING"
api_key = "SOME_STRING"
api_pass = "SOME_STRING"
```
- Sign up for a twitter developer account and generate API credentials to enter into the twitter_credentials.py script like the following:
```python
# Twitter API Credentials
API_KEY = "SOME_STRING"
API_SECRET_KEY = "SOME_STRING"
BEARER_TOKEN = "SOME_STRING"
ACCESS_TOKEN = "SOME_STRING"
ACCESS_TOKEN_SECRET = "SOME_STRING"
```
- You're now pretty much good to go, just run the following:
```python
python coinbase_algo.py
```
## Under the hood
Just for fun, let's dig into what the coinbase_algo.py script is doing in a bit more detail

- We utilise the cbpro library to open a websocket connection to receive data in real-time from coinbase (please ensure you point to the sandbox before going live!!)
```python
class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url           = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.message_count = 0
        self.initial_date = datetime.now()
```
- We place a market order, worth $1,000, to buy BTC if Elon says something pretty +ve about it
```python
class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url           = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.message_count = 0
        self.initial_date = datetime.now()
```
