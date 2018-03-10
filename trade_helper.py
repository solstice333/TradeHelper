from collections import namedtuple

DEFAULT_COMMISSION = 5.00

def ema_conv(days, mins):
   """return the equivalent MA period in mins |mins| 
   given an MA period of days |days|
   """

   return days*24*60/mins

def loss_price(price, perc):
   """return the result of price |price| decreased by |perc| percent (float)"""

   return price - price*perc

def loss_perc(a, b):
   """return the percent decrease associated to price |a| minus price |b|"""

   return (a - b)/a

def gain(sell, buy, money, comm=DEFAULT_COMMISSION):
   """return what the gain would be if buy at |buy| and sell at |sell|, 
   for the amount of shares that |money| can buy. Commissions |comm|
   defaults to 5.00
   """

   Gain = namedtuple('Gain', ['gain', 'shares'])
   shares = num_shares(buy, money)
   return Gain((sell - buy)*shares - comm*2, shares)

def num_shares(buy, money):
   """return number of shares at price |buy| that can be bought 
   with |money|
   """

   return int(money/buy)

def risk(buy, money, max_loss):
   """return the monetary movement that can be allowed with a total loss of
   |max_loss|, if shares are purchased at |buy| with amount |money|. 
   |max_loss| is your 1r multiplier basically
   """

   max_loss = max_loss - DEFAULT_COMMISSION
   shares = num_shares(buy, money)
   return max_loss/shares
