================================
Welcome to python-kucoin v2.0.0
================================

.. image:: https://img.shields.io/pypi/v/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/l/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/travis/sammchardy/python-kucoin.svg
    :target: https://travis-ci.org/sammchardy/python-kucoin

.. image:: https://img.shields.io/coveralls/sammchardy/python-kucoin.svg
    :target: https://coveralls.io/github/sammchardy/python-kucoin

.. image:: https://img.shields.io/pypi/wheel/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/pyversions/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

This is an official Python wrapper for the `Kucoin exchanges REST API v2 <https://docs.kucoin.com/>`_.


Features
--------

- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling

TODO
----

- Implement websockets

Quick Start
-----------

Register an account with `Kucoin <https://www.kucoin.com>`_.

To test on the Sandbox register with `Kucoin Sandbox <https://sandbox.kucoin.com/ucenter/signup>`_.

`Generate an API Key <https://kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install kucoin-python

.. code:: python

    from kucoin.client import Client

    # connect to production
    client = Client(api_key, api_secret, api_passphrase)

    # connect to sandbox
    client = Client(api_key, api_secret, api_passphrase, sandbox=True)

    # get currencies
    currencies = client.get_currencies()

    # get market depth
    depth = client.get_order_book('KCS-BTC')

    # get symbol klines
    klines = client.get_kline_dat('KCS-BTC')

    # place a market buy order
    order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)

    # get list of active orders
    orders = client.get_active_orders('KCS-BTC')


For more `check out the documentation <https://python-kucoin.readthedocs.io/en/latest/>`_.

