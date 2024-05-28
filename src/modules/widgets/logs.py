from gi.repository import Adw, Gtk
from modules.utils import NavContent, set_margins


class LogView(Gtk.Frame):
    def __init__(self):
        super().__init__()

        self.scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER)

        self.set_margin_bottom(10)
        self.set_margin_top(10)

        self.view = Gtk.TextView(bottom_margin=10, left_margin=10, right_margin=10, 
                                 top_margin=10, editable=False, monospace=True,
                                 wrap_mode=Gtk.WrapMode.CHAR)
        self.scroll.set_child(self.view)

        self.vadjustment = self.view.get_vadjustment()

        self.buffer = self.view.get_buffer()

        self.set_child(self.scroll)
    
    def clear(self):
        self.buffer.set_text("")
    
    def write(self, text):
        self.buffer.insert_at_cursor(text)
        self.vadjustment.set_value(self.vadjustment.get_upper())

class LogsPage(NavContent):
    def __init__(self, window):
        super().__init__()
        
        self.nav_stack = window.nav_stack
        self.navigation = window.navigation

        page, _, toolbar = self.create_page("Logs", "logs-page", add_box=False)
        
        self.logs = LogView()
        
        set_margins(self.logs, [10])

        toolbar.set_content(self.logs)
