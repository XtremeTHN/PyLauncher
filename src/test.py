import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from utils import setTimeout
from gi.repository import Gtk, Adw, Gio

@Gtk.Template(filename="ui/main.xml")
class PyLauncherUI(Adw.ApplicationWindow):
    __gtype_name__ = "main_window"
    
    bootstrap_dialog_user_status_revealer: Gtk.Revealer = Gtk.Template.Child()
    bootstrap_dialog_user_status_label: Gtk.Label = Gtk.Template.Child()
    bootstrap_dialog: Adw.Dialog = Gtk.Template.Child()
    profiles_listbox: Gtk.ListBox = Gtk.Template.Child()
    profiles_page: Adw.ViewStackPage = Gtk.Template.Child()
    user_entry: Gtk.Entry = Gtk.Template.Child()
    
    @Gtk.Template.Callback()
    def open_mine_root(self, _):
        ...
    
    @Gtk.Template.Callback()
    def close_dialog(self, _):
        user = self.user_entry.get_text()
        if user == "":
            self.bootstrap_dialog_user_status_label.set_label("Provide a username please")
            self.bootstrap_dialog_user_status_revealer.set_reveal_child(True)
        else:
            self.bootstrap_dialog.force_close()

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.XtremeTHN.PyLauncher1", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        
    def do_activate(self):
        win = PyLauncherUI()
        win.bootstrap_dialog.present(win)
        self.add_window(win)
        
        win.present()

# if __name__ == "__main__":
app = App().run()