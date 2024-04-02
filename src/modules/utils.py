from gi.repository import Gtk
import requests
import markdown

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

def parse_markdown(text: str):
    for x in text.splitlines():
        if x.startswith("#"):
             