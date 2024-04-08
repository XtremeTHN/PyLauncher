from gi.repository import Adw, Gtk, Gio

from modules.config import LauncherConfig, parse_icon, format_icon
from modules.variables import DEFAULT_PROFILE_PAGE_CHILD_ICON, MINECRAFT_DIR
from modules.utils import NavContent, set_margins
from modules.types import ProfileType

class ProfileConfig:
    def __init__(self, profile_widget):
        self.profile_conf: ProfileType = profile_widget.profile_config
        self.config: LauncherConfig = profile_widget.config
        
        self.widget = Adw.NavigationPage(title="Profile config")
        toolbar = Adw.ToolbarView.new()
        
        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        set_margins(content, [10])
        
        group = Adw.PreferencesGroup(title=f"Configuration of {self.profile_conf['name']}", description="Configure the profile settings")
        content.append(group)
        
        self.name_row = Adw.EntryRow(title="Profile name", text=self.profile_conf["name"])
        group.add(self.name_row)
        
        self.game_dir = Adw.EntryRow(title="Minecraft directory", text=self.profile_conf.get("gameDir", str(MINECRAFT_DIR)))
        group.add(self.game_dir)
        
        resolution_expand_row = Adw.ExpanderRow.new()
        width = self.profile_conf.get("resolution", {}).get("width", 854)
        height = self.profile_conf.get("resolution", {}).get("height", 480)
        
        self.res_width = Adw.SpinRow(adjustment=Gtk.Adjustment(value=int(width), page_increment=1, step_increment=1), 
                                     title="Width", subtitle="The width of the minecraft window")
        self.res_height = Adw.SpinRow(adjustment=Gtk.Adjustment(value=int(height), page_increment=1, step_increment=1),
                                      title="Height", subtitle="The height of the minecraft window")

        resolution_expand_row.add_row(self.res_width)
        resolution_expand_row.add_row(self.res_height)
        
        group.add(resolution_expand_row)
        
        apply_button = Gtk.Button.new()
        apply_button_content = Adw.ButtonContent(icon_name="emblem-ok-symbolic", label="Apply")
        apply_button.set_child(apply_button_content)
        
        apply_button.connect("clicked", self.__apply_all)
        
        content.append(apply_button)
        
        toolbar.set_content(content)
        
        self.widget.set_child(toolbar)
    
    def __apply_all(self, btt):
        ...
    
    # def update_key(self, key, value):
    #     self.profile_conf[key] = value
    
    # def __update_profile_name(self, new_name):
    #     self.config.remove_profile(self.profile_conf["name"], save=False)
    #     self.config.add_profile_dict(new_name, self.profile_conf)
    
class ProfileWidget(Gtk.Button):
    def __init__(self, profile_page_widget, profile_name: str):
        self.config: LauncherConfig = profile_page_widget.config
        self.nav_stack: list[Gtk.Widget] = profile_page_widget.nav_stack
        self.navigation: Adw.NavigationView = profile_page_widget.navigation
        
        self.profile_config = self.config.get_profile(profile_name)
        
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.icon = Gtk.Picture(content_fit=Gtk.ContentFit.COVER)
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
            self.icon.set_pixbuf(image)
        else:
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
        
        self.stack: Adw.ViewStack = window.stack
    
    def create_profiles_page(self):
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, valign=Gtk.Align.START)
        set_margins(content, [10])

        profiles = list(map(lambda x: ProfileWidget(self, x), self.config.get_profiles_names()))
        for x in profiles:
            content.append(x)
        
        self.stack.add_titled_with_icon(content, "profiles-page", "Profiles", "preferences-other-symbolic")