from threading import Thread, Event
from .style import Logger
import time

from subprocess import Popen, PIPE

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
        
def check_call(*args, wd=None, env=None, buffer=None, can_exit=False) -> bool:
    on_error = Logger.error if can_exit else Logger.warn
    with Popen(args, cwd=wd, env=env, stdout=PIPE) as process:
        if buffer is not None:
            while True:
                line = process.stdout.readline()

                if not line:
                    break
                buffer.write(line.decode("utf-8"))
        else:
            process.communicate()
            
        if process.wait() > 0:
            on_error(args[0], "exited with non-zero code")
            return False
        
        Logger.info(args[0], "called successfully")
        return True