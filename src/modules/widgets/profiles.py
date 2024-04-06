from gi.repository import Adw, Gtk, Gio

from modules.config import LauncherConfig, parse_icon, format_icon
from modules.variables import DEFAULT_PROFILE_PAGE_CHILD_ICON
from modules.utils import NavContent, set_margins
from modules.types import ProfileType

class ProfileWidget(Gtk.ToggleButton):
    def __init__(self, config: LauncherConfig, profile_name: str):
        self.profile_config = config.get_profile(profile_name)
        
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.icon = Gtk.Picture()
        self.__update_icon()
        self.icon.set_content_fit(Gtk.ContentFit.COVER)

        config.connect("changed", self.__update_icon)

        content.append(self.icon)

        text_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 3)
        title = Gtk.Label(label=self.profile_config["name"], css_classes=["title-3"])
        subtitle = Gtk.Label(label=f"Version: {self.profile_config["lastVersionId"]}", css_classes=["body", "dim-label"])
        
        text_box.append(title)
        text_box.append(subtitle)        

        content.append(text_box)
        set_margins(content, [10])

        super().__init__(child=content)
    
    def __update_icon(self, *_):
        image = parse_icon(self.profile_config["icon"]) or ""
        if image is not None:
            self.icon.set_pixbuf(image)
        else:
            self.icon.set_filename("")

class ProfilesPage(NavContent):
    def __init__(self, nav_stack: list[Gtk.Widget], navigation_view: Adw.NavigationView, config: LauncherConfig):
        super().__init__()
        self.nav_stack = nav_stack
        self.navigation = navigation_view
        self.config = config
    
    def show_profiles_page(self):
        page, content, _ = self.create_page("Profiles", "profiles-page")
        if page is None:
            self.navigation.push_by_tag("profiles-page")
            return

        profiles = list(map(lambda x: ProfileWidget(self.config, x), self.config.get_profiles_names()))
        for x in profiles:
            content.append(x)
            