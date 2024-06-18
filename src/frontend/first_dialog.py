from gi.repository import Adw, Gtk

@Gtk.Template(resource_path="/com/github/XtremeTHN/PyLauncherUI/bootstrap-dialog.ui")
class BootstrapDialog(Adw.Dialog):
    __gtype_name__ = "BootstrapDialog"
    bootstrap_dialog_user_status_revealer: Gtk.Revealer = Gtk.Template.Child()
    bootstrap_dialog_user_status_label: Gtk.Label = Gtk.Template.Child()
    user_entry: Gtk.Entry = Gtk.Template.Child()
    
    @Gtk.Template.Callback()
    def on_bootstrap_dialog_user_creation_finished(self, _):
        user = self.user_entry.get_text()
        if user == "":
            self.bootstrap_dialog_user_status_label.set_label("Provide a username please")
            self.bootstrap_dialog_user_status_revealer.set_reveal_child(True)
        else:
            self.force_close()