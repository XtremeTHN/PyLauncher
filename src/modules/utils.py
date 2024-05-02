from gi.repository import Gtk, GLib, Adw

from modules.variables import MINECRAFT_DIR
from modules.types import User
from minecraft_launcher_lib.utils import get_available_versions

def set_margins(widget: Gtk.Widget, margins: list[int]):
    """
        Reminder: margins = [top, right, bottom, left]
    """
    length = len(margins)
    
    top = margins[0]
    right = margins[1] if length > 1 else top
    bottom = margins[2] if length > 2 else right
    left = margins[3] if length > 3 else bottom

    widget.set_margin_top(top)
    widget.set_margin_end(right)
    widget.set_margin_bottom(bottom)
    widget.set_margin_start(left)

class Versions(dict):
    def __init__(self, versions):
        super().__init__(versions)

    def join(self):
        result = []
        for value in self:
            for y in self[value]:
                result.append(y)
                
        # Que dolor de cabeza
        return [f"{x['type']} {x['id']}" for x in sorted(result, key=lambda x: x["releaseTime"], reverse=True)]

def get_minecraft_versions():
    versions = {"release": [], "snapshot": [], "beta": [], "alpha": []}
    for version_dict in get_available_versions(MINECRAFT_DIR):
        if version_dict["type"] == "release":
            versions["release"].append(version_dict)
        if version_dict["type"] == "snapshot":
            versions["snapshot"].append(version_dict)
        if version_dict["type"] == "old_beta":
            versions["beta"].append(version_dict)
        if version_dict["type"] == "old_alpha":
            versions["alpha"].append(version_dict)
        
    return Versions(versions)

def generate_minecraft_options(user_data: User):
    return {
        "username": user_data["displayName"],
        "uuid": user_data["uuid"],
        "token": ""
    }

def idle(func, *args):
    def wrapper(*args):
        func(*args)
        return GLib.SOURCE_REMOVE
    
    GLib.idle_add(wrapper, *args)

class NavContent:
    nav_stack: list
    navigation: Adw.NavigationView
    toast: Adw.ToastOverlay

    def __init__(self):
        ...
    
    def create_page(self, title, tag, spacing=10, add_to_nav=True, header=True, add_box=True):
        if tag in self.nav_stack:
            return None, None, None
        
        page = Adw.NavigationPage(title=title, tag=tag)

        toolbar = Adw.ToolbarView()

        content = None
        if add_box is True:
            content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
            toolbar.set_content(content)

        if header is True:
            header_bar = Adw.HeaderBar.new()
            toolbar.add_top_bar(header_bar)

        page.set_child(toolbar)

        if add_to_nav is True:
            self.navigation.add(page)
            self.nav_stack.append(page)

        return page, content, toolbar

    def remove_page(self, page):
        self.navigation.remove(page)
        for index, x in enumerate(self.nav_stack):
            if x is page:
                self.nav_stack.pop(index)

    def notify(self, message):
        if self.toast is not None:
            toast_child = Adw.Toast.new(message)
            idle(self.toast.add_toast, toast_child)
