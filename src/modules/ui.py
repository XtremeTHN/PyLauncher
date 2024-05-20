from gi.repository import Gtk, Adw, GObject, Gio

from modules.variables import MINECRAFT_DIR
from modules.config import LauncherConfig

from modules.widgets.home import HomePage
from modules.widgets.profiles import ProfilesPage
from modules.widgets.assistant import AssistantPage

from modules.utils import NavContent

import os

class PyLauncherWindow(Adw.ApplicationWindow, NavContent):
    def __init__(self, app):
        app.create_action('quit', self.show_logs)

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
            self.create_main_page()
            
        self.toast.set_child(self.navigation)
    
        self.set_content(self.toast)

        self.present()
    
    
    def create_main_page(self):
        self.config = LauncherConfig()

        # Main page setup
        main_page = Adw.NavigationPage(title="PyLauncher", tag="main-page")
        toolbar = Adw.ToolbarView()
        
        self.navigation.replace([main_page])
        self.nav_stack = [main_page]

        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        toolbar.set_content(self.stack)

        header.set_title_widget(self.switcher)

        main_page.set_child(toolbar)

        header_menu_model = Gio.Menu.new()
        header_menu_model.append("Open logs", detailed_action="app.logs")

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button.set_menu_model(header_menu_model)

        header.pack_end(menu_button)

        # End setup

        profiles = ProfilesPage(self, self.config, header)
        profiles.create_profiles_page()
        
        self.home_obj.config = self.config

        self.home_obj.create_play_page(toolbar)
        
        self.stack.set_visible_child_name("home-page")
