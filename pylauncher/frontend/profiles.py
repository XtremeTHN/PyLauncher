from gi.repository import Gtk, Adw, GLib
from pylauncher.backend.config import LauncherConfig
from pylauncher.backend.types import Profile

@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/profile-conf-page.ui")
class ProfileConfPage(Adw.NavigationPage):
    __gtype_name__ = "ProfileConfigPage"
    
    apply_btt: Gtk.Button = Gtk.Template.Child()
    rm_btt: Gtk.Button = Gtk.Template.Child()
    
    activated: Adw.SwitchRow = Gtk.Template.Child()
    name_row: Adw.EntryRow = Gtk.Template.Child()
    mine_dir_row: Adw.EntryRow = Gtk.Template.Child()
    width_row: Adw.SpinRow = Gtk.Template.Child()
    height_row: Adw.SpinRow = Gtk.Template.Child()
    snapshots_row: Adw.SwitchRow = Gtk.Template.Child()
    old_betas_row: Adw.SwitchRow = Gtk.Template.Child()
    old_alphas_row: Adw.SwitchRow = Gtk.Template.Child()
    
    java_path_row: Adw.EntryRow = Gtk.Template.Child()
    java_args_row: Adw.EntryRow = Gtk.Template.Child()
    
    def __init__(self, profile: Profile, **kwargs):
        super().__init__(**kwargs)
        self.profile = profile
        
        self.set_title(f'{self.profile.get("name", "Unknown")} Config')
                
        print(self.activated, self.name_row)
        
        self.activated.set_active(LauncherConfig.get_selected_profile().get("name") == profile.get("name"))
        self.name_row.props.text = profile.get('name')
        self.mine_dir_row.props.text = profile.get('gameDir', '')
        self.width_row.props.value = profile.get("resolution").get("width")
        self.height_row.props.value = profile.get("resolution").get("height")
        
        allowed_released_types = profile.get("allowedReleaseTypes", [])

        for allowed in allowed_released_types:
            if allowed == "snapshot":
                self.snapshots_row.props.active = True
            if allowed == "beta":
                self.old_betas_row.props.active = True
            if allowed == "alpha":
                self.old_aplhas_row.props.active = True
        
        self.java_path_row.props.text = profile.get("javaDir", "")
        self.java_args_row.props.text = profile.get("javaArgs", "")

    @Gtk.Template.Callback()
    def on_apply_btt_clicked(self, _):
        ...
        
    @Gtk.Template.Callback()
    def on_rm_btt_clicked(self, _):
        ...

@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/profile-widget.ui")
class ProfileRow(Adw.ActionRow):
    __gtype_name__ = "ProfileWidget"
    def __init__(self, profile: Profile, window, **kwargs):
        super().__init__(**kwargs)
        
        self.nav: Adw.NavigationView = window.nav
                
        self.profile = profile
        self.profile_conf_page = ProfileConfPage(profile)
        
        self.__update(None, None)
        
        LauncherConfig.connect("changed", self.__update)
    
    def __update(self, _, __):
        self.props.title = f'{self.profile.get("name")}{" (Active)" if LauncherConfig.get_selected_profile().get("name") \
                                                                    == self.profile.get("name") else ""}'
        
        self.props.subtitle = f'Version: {self.profile.get("lastVersionId")}'
    
    @Gtk.Template.Callback()
    def on_profile_widget_clicked(self, _):
        print("Ad")
        self.nav.push(self.profile_conf_page)