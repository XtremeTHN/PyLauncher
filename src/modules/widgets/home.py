import subprocess
import shlex

from gi.repository import Gtk, Adw, Gio, WebKit, GLib

from modules.utils import NavContent, set_margins, get_minecraft_versions, idle, generate_minecraft_options
from modules.config import LauncherConfig
from modules.variables import MINECRAFT_DIR

from modules.widgets.logs import LogView

from minecraft_launcher_lib.utils import get_installed_versions, get_latest_version
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.command import get_minecraft_command

from subprocess import Popen

import threading


class HomePage(NavContent):
    def __init__(self, window):
        self.nav_stack: list[Gtk.Widget] = window.nav_stack
        self.navigation: Adw.NavigationView = window.navigation
        self.config: LauncherConfig = window.config
        self.toast: Adw.ToastOverlay = window.toast
        
        self.stack: Adw.ViewStack = window.stack
        self.switcher: Adw.ViewSwitcher = window.switcher
         
        self.logger: LogView

    def create_play_page(self, toolbar: Adw.ToolbarView):
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        clamp = Adw.Clamp(child=root_box)

        home_page = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START, vexpand=False)
        home_page.add_css_class("boxed-list")

        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        launch_btt = Gtk.Button(label="Launch", halign=Gtk.Align.CENTER, 
                                css_classes=["pill", "suggested-action"])
        set_margins(launch_btt, [10])
 
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
        self.__update_versions_model(None, versions_row)

        self.config.connect("changed", self.__update_versions_model, versions_row)

        versions_row.connect("notify::selected-item", self.set_selected_version)

        mine_launch_opts.append(versions_row)

        # user = self.config.get_selected_user()
        current_profile = Adw.ActionRow(title="Profile selected", subtitle=self.config.get_selected_profile().get("name", "None"), css_classes=["property"])
        self.config.connect("changed", lambda _: current_profile.set_subtitle(self.config.get_selected_profile().get("name", "None")))

        current_user = Adw.ActionRow(title="User selected", subtitle=self.config.get_selected_user().get("displayName", "None"), css_classes=["property"])
        self.config.connect("changed", lambda _: current_user.set_subtitle(self.config.get_selected_user().get("displayName", "None")))

        mine_launch_opts.append(current_profile)
        mine_launch_opts.append(current_user)

        root_box.append(home_page)
        root_box.append(mine_launch_opts)
        
        self.stack.add_titled_with_icon(clamp, "home-page", "Home", "go-home-symbolic")
    
    def __update_versions_model(self, _, combo: Adw.ComboRow):
        current_profile = self.config.get_selected_profile()
        if current_profile == {}:
            return
        
        versions = get_minecraft_versions()

        allowed_versions = current_profile.get("allowedReleaseTypes", [])
        if "snapshot" not in allowed_versions:
            del versions["snapshot"]
        if "beta" not in allowed_versions:
            del versions["beta"]
        if "alpha" not in allowed_versions:
            del versions["alpha"]
        
        _versions_list = ["latest"] + versions.join()

        versions_model = Gtk.StringList.new(_versions_list)
        combo.set_model(versions_model)

        if current_profile is not None:
            for index, value in enumerate(_versions_list):
                if value.split(" ")[-1] == current_profile.get("lastVersionId"):
                    combo.set_selected(index)
                    break
    
    def set_selected_version(self, combo: Adw.ComboRow, _):
        version: str = combo.get_selected_item().get_string()
        self.config.get_selected_profile()["lastVersionId"] = version.split(" ")[-1]
        self.config.save(notify=False)

    def install_minecraft(self, btt: Gtk.Button, box: Gtk.Box, label: Gtk.Label, progress_bar: Gtk.ProgressBar):
        btt.set_sensitive(False)
        btt.set_label("Launching...")

        profile = self.config.get_selected_profile()
        version = list(filter(lambda x: x["id"] == profile.get("lastVersionId"), get_installed_versions(MINECRAFT_DIR)))
        if len(version) == 0: 
            btt.set_visible(False)
            box.set_visible(True)

            versionId = profile.get("lastVersionId","latest")

            if versionId == "latest":
                versionId = get_latest_version()["release"]

            threading.Thread(target=install_minecraft_version, args=[versionId, MINECRAFT_DIR, {
                "setStatus": lambda x: self.set_status(x, label, box, btt),
                "setProgress": lambda _: self.set_progress(progress_bar)
            }]).start()
            return
        else:
            threading.Thread(target=self.launch_minecraft, args=[btt]).start()
    
    # Executed on another thread
    def launch_minecraft(self, btt):
        profile = self.config.get_selected_profile()
        user = self.config.get_selected_user()
        version = profile.get("lastVersionId", "latest")

        if version == "latest":
            version = get_latest_version()["release"]
        elif version == "latest-snapshot":
            version = get_latest_version()["snapshot"]

        options = generate_minecraft_options(user)

        jvm_args = profile.get("javaArgs", "")
        if jvm_args is not None:
            options["jvmArguments"] = shlex.split(jvm_args)
        options["executablePath"] = profile.get("javaDir", "")
        
        if profile.get("resolution") is not None:
            options["customResolution"] = True
            options["resolutionWidth"] = str(profile.get("resolution", {}).get("width", ""))
            options["resolutionHeight"] = str(profile.get("resolution", {}).get("height", ""))
        
        options["gameDirectory"] = profile.get("gameDir", "")

        command = get_minecraft_command(version, MINECRAFT_DIR, options)

        with Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=MINECRAFT_DIR) as process:
            idle(btt.set_label, "Launched")
            self.notify("Minecraft Launched. You can see minecraft logs on the logs page")

            idle(self.logger.clear)
            while True:
                line = process.stdout.readline()

                if not line:
                    break
                idle(self.logger.write, line.decode("utf-8"))
            self.restart_button_state(btt)

    def set_status(self, status, label, box, btt):
        if status == "Installation complete":
            idle(box.set_visible, False)
            idle(btt.set_visible, True)

            self.launch_minecraft(btt)

        idle(label.set_label, status)

    def restart_button_state(self, btt: Gtk.Button):
        idle(btt.set_visible, True)
        idle(btt.set_sensitive, True)
        idle(btt.set_label, "Launch")
        idle(btt.set_css_classes, ["pill", "suggested-action"])
    
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
