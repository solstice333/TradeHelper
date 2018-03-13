class EMA:
   def __init__(self, period, ema_prev):
      self._period = period
      self._ema_prev = ema_prev

   def _K(self):
      return 2/(self._period + 1)

   def next(self, close):
      next_ema = self._ema_prev + self._K()*(close - self._ema_prev)
      self._ema_prev = next_ema
      return next_ema
