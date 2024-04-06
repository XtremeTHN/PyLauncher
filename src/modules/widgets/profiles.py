from gi.repository import Adw, Gtk, Gio

from modules.config import LauncherConfig
from modules.utils import NavContent
from modules.types import ProfileType

class ProfileWidget(Gtk.ToggleButton):
    def __init__(self, profile_config: ProfileType):
        self.profile_config = profile_config
        
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        if Gtk.IconTheme.new().has_icon(profile_config["icon"]) is True:
            icon = Gtk.Image.new_from_icon_name(profile_config["icon"], Gtk.IconSize.LARGE)
        else:
            icon = Gtk.Picture.new_for_filename(profile_config["icon"])
            icon.set_content_fit(Gtk.ContentFit.COVER)
            
        
        content.append(icon)

        super().__init__()

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

        