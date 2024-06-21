import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio

from pylauncher.backend.paths import RESOURCES_FILE

# res = Gio.Resource.load("resources/com.github.XtremeTHN.PyLauncherUI.gresource")
res = Gio.Resource.load(str(RESOURCES_FILE))
Gio.resources_register(res)

from pylauncher.backend.config import LauncherConfig

from pylauncher.frontend.profiles import ProfileRow
from pylauncher.frontend.first_dialog import BootstrapDialog


@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/main.ui")
class PyLauncherUI(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"
    nav: Adw.NavigationView = Gtk.Template.Child()
    profiles_listbox: Gtk.ListBox = Gtk.Template.Child()

    def __init__(self, app, **kwargs):
        super().__init__(application=app, **kwargs)
        if LauncherConfig.is_first_launch():
            bootstrap = BootstrapDialog()
            bootstrap.present(self)
    
        self.__update(None, None)
        LauncherConfig.connect("changed", self.__update)
        
        self.present()
    
    def __update(self, _, __):
        while (n:=self.profiles_listbox.get_first_child()) is not None:
            self.profiles_listbox.remove(n)
        
        for x in LauncherConfig.get_profiles().values():
            self.profiles_listbox.append(ProfileRow(x, self))
    
    @Gtk.Template.Callback()
    def on_minecraft_root_clicked(self, _):
        ...

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.XtremeTHN.PyLauncher1", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
                
    def do_activate(self):        
        self.win = self.props.active_window
        if not self.win:
            self.win = PyLauncherUI(self)
            # self.add_window(self.win)
            
        # self.create_action("p")
            
    def create_action(self,name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)

        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)

def main():
    try:
        return App().run()
    except (KeyboardInterrupt, EOFError):
        return 1