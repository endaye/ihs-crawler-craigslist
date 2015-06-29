import threading
import time

class BuckysMessage(threading.Thread):
    def run(self):
        for _ in range(10):  # don't care about the variable
            print(threading.currentThread().getName())
            time.sleep(1/100000)  # sleep for 0.01 ms

x = BuckysMessage(name='Send out messages')
y = BuckysMessage(name='Receive messages')
z = BuckysMessage(name='Check messages')
x.start()
y.start()
z.start()