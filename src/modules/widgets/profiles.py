from gi.repository import Adw, Gtk, Gio, GLib

from modules.config import LauncherConfig
from modules.variables import DEFAULT_JVM_FLAGS, MINECRAFT_DIR, JAVA_PATH, \
                                DEFAULT_MINECRAFT_WINDOW_WIDTH, DEFAULT_MINECRAFT_WINDOW_HEIGHT
from modules.utils import NavContent, set_margins
from modules.types import ProfileType

class ProfileConfig:
    def __init__(self, profile_widget):
        self.name: str = profile_widget.profile_name

        self.profile_conf: ProfileType = profile_widget.profile_config
        self.config: LauncherConfig = profile_widget.config
        self.window: Adw.ApplicationWindow = profile_widget.window

        self.widget = Adw.NavigationPage(title="Profile config")
        toolbar = Adw.ToolbarView.new()
        
        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        scroll = Gtk.ScrolledWindow()
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        clamp = Adw.Clamp(child=content)

        scroll.set_child(clamp)
        set_margins(content, [10])
        
        group = Adw.PreferencesGroup(title=f"Configuration of {self.profile_conf['name']}", description="Configure the profile settings")
        
        self.activated = Adw.SwitchRow(subtitle="Set this profile as selected", title="Selected", active=self.config.get_selected_profile() == self.profile_conf)
        group.add(self.activated)

        self.name_row = Adw.EntryRow(title="Profile name (Required)", text=self.profile_conf["name"])
        group.add(self.name_row)

        icon_path = self.profile_conf.get("icon","")
        self.icon_row = Adw.ActionRow(title="Profile icon", subtitle=f"Click this to choose the profile icon", activatable=True)
        self.icon = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True, css_classes=["card"])
        set_margins(self.icon, [5, 0, 5, 0])

        if GLib.file_test(icon_path, GLib.FileTest.EXISTS) is True:
            self.icon.set_filename(icon_path)
            self.icon.set_visible(True)
        else:
            self.icon.set_visible(False)
        
        self.icon_row.connect("activated", self.__choose_icon)

        self.icon_row.add_prefix(self.icon)
        group.add(self.icon_row)
        
        self.game_dir = Adw.EntryRow(title="Minecraft directory", text=self.profile_conf.get("gameDir", str(MINECRAFT_DIR)))
        group.add(self.game_dir)
        
        resolution_expand_row = Adw.ExpanderRow(title="Resolution", subtitle="Change the resolution of the window")
        width = self.profile_conf.get("resolution", {}).get("width", DEFAULT_MINECRAFT_WINDOW_WIDTH)
        height = self.profile_conf.get("resolution", {}).get("height", DEFAULT_MINECRAFT_WINDOW_HEIGHT)

        self.res_width = Adw.SpinRow(adjustment=Gtk.Adjustment(value=int(width), upper=GLib.MAXDOUBLE, page_increment=10, step_increment=1), 
                                     title="Width", subtitle="The width of the minecraft window", sensitive=True, value=width)
        self.res_height = Adw.SpinRow(adjustment=Gtk.Adjustment(value=int(height), upper=GLib.MAXDOUBLE, page_increment=10, step_increment=1),
                                      title="Height", subtitle="The height of the minecraft window", value=height)

        resolution_expand_row.add_row(self.res_width)
        resolution_expand_row.add_row(self.res_height)
        
        group.add(resolution_expand_row)
        content.append(group)

        version_selection = Adw.PreferencesGroup(title="Version selection", description="Configure version related settings")

        allowed_releases = self.profile_conf.get("allowedReleaseTypes", [])
        self.allow_snapshots = Adw.SwitchRow(active="spanshots" in allowed_releases, title="Allow snapshots", subtitle="Allow snapshots to be selected")
        version_selection.add(self.allow_snapshots)

        self.allow_old_betas = Adw.SwitchRow(active="beta" in allowed_releases, title="Allow old betas", subtitle="Allow old betas to be selected")
        version_selection.add(self.allow_old_betas)

        self.allow_old_alphas = Adw.SwitchRow(active="alpha" in allowed_releases, title="Allow old alphas", subtitle="Allow old alphas to be selected")
        version_selection.add(self.allow_old_alphas)

        content.append(version_selection)

        java_settings = Adw.PreferencesGroup(title="Java settings", description="Configure java related settings")

        self.java_path = Adw.EntryRow(title="Java path")
        java_settings.add(self.java_path)

        self.java_args = Adw.EntryRow(title="JVM Flags")
        java_settings.add(self.java_args)

        content.append(java_settings)

        apply_button = Gtk.Button.new()
        apply_button_content = Adw.ButtonContent(icon_name="emblem-ok-symbolic", label="Apply")
        apply_button.set_child(apply_button_content)
        set_margins(apply_button, [10])
        
        apply_button.connect("clicked", self.__apply_all)

        self.name_row.connect("notify::text-length", lambda *_: apply_button.set_sensitive(len(self.name_row.get_text()) > 0))

        toolbar.add_bottom_bar(apply_button)

        toolbar.set_content(scroll)
        
        self.widget.set_child(toolbar)
    
    def __apply_all(self, btt):
        name = self.name_row.get_text()
        self.profile_conf["name"] = name

        directory = self.game_dir.get_text()
        if directory is not None:
            self.profile_conf["gameDir"] = directory

        width = self.res_width.get_value()
        height = self.res_height.get_value()
        self.profile_conf["resolution"] = {"width": width, "height": height}

        self.profile_conf["allowedReleaseTypes"] = []
        if self.allow_snapshots.get_active():
            self.profile_conf["allowedReleaseTypes"].append("snapshot")
        if self.allow_old_betas.get_active():
            self.profile_conf["allowedReleaseTypes"].append("beta")
        if self.allow_old_alphas.get_active():
            self.profile_conf["allowedReleaseTypes"].append("alpha")

        if (n:=self.java_path.get_text()) != "":
            self.profile_conf["javaDir"] = n
        if (n:=self.java_args.get_text()) != "":
            self.profile_conf["javaArgs"] = n

        if self.activated.get_active() is True:
            self.config.set_selected_profile(self.name)
        else:
            self.config.set_selected_profile("")

        self.config.save()
    
    def __choose_icon(self, row):
        dialog = Gtk.FileDialog(accept_label="Open")
        dialog.open(self.window, None, callback=self.__file_dial_cb)

    def __file_dial_cb(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult):
        try:
            file = dialog.open_finish(result)
        except:
            return

        if file is not None:
            if file.query_exists(None) is True:
                self.icon.set_filename(file.get_path())
                self.icon.set_visible(True)
                self.profile_conf["icon"] = file.get_path()
                return
            
        self.icon.set_visible(False)

