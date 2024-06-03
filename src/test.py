import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio

@Gtk.Template(filename="ui/main.xml")
class PyLauncherUI(Adw.ApplicationWindow):
    __gtype_name__ = "main-window"

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.XtremeTHN.PyLauncher1", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        
    def do_activate(self):
        win = PyLauncherUI()
        self.add_window(win)
        
        win.present()

# if __name__ == "__main__":
app = App().run()
print("As")