############################################
BitEx Framework - Bitcoin Exchange REST APIs
############################################

.. image:: https://circleci.com/gh/Crypto-toolbox/bitex-framework.svg?style=svg
    :target: https://app.circleci.com/pipelines/github/Crypto-toolbox/bitex-framework


`Bitex` is a python3 library for making requests to crypto currency exchanges
a breeze. With the ever increasing number of exchanges setting up shop, it becomes
increasingly more difficult to acquire data in a convenient way. This is mostly
due to the fact that each exchange cooks up their own API spec, with no general
consensus on HTTP methods, input format or authentication method.

Bitex aims to abstract the gritty details of exchange APIs away, by supplying
extensions to the popular :mod:`requests` library.

Under the hood, `BitEx` is powered by `Bitex-Framework`, as lightweight framework
laying the foundation for its features.

Features
========

- Easy to use: Bitex is an extension to the :mod:`requests` library, adding
    under-the-hood magic to take care of formatting and authenticating
    requests to exchanges.

- Extensible: Bitex uses :mod:`pluggy` and a simple hook system to allow developers
    to create their own API wrappers. Can't find an extension for the exchange
    of your choice? Simply write your own!

- Sensible set of default methods: Our BitexSession object supplies a robust set
    of common API operations, ranging from requesting market data to order
    modification, as well as withdrawal and deposit methods.

Installation
============

Installation is simple, as it should be::

    pip install bitex-framework

`bitex-framework`, being the core module, does not come with any extensions. But fret not! Plugins for
exchanges are available via pip as well, under the `bitex` namespace like so::

    pip install bitex-${EXCHANGE_NAME}

If you'd like to install the full suite of bells and whistles, try::

    pip install bitex

to install all of bitex's verified REST API plugins along with the core framework module.

Qickstart
=========

After installing, requesting data is easy::

    >>>from bitex import BitexSession
    >>>session = BitexSession()
    # bitex.BitexSession provides a set of methods to execute the most common queries
    >>>r = session.ticker("kraken", "BTCUSD")
    # The response objects returned are bitex.BitexResponses, which behave like regular requests.Response objects.
    >>>r
    <KrakenResponse [200]>
    >>>r.json()
    {
        "error":[],
        "result": {
            "XXBTZUSD":{
                "a":["3809.10000","1","1.000"],
                "b":["3809.00000","1","1.000"],
                "c":["3809.60000","0.11007700"],
                "v":["1378.29558699","4120.69226171"],
                "p":["3798.72908","3797.90051"],
                "t":[1960,5958],
                "l":["3776.90000","3775.80000"],
                "h":["3817.60000","3819.30000"],
                "o":"3796.20000"
            }
        }
    }
    # Additionally, plugins may supply improved data formats for consumptions by other libraries, such as pandas:
    >>>r.key_value_dict()
    {
        "ts": 12432153,
        "error": [],
        "pair": "XXBTZUSD",
        "ask": "3809.10000",
        "ask_whole_lot": "1",
        "ask_lot": "1.000",
        "bid":"3809.00000",
        "bid_whole_lot": "1",
        "bid_lot": "1.000",
        "last_closed": "3809.60000",
        "last_closed_lot": "0.11007700",
        "vol_today": "1378.29558699",
        "vol_24h": "4120.69226171",
        "vwap_today": "3798.72908",
        "vwap_24h": "3797.90051",
        "trades_today": 1960,
        "trades_24h": 5958,
        "low_today": "3776.90000",
        "low_24h": "3775.80000",
        "high_today": "3817.60000",
        "high_24h": "3819.30000",
        "open":"3796.20000"
    }
    # Or for storing them as timestamp-label-value triples
    >>>r.triples()
    [
        (12432153, "error", []),
        (12432153, "pair", "XXBTZUSD"),
        (12432153, "ask", "3809.10000"),
        (12432153, "ask_whole_lot", "1"),
        (12432153, "ask_lot", "1.000"),
        (12432153, "bid":"3809.00000"),
        (12432153, "bid_whole_lot", "1"),
        (12432153, "bid_lot", "1.000"),
        (12432153, "last_closed", "3809.60000"),
        (12432153, "last_closed_lot", "0.11007700"),
        (12432153, "vol_today", "1378.29558699"),
        (12432153, "vol_24h", "4120.69226171"),
        (12432153, "vwap_today", "3798.72908"),
        (12432153, "vwap_24h", "3797.90051"),
        (12432153, "trades_today", 1960,
        (12432153, "trades_24h", 5958,
        (12432153, "low_today", "3776.90000"),
        (12432153, "low_24h", "3775.80000"),
        (12432153, "high_today", "3817.60000"),
        (12432153, "high_24h", "3819.30000"),
        (12432153, "open", "3796.20000"),
    ]

Development
===========

If you're looking to work on or with :mod:`bitex-framework`, you'll want the development
environment setup. We've supplied a few `make` targets to make your life easier::

    # Install bitex and its development requirements
    make development


We also supply targets to run code formatters, linters and tests::

    # Run code formatters
    make pretty

    # Verify code style
    make style-check

    # Run tests via tox
    tox -e testenv

If you'd like to contribute to the project, please have a look at :doc:`CONTRIBUTING.rst`
on some general pointers about how development takes place, what the expected
steps of you are and what requirements we have to merge a PR.