class ProfileWidget(Gtk.Button):
    def __init__(self, profile_page_widget, profile_name: str):
        self.widget = Adw.ActionRow(activatable=True)
        set_margins(self.widget, [4,0,4,0])

        self.config: LauncherConfig = profile_page_widget.config
        self.nav_stack: list[Gtk.Widget] = profile_page_widget.nav_stack
        self.navigation: Adw.NavigationView = profile_page_widget.navigation

        self.window = profile_page_widget.window
        
        self.profile_config = self.config.get_profile(profile_name)
        self.profile_name = profile_name
        
        self.icon = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, css_classes=["card"])
        self.__update_icon()

        self.widget.add_prefix(self.icon)

        self.__update_title()
        self.__update_subtitle()
        
        next_icon = Gtk.Image.new_from_icon_name("applications-system-symbolic")
        self.widget.add_suffix(next_icon)
                
        self.config.connect("changed", self.__update)
        self.widget.connect("activated", self.__activate_cb)
        
    def __update(self, *_):
        self.__update_icon()
        self.__update_title()
        self.__update_subtitle()
    
    def __update_icon(self):
        icon = self.profile_config.get("icon","")
        self.icon.set_filename(icon)
        self.icon.set_visible(icon != "")

    def __update_title(self):
        name = self.profile_config.get("name", "").strip() or "No name"
        profile = self.config.get_selected_profile()
        if profile is not None:
            name += f' {"(Active)" if profile.get("name") == self.profile_config["name"] else ""}'

        self.widget.set_title(name)
    def __update_subtitle(self):
        self.widget.set_subtitle(f'Version: {self.profile_config.get("lastVersionId","latest")}')
    
    def __activate_cb(self, _row) -> None:
        conf = ProfileConfig(self)
        self.navigation.push(conf.widget)
    
class ProfilesPage(NavContent):
    def __init__(self, window, config: LauncherConfig):
        super().__init__()
        self.nav_stack = window.nav_stack
        self.navigation = window.navigation
        self.config = config
        
        self.window = window

        self.stack: Adw.ViewStack = window.stack
    
    def create_profiles_page(self):
        scroll = Gtk.ScrolledWindow()

        clamp = Adw.Clamp(child=scroll)

        content = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START, css_classes=["boxed-list"])

        scroll.set_child(content)

        profiles = list(map(lambda x: ProfileWidget(self, x), self.config.get_profiles_key_names()))
        for x in profiles:
            content.append(x.widget)
        
        self.stack.add_titled_with_icon(clamp, "profiles-page", "Profiles", "preferences-other-symbolic")