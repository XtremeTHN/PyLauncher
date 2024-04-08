from gi.repository import Adw, Gtk, Gio, GLib

from modules.config import LauncherConfig, parse_icon, FormatIconFile
from modules.variables import DEFAULT_JVM_FLAGS, MINECRAFT_DIR, JAVA_PATH, \
                                DEFAULT_MINECRAFT_WINDOW_WIDTH, DEFAULT_MINECRAFT_WINDOW_HEIGHT
from modules.utils import NavContent, set_margins, pixbuf_from_bytes
from modules.types import ProfileType

class ProfileConfig:
    def __init__(self, profile_widget):
        self.profile_conf: ProfileType = profile_widget.profile_config
        self.config: LauncherConfig = profile_widget.config
        self.window: Adw.ApplicationWindow = profile_widget.window

        self.widget = Adw.NavigationPage(title="Profile config")
        toolbar = Adw.ToolbarView.new()
        
        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        scroll = Gtk.ScrolledWindow()
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scroll.set_child(content)
        set_margins(content, [10])
        
        group = Adw.PreferencesGroup(title=f"Configuration of {self.profile_conf['name']}", description="Configure the profile settings")
        
        self.name_row = Adw.EntryRow(title="Profile name (Required)", text=self.profile_conf["name"])
        group.add(self.name_row)

        self.icon_row = Adw.ActionRow(title="Profile icon", subtitle=f"Click this to choose the profile icon", activatable=True)
        self.icon = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True, css_classes=["card"])
        set_margins(self.icon, [5, 0, 5, 0])
        if (n:=parse_icon(self.profile_conf.get("icon", ""))) is not None:
            self.icon.set_pixbuf(n)
        
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

        self.java_path = Adw.EntryRow(title="Java path", text=self.profile_conf.get("javaDir", JAVA_PATH))
        java_settings.add(self.java_path)

        self.java_args = Adw.EntryRow(title="JVM Flags", text=self.profile_conf.get("javaArgs", DEFAULT_JVM_FLAGS))
        java_settings.add(self.java_args)

        content.append(java_settings)

        apply_button = Gtk.Button.new()
        apply_button_content = Adw.ButtonContent(icon_name="emblem-ok-symbolic", label="Apply")
        apply_button.set_child(apply_button_content)
        set_margins(apply_button, [10])
        
        apply_button.connect("clicked", self.__apply_all)

        # self.name_row.bind_property("text-lenght", apply_button, "sensitive", transform_from=lambda *_: len(self.name_row.get_text()) > 0)
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

        self.config.save()
    
    def __choose_icon(self, row):
        dialog = Gtk.FileDialog(accept_label="Open")
        dialog.open(self.window, None, callback=self.__file_dial_cb)

    def __file_dial_cb(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult):
        file = dialog.open_finish(result)

        if file is not None:
            content = file.load_contents(None)[1]
            icon = FormatIconFile.from_bytes(content)
            pixbuf = pixbuf_from_bytes(content)
            print(icon)
            self.profile_conf["icon"] = icon.decode()
            self.icon.set_pixbuf(pixbuf)
            
class ProfileWidget(Gtk.Button):
    def __init__(self, profile_page_widget, profile_name: str):
        self.config: LauncherConfig = profile_page_widget.config
        self.nav_stack: list[Gtk.Widget] = profile_page_widget.nav_stack
        self.navigation: Adw.NavigationView = profile_page_widget.navigation

        self.window = profile_page_widget.window
        
        self.profile_config = self.config.get_profile(profile_name)
        
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.icon = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, css_classes=["card"])
        self.__update_icon()

        content.append(self.icon)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3, hexpand=True)
        self.title = Gtk.Label(css_classes=["title-4"], xalign=0)
        self.__update_title()
        
        self.subtitle = Gtk.Label(xalign=0, css_classes=["body", "dim-label"])
        self.__update_subtitle()
        
        text_box.append(self.title)
        text_box.append(self.subtitle)        

        content.append(text_box)
        set_margins(content, [10])

        next_icon = Gtk.Image.new_from_icon_name("go-next-symbolic")
        next_icon.set_halign(Gtk.Align.END)
        content.append(next_icon)
                
        self.config.connect("changed", self.__update)
        super().__init__(child=content)
        
    def __update(self, *_):
        self.__update_icon()
        self.__update_title()
        self.__update_subtitle()
    
    def __update_icon(self):
        image = parse_icon(self.profile_config.get("icon",""))
        if image is not None:
            self.icon.set_visible(True)
            self.icon.set_pixbuf(image)
        else:
            self.icon.set_visible(False)
            self.icon.set_filename("")

    def __update_title(self):
        self.title.set_label(f'{self.profile_config["name"].strip()} {"(Active)" if self.config.get_selected_profile()["name"] == self.profile_config["name"] else ""}')
    
    def __update_subtitle(self):
        self.subtitle.set_label(f'Version: {self.profile_config.get("lastVersionId","latest")}')
    
    def do_clicked(self) -> None:
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
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, valign=Gtk.Align.START)
        set_margins(content, [10])

        profiles = list(map(lambda x: ProfileWidget(self, x), self.config.get_profiles_names()))
        for x in profiles:
            content.append(x)
        
        self.stack.add_titled_with_icon(content, "profiles-page", "Profiles", "preferences-other-symbolic")