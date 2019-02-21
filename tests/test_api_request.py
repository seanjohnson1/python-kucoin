#!/usr/bin/env python
# coding=utf-8

from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException, KucoinRequestException, MarketOrderException, LimitOrderException
import pytest
import requests_mock
import uuid

api_key = "5c6e2092ef83c76d7cb3e1d2"
api_secret = "df848eb1-ba44-434c-97de-f36d06dc58a1"
api_passphrase = "kucoin123"
client = Client(api_key, api_secret, api_passphrase, sandbox=True)


def test_currency():
    assert client.get_currency('BTC')['currency'] == 'BTC'


def test_symbols():
    assert len(client.get_symbols()) > 0


def test_currencies():
    assert len(client.get_currencies()) > 0


def test_get_ticker():
    assert len(client.get_ticker('ETH-BTC')) > 0


def test_get_order():
    assert client.get_order('5c63c4aeef83c72f99c71e1a') is not None


def test_create_limit_order():
    client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.0001', '1000',
                              client_oid=str(uuid.uuid4()).replace('-', ''), remark='create limit order')
    client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.0001', '1000', post_only=True)
    client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.0001', '1000', cancel_after='60', time_in_force='GTT')
    client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.00000001', '1000', stop='loss', stop_price='0.00000002')
    client.create_limit_order('KCS-BTC', 'buy', '0.00015', '100', hidden=True)
    client.create_limit_order('KCS-BTC', 'buy', '0.00015', '100', iceberg=True, visible_size='1')
    client.cancel_all_orders()


def test_create_market_order_1():
    client.create_market_order('KCS-BTC', Client.SIDE_BUY, size='1', client_oid=str(uuid.uuid4()).replace('-', ''),
                               remark='create market order')


def test_get_orders():
    client.get_orders()
    # 94665600000 1970/1/1
    assert client.get_orders(start='946656000000', end='946656000000')['totalNum'] == 0
    assert client.get_orders(page=1, page_size=50, symbol='KCS-BTC', status='done', order_type='limit', side='buy',
                             start='1550042780000', end='1550042782000')['totalNum'] == 1


def test_get_withdrawal():
    assert client.get_withdrawals('KCS', 'SUCCESS', '946656000000', '946656000000', 1, 50)['totalNum'] == 0


def test_withdrawal_quota():
    assert float(client.get_withdrawal_quotas('ETH')['usedBTCAmount']) == 0


def test_accounts():
    all_account = client.get_accounts()
    account_id = all_account[0]['id']
    single = client.get_account(account_id)
    assert single['balance'] == all_account[0]['balance']
    assert client.get_account_holds(account_id, 1, 50)['totalNum'] >= 0
    # sandbox will deposit for you after registering
    assert client.get_account_history(account_id='5c51163aef83c72f924574e3')['totalNum'] >= 1
    assert client.get_account_history(account_id='5c51163aef83c72f924574e3', start='1550043119000', end='1550043119000',
                                      page=1, page_size=10)['totalNum'] > 0


def test_get_24hr_stats():
    client.get_24hr_stats('KCS-BTC')


def test_get_kline_data():
    assert len(client.get_kline_data('KCS-BTC')) > 0
    assert len(client.get_kline_data('KCS-BTC', '1hour', 946656000000, 946656000000)) == 0


def test_get_orderbook():
    client.get_order_book('KCS-BTC')


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
    client.create_inner_transfer(account_map['KCSmain']['id'], account_map['KCStrade']['id'], 1,
                                 str(uuid.uuid4()).replace('-', ''))
    client.create_inner_transfer(account_map['KCStrade']['id'], account_map['KCSmain']['id'], 1)
    assert client.get_account(kcs_main['id'])['balance'] == kcs_main['balance']
    assert client.get_account(kcs_trade['id'])['balance'] == kcs_trade['balance']


def test_get_fills():
    assert client.get_fills('5c65138cef83c72f99d948b1')['totalNum'] == 4
    assert client.get_fills(symbol='ABC-BTC', page=1, page_size=50, side='buy', order_type='limit')['totalNum'] == 0
    assert client.get_fills(start='946656000000', end='946656000000')['totalNum'] == 0


def test_get_deposit_address_exception():
    with pytest.raises(KucoinAPIException):
        client.get_deposit_address('BTC')


def test_market_list():
    client.get_market_list()


def test_create_deposit_address_exception():
    with pytest.raises(KucoinAPIException):
        client.create_deposit_address('BTC')


def test_get_deposit():
    response = client.get_deposits('BTC', 'SUCCESS', '946656000000', '946656000000', 1, 66)
    assert response['totalNum'] == 0
    assert response['pageSize'] == 66


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


def test_get_order_exception():
    with pytest.raises(KucoinAPIException):
        client.get_order('dummy')


def test_cancel_order_exception():
    with pytest.raises(KucoinAPIException):
        client.cancel_order('dummy')


def test_withdrawal_exception_1():
    with pytest.raises(KucoinAPIException):
        client.create_withdrawal('KCS', '1', 'dummy')


def test_withdrawal_exception_2():
    with pytest.raises(KucoinAPIException):
        client.create_withdrawal('KCS', '1', 'dummy', 'memo', False, 'remark')


def test_withdrawal_exception_3():
    with pytest.raises(KucoinAPIException):
        client.create_withdrawal('KCS', '1', 'dummy', 'memo', True, 'remark')


def test_withdrawal_exception_4():
    with pytest.raises(KucoinAPIException):
        client.cancel_withdrawal('dummy')


def test_create_limit_order_exception_1():
    with pytest.raises(LimitOrderException):
        client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.01', '1000', stop='True')


def test_create_limit_order_exception_2():
    with pytest.raises(LimitOrderException):
        client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.01', '1000', stop_price='0.02')


def test_create_limit_order_exception_3():
    with pytest.raises(LimitOrderException):
        client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.01', '1000', cancel_after='1m', time_in_force='FOK')


def test_create_limit_order_exception_4():
    with pytest.raises(LimitOrderException):
        client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.01', '1000', hidden=True, iceberg=True)


def test_create_limit_order_exception_5():
    with pytest.raises(LimitOrderException):
        client.create_limit_order('KCS-BTC', Client.SIDE_SELL, '0.01', '1000', iceberg=True)


def test_create_market_order_1():
    with pytest.raises(MarketOrderException):
        client.create_market_order('KCS-BTC', Client.SIDE_SELL, size='1', funds='1')


def test_create_market_order_2():
    with pytest.raises(MarketOrderException):
        client.create_market_order('KCS-BTC', Client.SIDE_SELL)


def test_create_market_order_2():
    client.create_market_order('KCS-BTC', Client.SIDE_BUY, funds='0.0001', stp='CN')
