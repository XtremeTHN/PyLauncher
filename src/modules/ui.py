from gi.repository import Gtk, Adw, GObject

from modules.variables import MINECRAFT_DIR
from modules.config import LauncherConfig

from modules.widgets.home import HomePage
from modules.widgets.assistant import AssistantPage
from modules.utils import NavContent

import os

class PyLauncherWindow(Adw.ApplicationWindow, NavContent):
    def __init__(self, app):
        Adw.ApplicationWindow.__init__(self, title="PyLauncher", application=app)
        NavContent.__init__(self)

        self.nav_stack = []
        self.config = None
        self.toast = Adw.ToastOverlay.new()
        
        self.stack = Adw.ViewStack.new()
        self.switcher = Adw.ViewSwitcher(stack=self.stack, policy=Adw.ViewSwitcherPolicy.WIDE)

        self.set_default_size(600, 300)
        self.set_size_request(600, 300)

        self.navigation = Adw.NavigationView.new()

        self.home_obj = HomePage(self)

        if os.path.exists(os.path.join(MINECRAFT_DIR)) is False:
            assistant = AssistantPage(self.nav_stack, self.navigation, self.home_obj.show_main_page)
            assistant.show_first_launch()
        else:
            self.home_obj.show_main_page()

        self.toast.set_child(self.navigation)
        self.set_content(self.toast)

        self.present()
    