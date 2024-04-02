from gi.repository import Gtk

from modules.variables import MINECRAFT_DIR
from minecraft_launcher_lib.utils import get_available_versions, get_installed_versions

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