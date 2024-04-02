from gi.repository import Gtk, Adw, Gio, WebKit

from modules.variables import MINECRAFT_DIR
from modules.config import LauncherConfig
from modules.utils import set_margins, get_minecraft_versions

from minecraft_launcher_lib.utils import get_installed_versions

import os

class PyLauncherWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(title="PyLauncher", application=app)
        self.nav_stack = []

        self.set_default_size(600, 400)
        self.set_size_request(600, 400)


        self.navigation = Adw.NavigationView.new()

        if os.path.exists(os.path.join(MINECRAFT_DIR)) is False:
            self.show_first_launch()
        else:
            self.show_main_page()

        self.set_content(self.navigation)

        self.present()
    
    def is_on_nav_stack(func):
        tag = func.__name__.replace("_", "-")
        if tag.startswith("show-"):
            tag = tag[5:]
        def wrapper(self, *args, **kwargs):
            for x in self.nav_stack:
                if x.get_tag() == tag:
                    self.navigation.push(x)
                    return
            
            func(self, *args, **kwargs)

        return wrapper

    # Step 1
    def show_first_launch(self):
        page, fl_box, _ = self.create_page("PyLauncher", "first-launch", add_to_nav=False)
        status = Adw.StatusPage(icon_name="minecraft", title="PyLauncher", vexpand=True, description="Welcome to PyLauncher, a Minecraft launcher written in Python!")

        gs_button = Gtk.Button.new_with_label("Continue")
        gs_button.set_halign(Gtk.Align.CENTER)
        gs_button.set_css_classes(["pill", "suggested-action"])

        gs_button.connect('clicked', self.create_minecraft_root, page)

        status.set_child(gs_button)

        fl_box.append(status)

        self.navigation.push(page)

    # Step 2
    def create_minecraft_root(self, _, page):
        MINECRAFT_DIR.mkdir(parents=True, exist_ok=True)
        self.remove_page(page)
        self.show_main_page()

    def create_page(self, title, tag, spacing=10, add_to_nav=True, header=True, add_box=True):
        page = Adw.NavigationPage(title=title, tag=tag)

        toolbar = Adw.ToolbarView()

        content = None
        if add_box is True:
            content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
            toolbar.set_content(content)

        if header is True:
            header_bar = Adw.HeaderBar.new()
            toolbar.add_top_bar(header_bar)

        page.set_child(toolbar)

        if add_to_nav is True:
            self.navigation.add(page)
            self.nav_stack.append(page)

        return page, content, toolbar

    def remove_page(self, page):
        self.navigation.remove(page)
        for index, x in enumerate(self.nav_stack):
            if x is page:
                self.nav_stack.pop(index)
    
    # Step 3/1
    @is_on_nav_stack
    def show_main_page(self):
        self.config = LauncherConfig()
        
        page, _, toolbar = self.create_page("PyLauncher", "main-page", add_to_nav=False, header=False, add_box=False)
        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        stack = Adw.ViewStack.new()
        switcher = Adw.ViewSwitcher(stack=stack, policy=Adw.ViewSwitcherPolicy.WIDE)

        toolbar.set_content(stack)

        header.set_title_widget(switcher)

        self.create_play_page(stack, toolbar)

        self.navigation.replace([page])

    def create_play_page(self, stack: Adw.ViewStack, toolbar: Adw.ToolbarView):
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        set_margins(root_box, [10])

        home_page = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START, vexpand=False)
        home_page.add_css_class("boxed-list")

        launch_btt = Gtk.Button.new_with_label("Launch")
        launch_btt.set_halign(Gtk.Align.CENTER)
        launch_btt.set_css_classes(["pill", "suggested-action"])
        set_margins(launch_btt, [10])

        launch_btt.connect('clicked', self.launch_minecraft)

        toolbar.add_bottom_bar(launch_btt)

        news_row = Adw.ActionRow(activatable=True, title="Minecraft News", 
                                 subtitle="See the latest news about Minecraft!",)
        news_row.add_suffix(Gtk.Image.new_from_icon_name("go-next-symbolic"))
        news_row.connect("activated", self.show_minecraft_news_page)

        home_page.append(news_row)

        minecraft_root_row = Adw.ActionRow(activatable=True, title="Minecraft root", subtitle="Open the Minecraft folder")
        minecraft_root_row.connect("activated", self.open_minecraft_root)

        home_page.append(minecraft_root_row)


        mine_launch_opts = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START, vexpand=False, css_classes=["boxed-list"])
        
        versions_row = Adw.ComboRow(title="Version", subtitle="Select minecraft version you want to play")
        self.versions = get_minecraft_versions()

        if self.config.py_launcher_config["show_snapshots"] is False:
            del self.versions["snapshot"]
        if self.config.py_launcher_config["show_beta_versions"] is False:
            del self.versions["beta"]
        if self.config.py_launcher_config["show_alpha_versions"] is False:
            del self.versions["alpha"]

        versions_model = Gtk.StringList.new(self.versions.join())
        versions_row.set_model(versions_model)

        mine_launch_opts.append(versions_row)

        root_box.append(home_page)
        root_box.append(mine_launch_opts)
        stack.add_titled_with_icon(root_box, "home-page", "Home", "go-home-symbolic")

    def launch_minecraft(self, btt: Gtk.Button):
        btt.set_sensitive(False)
        # selected_version = versions_row.get_selected_item().get_str()    

        for x in get_installed_versions(MINECRAFT_DIR):
            ...
    def open_minecraft_root(self, _):
        Gio.AppInfo.launch_default_for_uri(MINECRAFT_DIR.as_uri())

    @is_on_nav_stack
    def show_minecraft_news_page(self, action):   
        page, content, _ = self.create_page("News", "minecraft-news-page")

        webview = WebKit.WebView.new()
        webview.set_vexpand(True)

        webview.load_uri("https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs")

        content.append(webview)

        self.navigation.push(page)
