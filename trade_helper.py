from collections import namedtuple

DEFAULT_COMMISSION = 5.00
DEFAULT_TOL = 50
DEFAULT_MONEY = 4e3

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

def stoploss(ema, atr):
   """return |ema| - |atr|"""

   return ema - atr

class GainRiskCalc:
   """interface for common gain/risk calculations"""

   @classmethod
   def with_buy_stop(cls, buy, stop):
      """return a GainRiskCalc object based on the point of purchase |buy|
      and stop |stop|
      """
      gl = cls(buy)
      gl.money = gl.risk_stop(stop)
      return gl

   def __init__(self, buy=0, money=None, comm=None, tol=None):
      """create a GainRiskCalc object with purchase price at |buy|,
      total amount of money |money| that you're willing to play, 
      commissions |comm|, and risk tolerance 1r |tol|. 

      |buy| defaults to 0, |money| defaults to DEFAULT_MONEY, 
      |comm| defaults to DEFAULT_COMMISSION, |tol| defaults to
      DEFAULT_RISK.
      """

      self._money = money or DEFAULT_MONEY
      self._comm = comm or DEFAULT_COMMISSION
      self._tol = tol or DEFAULT_TOL
      self._buy = buy

   def __repr__(self):
      """string representation of self which contains money, comm, tol"""

      return "GainRiskCalc(" + \
         "buy={}, ".format(self._buy) + \
         "money={}, ".format(self._money) + \
         "num_shares={}, ".format(self.num_shares()) + \
         "comm={}, ".format(self._comm) + \
         "tol={})".format(self._tol)

   @property
   def money(self):
      """get money your willing to play"""

      return self._money

   @money.setter
   def money(self, money):
      """set money your willing to play"""

      self._money = money

   @property
   def comm(self):
      """get commissions"""

      return self._comm

   @comm.setter
   def comm(self, comm):
      """set commissions"""

      self._comm = comm

   @property
   def tol(self):
      """get risk tolerance 1r"""

      return self._tol

   @tol.setter
   def tol(self, tol):
      """set risk tolerance 1r"""

      self._tol = tol

   @property
   def buy(self):
      """get the purchase price"""

      return self._buy

   @buy.setter
   def buy(self, purchase):
      """set purchase price"""

      self._buy = purchase

   def gain(self, sell):
      """return what the gain would be if self.buy and sell at |sell|, 
      for the amount of shares that self.money can buy taking into
      account self.comm commissions
      """

      Gain = namedtuple('Gain', ['gain', 'shares'])
      shares = self.num_shares().shares
      return Gain((sell - self._buy)*shares - self._comm*2, shares)

   def num_shares(self):
      """return (number of shares, adjusted total amount) pair
      at price self.buy that can be bought with self.money
      """

      NumShares = namedtuple('NumShares', ['shares', 'adjamt'])
      shares = int(self._money/self._buy)
      return NumShares(shares, shares*self._buy) 

   def risk(self):
      """return the (stop, monetary movement) pair that can be allowed 
      with a total risk of self.tol, if shares are purchased at self.buy 
      with amount self.money. self.tol is your 1r multiplier. In short,
      this tells you where to place your stop, given a certain amount
      of money self.money and the purchase price self.buy.
      """

      Risk = namedtuple('Risk', ['exit', 'move'])
      risk = self._tol - 2*self._comm
      shares = self.num_shares().shares
      move = risk/shares
      return Risk(self._buy - move, move)

   def risk_stop(self, stop):
      """return the money required to achieve the stop price |stop| with 
      max loss of self.tol and purchase at self.buy. Note that between 
      risk() and risk_stop(), risk_stop() is slightly more conservative.
      In short, this tells you how much money to play, given the purchase
      price self.buy and the stop price |stop|. It is typically useful to
      assign the return value to self.money if you decide that's the
      amount to play.
      """

      delta = stop - self._buy
      comm_total = 2*self._comm
      return self._buy*(comm_total - self._tol)/delta
