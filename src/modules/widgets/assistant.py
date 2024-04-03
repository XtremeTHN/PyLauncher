from gi.repository import Gtk, Adw, GObject
from modules.variables import MINECRAFT_DIR
from modules.utils import NavContent
from modules.config import LauncherConfig

class AssistantPage(NavContent):
    def __init__(self, nav_stack, navigation_view, main_page_func):
        self.nav_stack = nav_stack
        self.navigation = navigation_view
        self.show_main_page = main_page_func
        super().__init__()
    # Step 1
    def show_first_launch(self):
        page, fl_box, _ = self.create_page("PyLauncher", "first-launch", add_to_nav=False)
        status = Adw.StatusPage(icon_name="minecraft", title="PyLauncher", vexpand=True, description="Welcome to PyLauncher, a Minecraft launcher written in Python!")

        gs_button = Gtk.Button.new_with_label("Continue")
        gs_button.set_halign(Gtk.Align.CENTER)
        gs_button.set_css_classes(["pill", "suggested-action"])

        gs_button.connect('clicked', self.create_minecraft_root, page)

        status.set_child(gs_button)

        fl_box.append(status)

        self.navigation.push(page)

    # Step 2
    def create_minecraft_root(self, _, page):
        MINECRAFT_DIR.mkdir(parents=True, exist_ok=True)
        self.show_user_creation_page()

    # Step 3
    def show_user_creation_page(self):
        self.config = LauncherConfig()

        page, content, _ = self.create_page("User Creation", "user-creation-page")
        content.set_valign(Gtk.Align.CENTER)
        content.set_halign(Gtk.Align.CENTER)

        title = Gtk.Label(label="Type a username", css_classes=["title-2"], halign=Gtk.Align.START)
        entry = Gtk.Entry(placeholder_text="Username")
        accept = Gtk.Button(label="Continue", css_classes=["pill", "suggested-action"])
        accept.bind_property("sensitive", entry, "text", flags=GObject.BindingFlags, transform_to=lambda *_: len(entry.get_text()) > 0)

        accept.connect('clicked', self.create_user, entry, page)

        content.append(title)
        content.append(entry)
        content.append(accept)

        self.navigation.push(page)
    
    # Step 4
    def create_user(self, _, entry, page):
        username = entry.get_text()
        print(username)
        user_id = self.config.add_user(username)
        self.config.set_selected_user(user_id)
        self.config.save()
        self.show_main_page()
