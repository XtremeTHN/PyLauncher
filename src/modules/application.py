import gi
gi.require_versions({
    "Gtk": "4.0",
    "Adw": "1",
    "WebKit": "6.0",
    "GdkPixbuf": "2.0",
})

from gi.repository import Gtk, Adw, Gio
from modules.ui import PyLauncherWindow

class App(Adw.Application):    
    def __init__(self):
        super().__init__(
            application_id="com.github.XtremeTHN.PyLauncher",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
    
    def do_activate(self) -> None:
        self.win = self.props.active_window
        if not self.win:
            self.win = PyLauncherWindow(self)
        
        self.create_action('quit', self.exit_app, ['<primary>q'])
    
    def exit_app(self, action, param):
        self.quit()
    
    def create_action(self,name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)

        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)