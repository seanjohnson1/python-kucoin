#!/usr/bin/env python
# coding=utf-8

from kucoin.client import Client
import time

api_key = "5c753504ef83c77635824f12"
api_secret = "17d66aff-2b08-4473-9610-aa25e5993841"
api_passphrase = "abcd1234"
client = Client(api_key, api_secret, api_passphrase, sandbox=True)


def on_message(ws, message):
    print("receive a %s" % message)


def test_public_channel():
    client.create_websocket(["/account/balance"], on_message, private=True)
    time.sleep(5)
    client.shutdown()


def test_private_channel():
    client.create_websocket(["/market/level2:ETH-BTC"], on_message)
    time.sleep(5)
    client.shutdown()
