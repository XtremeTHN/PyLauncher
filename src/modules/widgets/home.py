from gi.repository import Gtk, Adw, Gio, WebKit

from modules.utils import NavContent, set_margins, get_minecraft_versions, idle, generate_minecraft_options
from modules.config import LauncherConfig
from modules.variables import MINECRAFT_DIR

from minecraft_launcher_lib.utils import get_installed_versions, get_latest_version
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.command import get_minecraft_command

from subprocess import Popen

import threading


class HomePage(NavContent):
    def __init__(self, config, nav_stack, navigation_view):
        self.nav_stack = nav_stack
        self.navigation = navigation_view
        self.config: LauncherConfig = config

    def show_main_page(self):
        self.config = self.config or LauncherConfig()
        page, _, toolbar = self.create_page("PyLauncher", "main-page", add_to_nav=False, header=False, add_box=False)
        self.navigation.replace([page])
        self.nav_stack = [page]

        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        stack = Adw.ViewStack.new()
        switcher = Adw.ViewSwitcher(stack=stack, policy=Adw.ViewSwitcherPolicy.WIDE)

        toolbar.set_content(stack)

        header.set_title_widget(switcher)

        self.create_play_page(stack, toolbar)
        self.navigation.push(page)

    def create_play_page(self, stack: Adw.ViewStack, toolbar: Adw.ToolbarView):
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        set_margins(root_box, [10])

        home_page = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START, vexpand=False)
        home_page.add_css_class("boxed-list")

        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        launch_btt = Gtk.Button(label="Launch", halign=Gtk.Align.CENTER, 
                                css_classes=["pill", "suggested-action"])
        set_margins(launch_btt, [10])

        # launch_btt.set_size_request(300, -1)
 
        bottom_bar.append(launch_btt)

        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, visible=False, spacing=2)

        label_progress = Gtk.Label(label="")
        progress_bar = Gtk.ProgressBar()

        progress_box.append(label_progress)
        progress_box.append(progress_bar)

        bottom_bar.append(progress_box)

        launch_btt.connect('clicked', self.install_minecraft, progress_box, label_progress, progress_bar)

        toolbar.add_bottom_bar(bottom_bar)

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

        _versions_list = ["latest"] + self.versions.join()
        versions_model = Gtk.StringList.new(_versions_list)
        versions_row.set_model(versions_model)

        versions_row.connect("notify::selected-item", self.set_selected_version)

        profile = self.config.get_selected_profile()
        for index, value in enumerate(_versions_list):
            if value.split(" ")[-1] == profile["lastVersionId"]:
                versions_row.set_selected(index)
                break

        mine_launch_opts.append(versions_row)

        current_profile = Adw.ActionRow(title="Profile selected", subtitle=self.config.get_selected_profile()["name"], css_classes=["property"])
        self.config.connect("changed", lambda x: current_profile.set_subtitle(self.config.get_selected_profile()["name"]))

        current_user = Adw.ActionRow(title="User selected", subtitle=self.config.get_selected_user()["displayName"], css_classes=["property"])
        self.config.connect("changed", lambda x: current_user.set_subtitle(self.config.get_selected_user()["name"]))

        mine_launch_opts.append(current_profile)
        mine_launch_opts.append(current_user)

        root_box.append(home_page)
        root_box.append(mine_launch_opts)
        stack.add_titled_with_icon(root_box, "home-page", "Home", "go-home-symbolic")
    
    def set_selected_version(self, combo: Adw.ComboRow, _):
        version: str = combo.get_selected_item().get_string()
        self.config.get_selected_profile()["lastVersionId"] = version.split(" ")[-1]
        self.config.save()

    def install_minecraft(self, btt: Gtk.Button, box: Gtk.Box, label: Gtk.Label, progress_bar: Gtk.ProgressBar):
        btt.set_sensitive(False)

        profile = self.config.get_selected_profile()
        version = list(filter(lambda x: x["id"] == profile.get("lastVersionId"), get_installed_versions(MINECRAFT_DIR)))
        if len(version) == 0: 
            btt.set_visible(False)
            box.set_visible(True)

            versionId = profile.get("lastVersionId")
            if versionId is None:
                versionId = "latest"

            if versionId == "latest":
                versionId = get_latest_version()["release"]

            threading.Thread(target=install_minecraft_version, args=[versionId, MINECRAFT_DIR, {
                "setStatus": lambda x: self.set_status(x, label, box, btt),
                "setProgress": lambda _: self.set_progress(progress_bar)
            }]).start()
    
    # Executed on another thread
    def launch_minecraft(self, btt):
        profile = self.config.get_selected_profile()
        user = self.config.get_selected_user()
        version = profile["lastVersionId"]

        if version == "latest":
            version = get_latest_version()["release"]

        command = get_minecraft_command(version, MINECRAFT_DIR, generate_minecraft_options(user))

        with Popen(command) as process:
            process.wait()
            idle(btt.set_sensitive, True)

    def set_status(self, status, label, box, btt):
        if status == "Installation complete":
            idle(box.set_visible, False)
            idle(btt.set_visible, True)

            self.launch_minecraft(btt)

        idle(label.set_label, status)
    
    def set_progress(self, progress_bar: Gtk.ProgressBar):
        idle(progress_bar.pulse)

    # Below functions are executed on main thread... Maybe idk.
    def open_minecraft_root(self, _):
        Gio.AppInfo.launch_default_for_uri(MINECRAFT_DIR.as_uri())

    def show_minecraft_news_page(self, action):   
        page, content, _ = self.create_page("News", "minecraft-news-page")
        if page is None:
            self.navigation.push_by_tag("minecraft-news-page")

        webview = WebKit.WebView.new()
        webview.set_vexpand(True)

        webview.load_uri("https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs")

        content.append(webview)

        self.navigation.push(page)
