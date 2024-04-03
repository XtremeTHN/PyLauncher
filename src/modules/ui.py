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

        self.set_default_size(600, 600)
        self.set_size_request(600, 600)

        self.navigation = Adw.NavigationView.new()

        self.home_obj = HomePage(self.config, self.nav_stack, self.navigation)

        if os.path.exists(os.path.join(MINECRAFT_DIR)) is False:
            assistant = AssistantPage(self.nav_stack, self.navigation, self.home_obj.show_main_page)
            assistant.show_first_launch()
        else:
            self.home_obj.show_main_page()

        self.set_content(self.navigation)

        self.present()
    
    # Step 5/1
    # def show_main_page(self):