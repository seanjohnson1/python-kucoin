#!/usr/bin/env python
# coding=utf-8

from kucoin.exceptions import KucoinAPIException, KucoinRequestException, MarketOrderException, LimitOrderException
import requests
import pytest


def test_kucoin_api_exception():
    e = KucoinAPIException(requests.Response())
    assert str(e) == 'KucoinAPIException : None'


def test_market_order_exception():
    e = MarketOrderException('oops')
    assert str(e) == 'MarketOrderException: oops'


def test_limit_order_exception():
    e = LimitOrderException('oops')
    assert str(e) == 'LimitOrderException: oops'


def test_kucoin_request_xception():
    e = KucoinRequestException('oops')
    assert str(e) == 'KucoinRequestException: oops'
