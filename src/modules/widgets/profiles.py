from gi.repository import Adw, Gtk, Gio, GLib

from modules.config import LauncherConfig
from modules.variables import DEFAULT_JVM_FLAGS, MINECRAFT_DIR, JAVA_PATH, \
                                DEFAULT_MINECRAFT_WINDOW_WIDTH, DEFAULT_MINECRAFT_WINDOW_HEIGHT
from modules.utils import NavContent, StyledButton, set_margins
from modules.types import ProfileType

class ProfileConfig:
    def __init__(self, profile_widget):
        self.name: str = profile_widget.profile_name

        self.profile_conf: ProfileType = profile_widget.profile_config
        self.config: LauncherConfig = profile_widget.config
        self.window: Adw.ApplicationWindow = profile_widget.window

        self.navigation: Adw.NavigationView = profile_widget.navigation

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

        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5, homogeneous=True)
        set_margins(bottom_bar, [10])

        apply_button = StyledButton("Apply changes", "emblem-ok-symbolic", "suggested-action")
        apply_button.connect("clicked", self.__apply_all)
        bottom_bar.append(apply_button)

        cancel_button = StyledButton("Remove profile", "user-trash-symbolic", "destructive-action")
        cancel_button.connect("clicked", self.__remove_profile)
        bottom_bar.append(cancel_button)

        self.name_row.connect("notify::text-length", lambda *_: apply_button.set_sensitive(len(self.name_row.get_text()) > 0))

        toolbar.add_bottom_bar(bottom_bar)

        toolbar.set_content(scroll)
        
        self.widget.set_child(toolbar)
    
    def __remove_profile(self, _):
        self.config.remove_profile(self.name, save=True)
        self.navigation.pop()
        
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

class ProfileWidget(Gtk.Button):
    def __init__(self, profile_page_widget, profile_name: str):
        self.widget = Adw.ActionRow(activatable=True)

        self.config: LauncherConfig = profile_page_widget.config
        self.nav_stack: list[Gtk.Widget] = profile_page_widget.nav_stack
        self.navigation: Adw.NavigationView = profile_page_widget.navigation

        self.window = profile_page_widget.window
        
        self.profile_config = self.config.get_profile(profile_name)
        self.profile_name = profile_name
        
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
    def __init__(self, window, config: LauncherConfig, header: Adw.HeaderBar):
        super().__init__()

        self.nav_stack = window.nav_stack
        self.navigation = window.navigation
        self.config = config
        
        self.window = window
        self.header: Adw.HeaderBar = header

        self.stack: Adw.ViewStack = window.stack

        self.add_btt = Gtk.Button.new_from_icon_name("list-add-symbolic")
        self.add_btt.connect("clicked", self.open_profile_dialog)

        self.stack.connect("notify::visible-child", self.toggle_add_button)
    
    def toggle_add_button(self, *_):
        if self.stack.get_visible_child_name() == "profiles-page":
            self.header.pack_start(self.add_btt)
        else:
            if self.add_btt.get_parent() is not None:
                self.header.remove(self.add_btt)
    
    def add_profile(self, name):
        self.config.add_profile(name, "latest-release", "latest")
    
    def open_profile_dialog(self, _):
        def on_accept(button, dialog):
            self.add_profile(entry.get_text().strip())
            dialog.close()

        dialog = Adw.Dialog.new()
        dialog.set_title("Add new profile")

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        header = Adw.HeaderBar.new()
        header.set_show_end_title_buttons(False)
        root.append(header)

        cancel = Gtk.Button(label="Cancel")

        cancel.connect("clicked", lambda _: dialog.close())

        accept = Gtk.Button(label="Add", css_classes=["suggested-action"])
        accept.set_size_request(80, -1)

        accept.connect("clicked", on_accept, dialog)

        header.pack_start(cancel)
        header.pack_end(accept)

        clamp = Adw.Clamp.new()

        content = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, css_classes=["boxed-list"])

        set_margins(content, [10])

        entry = Adw.EntryRow(title="Profile name")

        content.append(entry)

        clamp.set_child(content)

        root.append(clamp)

        dialog.set_child(root)

        dialog.present(self.window)
    
    def clear_listbox(self, listbox: Gtk.ListBox):
        child = listbox.get_first_child()
        while child is not None:
            listbox.remove(child)
            child = listbox.get_first_child()
    
    def populate_listbox(self, listbox: Gtk.ListBox):
        self.clear_listbox(listbox)

        profiles = list(map(lambda x: ProfileWidget(self, x), self.config.get_profiles_key_names()))
        for x in profiles:
            listbox.append(x.widget)

    def create_profiles_page(self):
        scroll = Gtk.ScrolledWindow()

        clamp = Adw.Clamp(child=scroll)

        content = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE, valign=Gtk.Align.START, css_classes=["boxed-list"])

        scroll.set_child(content)
        self.populate_listbox(content)
        
        self.config.connect("changed", lambda *_: self.populate_listbox(content))
        
        self.stack.add_titled_with_icon(clamp, "profiles-page", "Profiles", "preferences-other-symbolic")