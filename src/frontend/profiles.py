from gi.repository import Gtk, Adw
from backend.config import LauncherConfig
from backend.types import Profile

@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/profile-widget.ui")
class ProfileRow(Adw.ActionRow):
    __gtype_name__ = "ProfileWidget"
    def __init__(self, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        
        self.profile = profile
        
        self.__update(None, None)
        
        LauncherConfig.connect("changed", self.__update)
    
    def __update(self, _, __):
        self.props.title = f'{self.profile.get("name")}{" (Active)" if LauncherConfig.get_selected_profile().get("name") \
                                                                    == self.profile.get("name") else ""}'
        
        self.props.subtitle = f'Version: {self.profile.get("lastVersionId")}'