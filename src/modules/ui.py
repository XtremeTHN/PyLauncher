from gi.repository import Gtk, Adw, Gio, WebKit

from modules.variables import MINECRAFT_DIR
from modules.config import LauncherConfig

import os

class PyLauncherWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(title="PyLauncher", application=app)
        self.set_default_size(600, 400)
        self.set_size_request(600, 400)


        self.navigation = Adw.NavigationView.new()

        if os.path.exists(os.path.join(MINECRAFT_DIR)) is False:
            self.show_first_launch()
        else:
            self.show_main_page()

        self.set_content(self.navigation)

        self.present()
    
    # Step 1
    def show_first_launch(self):
        page, fl_box, _ = self.create_page("PyLauncher", "first-launch", add_to_nav=False)
        status = Adw.StatusPage(icon_name="minecraft", title="PyLauncher", vexpand=True, description="Welcome to PyLauncher, a Minecraft launcher written in Python!")

        gs_button = Gtk.Button.new_with_label("Continue")
        gs_button.set_halign(Gtk.Align.CENTER)
        gs_button.set_css_classes(["pill", "suggested-action"])

        gs_button.connect('clicked', self.create_minecraft_root)

        status.set_child(gs_button)

        fl_box.append(status)

        self.navigation.push(page)

    # Step 2
    def create_minecraft_root(self, _):
        MINECRAFT_DIR.mkdir(parents=True, exist_ok=True)

        self.show_main_page()

    def create_page(self, title, tag, spacing=10, add_to_nav=True, header=True, add_box=True):
        page = Adw.NavigationPage(title=title, tag=tag)

        toolbar = Adw.ToolbarView(vexpand=True)

        content = None
        if add_box is True:
            content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True, spacing=spacing)
            toolbar.set_content(content)

        if header is True:
            header_bar = Adw.HeaderBar.new()
            toolbar.add_top_bar(header_bar)

        page.set_child(toolbar)

        if add_to_nav is True:
            self.navigation.add(page)

        return page, content, toolbar
    
    # Step 3/1
    def show_main_page(self):
        self.config = LauncherConfig()
        
        page, _, toolbar = self.create_page("PyLauncher", "main-page", add_to_nav=False, header=False, add_box=False)
        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        stack = Adw.ViewStack.new()
        switcher = Adw.ViewSwitcher(stack=stack, policy=Adw.ViewSwitcherPolicy.WIDE)

        toolbar.set_content(stack)

        header.set_title_widget(switcher)

        self.create_play_page(stack)

        self.navigation.replace([page])

    def create_play_page(self, stack: Adw.ViewStack):

        home_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True, spacing=10)

        

        stack.add_titled_with_icon(home_page, "home-page", "Home", "go-home-symbolic")
