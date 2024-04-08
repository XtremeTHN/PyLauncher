from gi.repository import Gio

def timeit(func):
    def wrapper(*args, **kwargs):
        import time
        t1 = time.perf_counter()
        func(*args, **kwargs)
        t2 = time.perf_counter()

        time = t2 - t1
        print(f"Took '{time:.3f}' seconds to complete")
    
    return wrapper

@timeit
def read_gio():
    file = Gio.File.new_for_path("/home/axel/.config/fish/config.fish")
    file.load_contents(None)

@timeit
def read_builtin():
    file = open("/home/axel/.config/fish/config.fish", "r")
    file.read()
read_gio()
read_builtin()
