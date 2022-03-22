import websocket
import json
import pprint
import talib
import numpy
import config
from binance.client import Client
from binance.enums import *

symbol = "ethusdt"
interval = "1m"
socket = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"

rsi_period = 14
rsi_overbought = 70
rsi_oversold = 30
trade_symbol = "ETHUSDT"
trade_quantity = 0.05

closes = []
bought_eth = False

client = Client(config.API_KEY, config.API_SECRET, tld='com')


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        return False

    return True


def on_open(ws):
    print('opened connected')


def on_close(ws, *args):
    print('closed connection')


def on_message(ws, message):
    global closes
    global bought_eth

    print('received message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print(f"candle closed at {close}")
        closes.append(float(close))
        print(closes)

        if len(closes) > rsi_period:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, rsi_period)
            print("######## all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print(f"the current rsi is {last_rsi}")

            if last_rsi > rsi_overbought:
                if bought_eth:
                    print("Overbought!!! Sell! Sell! Sell!")
                    order_succeeeded = order(
                        SIDE_SELL, trade_quantity, trade_symbol)
                    if order_succeeeded:
                        bought_eth = False
                    #sell in binance
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")

            if last_rsi < rsi_oversold:
                if bought_eth:
                    print("it is oversold, but you already own it, nothing to do.")
                else:
                    print("OVERSOLD! BUY BUY BUY!!!")
                    #buy in binance
                    order_succeeeded = order(
                        SIDE_BUY, trade_quantity, trade_symbol)
                    if order_succeeeded:
                        bought_eth = True


def on_error(ws, error):
    print(error)
    print('we have an error')


ws = websocket.WebSocketApp(socket, on_open=on_open,
                            on_message=on_message, on_close=on_close, on_error=on_error)


ws.run_forever()
