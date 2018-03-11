import datetime
import asyncio

class TimerEvent:
   def __init__(self, freq, callback):
      self._freq = freq
      self._cb = callback

   async def every_n_min(self):
      while True:
         now_dt = datetime.datetime.now()
         now_time = now_dt.time()
         if now_time.minute % self._freq == 0 and now_time.second == 0:
            self._cb(now_dt)
         await asyncio.sleep(1)

   def run(self):
      loop = asyncio.get_event_loop()
      loop.run_until_complete(self.every_n_min())
      loop.close()

