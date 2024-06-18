from threading import Thread, Event
from .style import Logger
from typing import Callable

from pathlib import Path
from glob import glob

from gi.repository import Gtk

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
        
def check_call(*args, wd=None, env=None, buffer=None, can_exit=False, on_error: Callable[[str, str], None]=None) -> bool:
    """Calls an executable and returns/exit if the command exited succesfully

    Args:
        wd (os.PathLike, optional): The working directory where the program will run. Defaults to None.
        env (dict, optional): The environment variables in form of a dict. Defaults to None.
        buffer (file, optional): A file like object to which the output of the command will be written. Defaults to None.
        can_exit (bool, optional): If this function can exit. If yes it wil use Logger.error, otherwise will use Logger.warn. Defaults to False.
        on_error (Callable[[str, str], None], optional): A function that will be called if there was an error. If it's Nonw it will use Logger functions. Defaults to None.

    Returns:
        bool: Returns a bolean wether if the command exited succesfylly. It will return False if can_exit is False, otherwise it will exit
    """
    if on_error is None:
        on_error = Logger.error if can_exit else Logger.warn
    with Popen(args, cwd=wd, env=env, stdout=PIPE) as process:
        if buffer is not None:
            while True:
                try:
                    line = process.stdout.readline()
                except:
                    break

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