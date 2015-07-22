import threading


class Messenger(threading.Thread):
    def run(self):
        for _ in range(10):
            print(threading.currentThread().getName())


x = Messenger(name='Send out messages')
y = Messenger(name='Receive messages')
x.start()
y.start()
