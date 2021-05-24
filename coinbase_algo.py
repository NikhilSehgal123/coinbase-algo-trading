import cbpro
from slacker import Slacker
from datetime import datetime
slack = Slacker('xoxb-2078533751079-2093419260002-lPKnfTFHqB0p3WBmTvM9Rbnd')
from coinbase_creds import api_key, api_secret, api_pass
from streamer import get_elons_tweets
import numpy as np
import pandas as df

# Example of how to use slack functionality in python
# message = 'Initializing'
# slack.chat.post_message('#algo-trader', message)

# Define the websocket to connect to
class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url           = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.message_count = 0
        self.initial_date = datetime.now()
    
    def on_message(self,msg):
        self.message_count += 1
        msg_type = msg.get('type',None)
        if msg_type == 'ticker':
            time_val =   msg.get('time',('-'*27))
            price_val =  msg.get('price',None)
            bid_val =    msg.get('best_bid', None)
            ask_val =    msg.get('best_ask', None)
            if price_val is not None:
                price_val = float(price_val)
            if bid_val is not None:
                bid_val = float(bid_val)
            if ask_val is not None:
                ask_val = float(ask_val)
                
            spread_val = ask_val - bid_val
            product_id = msg.get('product_id',None)

            print('Product %s | Time_val %s | Price %s | Bid %s | Ask %s' % (product_id, time_val, price_val, bid_val, ask_val))

            # ------------------------
            # Trade based on the below
            # ------------------------
            
            # Get df with Elon's related tweets from
            df = get_elons_tweets()
            # Filter the df to listen out for upcoming tweets
            filtered_df = df[(df['date'] > self.initial_date) & (df['crypto_mention'] == True)]

            if len(filtered_df) < 1:
                print('Nothing to look for yet')
            else:
                # Get average polarity
                sentiment_array = np.array(filtered_df['sentiment'])
                average_polarity = np.mean(sentiment_array)

                # Check if the statements are +ve enough
                if average_polarity > 0.6:
                    # Send a buy order to coinbase for $1000 of bitcoin
                    # # Authenticated Client
                    url='https://api-public.sandbox.pro.coinbase.com'

                    client = cbpro.AuthenticatedClient(
                        api_key,
                        api_secret,
                        api_pass,
                        api_url=url
                    )
                    client.place_market_order(product_id='BTC-USD',side='buy',funds=1000)
    
    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")

# Clever execution algorithm to be developed at a later stage
class MarketMakerAlgo():
    
    def __init__(self):
        self.open_positions = 0
        self.best_bid = 0
        self.best_ask = 0
        self.last_trade = 0
        self.spread = 0
        self.account_balance = 0
        
    def calc_VWAP(self):
        self.price = []
        self.volume = []
        self.vwap = np.sum(self.price * self.volume)/np.sum(self.volume)
        
    def update_info(self, open, bid, ask, last, spread):
        self.open_positions = open
        self.best_bid = bid
        self.best_ask = ask
        self.last_trade = last
        self.spread = spread
        self.account_balance = 0






if __name__ == '__main__':
    # # Authenticated Client
    # url='https://api-public.sandbox.pro.coinbase.com'

    # client = cbpro.AuthenticatedClient(
    #     api_key,
    #     api_secret,
    #     api_pass,
    #     api_url=url
    # )

    # client.place_market_order(product_id='BTC-USD',side='buy',funds=1000)

    stream = TextWebsocketClient(products=['BTC-USD'],channels=['ticker'])
    stream.start()