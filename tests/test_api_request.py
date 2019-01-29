#!/usr/bin/env python
# coding=utf-8

from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException, KucoinRequestException, MarketOrderException, LimitOrderException
import pytest
import requests_mock

api_key = "5c4eb3b1ef83c721c02cb97c"
api_secret = "9589ff2f-c8ac-4ca6-8d72-83f38125c540"
api_passphrase = "1234qwer"
client = Client(api_key, api_secret, api_passphrase, sandbox=True)


def test_currency():
    assert client.get_currency('BTC')['currency'] == 'BTC'


def test_symbols():
    assert len(client.get_symbols()) > 0


def test_currencies():
    assert len(client.get_currencies()) > 0


def test_get_ticker():
    assert len(client.get_ticker('ETH-BTC')) > 0


def test_accounts():
    all_account = client.get_accounts()
    account_id = all_account[0]['id']
    single = client.get_account(account_id)
    assert single['balance'] == all_account[0]['balance']
    assert client.get_account_holds(account_id)['totalNum'] == 0
    # sandbox will deposit for you after registering
    assert client.get_account_history(account_id)['totalNum'] >= 1


def test_get_24hr_stats():
    client.get_24hr_stats('ETH-BTC')


def test_create_account():
    with pytest.raises(KucoinAPIException):
        response = client.create_account('trade', 'BTC')
        assert response['code'] == "230005"


def test_get_trade_histories():
    client.get_trade_histories('ETH-BTC')


def test_timestamp():
    t1 = client.get_timestamp()
    t2 = client.get_timestamp()
    assert t2 - t1 >= 0


def test_orderbook():
    client.get_full_order_book('ETH-BTC')
    client.get_full_order_book_level3('ETH-BTC')


def test_inner_transfer():
    response = client.get_accounts()
    account_map = {}
    for item in response:
        if item['currency'] == 'KCS':
            account_map['KCS' + item['type']] = item
    kcs_main = account_map['KCSmain']
    kcs_trade = account_map['KCStrade']
    client.create_inner_transfer(account_map['KCSmain']['id'], account_map['KCStrade']['id'], 1)
    client.create_inner_transfer(account_map['KCStrade']['id'], account_map['KCSmain']['id'], 1)
    assert client.get_account(kcs_main['id'])['balance'] == kcs_main['balance']
    assert client.get_account(kcs_trade['id'])['balance'] == kcs_trade['balance']


def test_get_deposit_address():
    with pytest.raises(KucoinAPIException):
        client.get_deposit_address('BTC')


def test_market_list():
    client.get_market_list()


def test_create_deposit_address():
    with pytest.raises(KucoinAPIException):
        client.create_deposit_address('BTC')


def test_get_deposit():
    assert client.get_deposits('BTC')['totalNum'] == 0


def test_invalid_json():
    with pytest.raises(KucoinRequestException):
        with requests_mock.mock() as m:
            m.get('https://openapi-sandbox.kucoin.com/api/v1/currencies', text='<head></html>')
            client.get_currencies()


def test_api_exception():
    with pytest.raises(KucoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                "code": "900003",
                "msg": "currency {0} not exists"
            }
            m.get('https://openapi-sandbox.kucoin.com/api/v1/currencies/BTD', json=json_obj, status_code=400)
            client.get_currency('BTD')
