from gi.repository import Gtk, Adw, GObject

from modules.variables import MINECRAFT_DIR
from modules.config import LauncherConfig

from modules.widgets.home import HomePage
from modules.widgets.profiles import ProfilesPage
from modules.widgets.assistant import AssistantPage
from modules.utils import NavContent

import os

class PyLauncherWindow(Adw.ApplicationWindow, NavContent):
    def __init__(self, app):
        Adw.ApplicationWindow.__init__(self, title="PyLauncher", application=app)
        NavContent.__init__(self)

        self.nav_stack = []
        self.toast = Adw.ToastOverlay.new()
        self.config: LauncherConfig = None
        
        self.stack = Adw.ViewStack.new()
        self.switcher = Adw.ViewSwitcher(stack=self.stack, policy=Adw.ViewSwitcherPolicy.WIDE)

        self.set_default_size(600, 300)
        self.set_size_request(600, 300)

        self.navigation = Adw.NavigationView.new()

        self.home_obj = HomePage(self)

        if os.path.exists(os.path.join(MINECRAFT_DIR)) is False:
            assistant = AssistantPage(self)
            assistant.show_first_launch()
        else:
            self.show_main_page()
            
        self.toast.set_child(self.navigation)
    
        self.set_content(self.toast)

        self.present()
    
    def show_main_page(self):
        self.config = LauncherConfig()
        
        profiles = ProfilesPage(self, self.config)
        profiles.create_profiles_page()
        
        self.home_obj.config = self.config
        self.home_obj.create_main_page()
        
        self.stack.set_visible_child_name("home-page")
