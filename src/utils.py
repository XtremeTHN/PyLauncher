from threading import Thread, Event
import time

class setTimeout(Thread):
    def __init__(self, seconds, cb, *args, **kwargs):
        self.cb = cb
        self.args = args
        self.kwargs = kwargs
        
        self.seconds = seconds
        self.start()
    
    def run(self):
        time.sleep(self.seconds)
        self.cb(*self.cb, **self.kwargs)