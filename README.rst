================================
Welcome to kucoin-python v2.0.0
================================

.. image:: https://img.shields.io/pypi/v/kucoin-python.svg
    :target: https://pypi.python.org/pypi/kucoin-python

.. image:: https://img.shields.io/pypi/l/kucoin-python.svg
    :target: https://pypi.python.org/pypi/kucoin-python

.. image:: https://img.shields.io/travis/Kucoin/kucoin-python.svg
    :target: https://travis-ci.org/Kucoin/python-kucoin

.. image:: https://img.shields.io/coveralls/Kucoin/kucoin-python.svg
    :target: https://coveralls.io/github/Kucoin/python-kucoin

.. image:: https://img.shields.io/pypi/pyversions/kucoin-python.svg
    :target: https://pypi.python.org/pypi/kucoin-python

This is an official Python wrapper for the `Kucoin exchanges REST API v2 <https://docs.kucoin.com/>`_.
The sdk is under development, the test did not complete.


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

`Generate an API Key <https://www.kucoin.com/account/api>`_ 
or `Generate an API Key in Sandbox <https://sandbox.kucoin.com/account/api>`_ and enable it.

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

    # get accounts
    accounts = client.get_accounts()

