from gi.repository import Adw, Gtk
from modules.utils import NavContent

import traceback

class LogView(Gtk.Frame):
    def __init__(self):
        super().__init__()

        self.scroll = Gtk.ScrolledWindow()

        self.set_margin_bottom(10)
        self.set_margin_top(10)

        self.view = Gtk.TextView(bottom_margin=10, left_margin=10, right_margin=10, top_margin=10, editable=False, monospace=True)
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
        
        stack = traceback.extract_stack()[-2]
        print(stack.filename, stack.lineno)

        self.nav_stack = window.nav_stack
        self.navigation = window.navigation

        page, _, toolbar = self.create_page("Logs", "logs-page", add_box=False)

        content = Adw.Clamp.new()

        self.logs = LogView()

        content.set_child(self.logs)

        toolbar.set_content(content)

        # self.navigation.add(page)
        # self.nav_stack.append(page)

        print([x.get_tag() for x in self.nav_stack])