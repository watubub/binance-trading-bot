# Binance Trading Bot

This bot trades between Ethereum and USDT on the Binance platform. It uses the RSI indicator by looking at the last 14 one-minute candles and trades at the 30/70 thresholds. Although this code effectively uses websockets, the trading strategy is very rudimentary. If you intend on using this code to trade in this market, I'd recommend you look into further trading strategies or, at the very least, add a stop-loss.

This was heavily inspired by [Part Time Larry](https://www.youtube.com/c/parttimelarry). I recommend checking out his [youtube channel](https://www.youtube.com/c/parttimelarry) for more related content.

## Requirements

To run this code, you'll need a binance account and python3. You'll also need to install the following libraries:
* python-binance
* TA-lib
* numpy
* websocket_client
* json

Although the 'pprint' library isn't required for using the code, it is recommended to view the incoming data more easily.

You'll also need to update config.py with your binance API values. These are unique to your account and you should not share them with anyone.
