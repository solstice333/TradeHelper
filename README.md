# TradeHelper

## Description

This is meant to be an interactive API to assist with risk management in stock trading, which is probably one of the few things in stock trading that's easy to do, but the math is really redundant, so might as well partially automate it

## Usage

Open a python3 shell within project top-level:

```
$ cd path/to/TradeHelper
$ python3
```

import the GainRiskCalc class

```
>>> from trade_helper import GainRiskCalc as GRC
```

invoke `GainRiskCalc.with_buy_stop()` factory method. First argument is your entry point, second argument is your mental or live stop loss:

```
>>> my_stock = GRC.with_buy_stop(32.14, 31.28) 
```

print out the number of shares you should buy:
```
>>> my_stock.num_shares()
NumShares(shares=46, adjamt=1478.44)
```

The above says buy 46 shares (which will cost a total of $1478.44) such that if the price drops from your entry point ($32.14) to your stop loss ($31.28), you only lose a total of `GRC.DEFAULT_TOL` which is set to $50 by default. This takes into account commission fees `GRC.DEFAULT_COMMISSION` which is set to $5.00 by default. 

To adjust your 1r risk multiplier, simply set `GRC.DEFAULT_TOL` to whatever you'd like:

```
>>> GRC.DEFAULT_TOL = 100
```

To adjust your commission fees, simply set `GRC.DEFAULT_COMMISSION` to whatever you'd like:

```
>>> GRC.DEFAULT_COMMISSION = 10 
```

If you know your cost basis and how many shares you've bought in a previous transaction, to get a GainRiskCalc object, do:

```
>>> stock = GRC.with_cost_basis(32.14, 46)
>>> stock.num_shares()
NumShares(shares=46, adjamt=1478.44)
```
