import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio

res = Gio.Resource.load("resources/com.github.XtremeTHN.PyLauncherUI.gresource")
Gio.resources_register(res)

from backend.config import LauncherConfig

from frontend.profiles import ProfileRow
from frontend.first_dialog import BootstrapDialog


@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/main.ui")
class PyLauncherUI(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"
    profiles_listbox: Gtk.ListBox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bootstrap = BootstrapDialog()
        bootstrap.present(self)
    
        self.__update(None, None)
        LauncherConfig.connect("changed", self.__update)
        
        self.present()
    
    def __update(self, _, __):
        while (n:=self.profiles_listbox.get_first_child()) is not None:
            self.profiles_listbox.remove(n)
        
        for x in LauncherConfig.get_profiles().values():
            # profile = LauncherConfig.get_profile(x)
            self.profiles_listbox.append(ProfileRow(x))
    
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