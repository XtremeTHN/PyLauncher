import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from modules.utils import setTimeout
from gi.repository import Gtk, Adw, Gio

res = Gio.Resource.load("resources/com.github.XtremeTHN.PyLauncherUI.gresource")
Gio.resources_register(res)

@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/bootstrap-dialog.ui")
class BootstrapDialog(Adw.Dialog):
    __gtype_name__ = "BootstrapDialog"
    bootstrap_dialog_user_status_revealer: Gtk.Revealer = Gtk.Template.Child()
    bootstrap_dialog_user_status_label: Gtk.Label = Gtk.Template.Child()
    user_entry: Gtk.Entry = Gtk.Template.Child()
    
    @Gtk.Template.Callback()
    def on_bootstrap_dialog_user_creation_finished(self, _):
        user = self.user_entry.get_text()
        if user == "":
            self.bootstrap_dialog_user_status_label.set_label("Provide a username please")
            self.bootstrap_dialog_user_status_revealer.set_reveal_child(True)
        else:
            self.force_close()

@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/main.ui")
class PyLauncherUI(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"
    profiles_listbox: Gtk.ListBox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bootstrap = BootstrapDialog()
        bootstrap.present(self)
        
        self.present()
    
    @Gtk.Template.Callback()
    def on_minecraft_root_clicked(self, _):
        ...

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.XtremeTHN.PyLauncher1", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        
    def do_activate(self):        
        self.win = self.props.active_window
        if not self.win:
            self.win = PyLauncherUI()
            self.add_window(self.win)
# if __name__ == "__main__":

app = App().run()