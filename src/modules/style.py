import sys
import traceback

from colorama import Fore, Style
# from pystyle import Colorate, Colors

DEBUG=False

def bold(msg) -> str:
    return f"{Style.BRIGHT}{msg}{Style.RESET_ALL}"

def underlined(msg) -> str:
    return '\033[4m' + msg + Style.RESET_ALL

def color(string, color) -> str:
    return color + string + Style.RESET_ALL


class _log:
    def __init__(self):
        self.buffer = None
    
    def set_buffer(self, buffer):
        self.buffer = buffer
        
    def info(self,*args):
        func = traceback.extract_stack()[-2]
        string = f"{func.name} > INFO:" if DEBUG is True else "INFO:"
        print(
            underlined(
                bold(
                    color(string, Fore.GREEN)
                    )
                ), *args
            )
        
        if self.buffer is not None:
            self.buffer.write(string)

    def debug(self,*args):
        func = traceback.extract_stack()[-2]
        string = f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > DEBUG:"
        
        if "--debug" in sys.argv:
            print(
                underlined(
                    bold(
                        color(
                            string, Fore.BLUE
                            )
                        )
                    ), *args
                )
        
        if self.buffer is not None:
            self.buffer.write(string)

    def warn(self,*args):
        func = traceback.extract_stack()[-2]
        string = f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > WARNING:" if DEBUG is True else "WARNING:"
        print(
            underlined(
                bold(
                    color(
                        string, Fore.LIGHTRED_EX
                        )
                    )
                ), *args
            )
        
        if self.buffer is not None:
            self.buffer.write(string)

    def error(self,*args, exit_code=1):
        func = traceback.extract_stack()[-2]
        string = f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > ERROR:" if DEBUG is True else "ERROR:"
        print(
            underlined(
                bold(
                    color(
                        string, Fore.RED
                        )
                    )
                ), *args
            )
        
        sys.exit(exit_code)

Logger = _log()