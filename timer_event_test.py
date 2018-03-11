import timer_event as te

def display_time(dt):
   print(dt)

def main():
   t = te.TimerEvent(1, display_time)
   t.run()

if __name__ == '__main__':
   main()