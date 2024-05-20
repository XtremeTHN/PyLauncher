from gi.repository import Adw, Gtk
from modules.utils import NavContent

class LogsPage(NavContent):
    def __init__(self, window):
        super().__init__()

        self.nav_stack = window.nav_stack
        self.navigation = window.navigation

        page = Adw.NavigationPage(title="Logs", tag="logs-page")

        toolbar = Adw.ToolbarView()

        header = Adw.HeaderBar.new()
        toolbar.add_top_bar(header)

        content = Adw.Clamp.new()

        text_view = Gtk.TextView()
        buffer = text_view.get_buffer()
        buffer.set_text("Logs go here")

        content.set_child(text_view)

        page.set_child(toolbar)

        self.navigation.add(page)
        self.nav_stack.append(page)