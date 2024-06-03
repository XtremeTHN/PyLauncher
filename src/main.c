#include <gtk/gtk.h>
#include <libadwaita-1/adw-application.h>
#include <libadwaita-1/adw-application-window.h>
#include <gio/gfile.h>
#include <gio/gresource.h>


G_DECLARE_FINAL_TYPE(PyLauncherUI, pylauncher_ui, PYLAUNCHER, UI, GtkWidget);

struct _PyLauncherUI {
    AdwApplicationWindow parent;
};

G_DEFINE_TYPE(PyLauncherUI, pylauncher_ui, GTK_TYPE_WINDOW);


static void pylauncher_ui_dispose(GObject *gobject) {
    gtk_widget_dispose_template(GTK_WIDGET (gobject), PYLAUNCHER_TYPE_UI);
}

static void pylauncher_ui_class_init(PyLauncherUIClass *klass) {
    GtkWidgetClass *widget_class = GTK_WINDOW_CLASS (klass);
    
    gtk_widget_class_set_template_from_resource(widget_class, "/com/github/XtremeTHN/PyLauncher/ui.xml");
}

static void pylauncher_ui_init(PyLauncherUI *self) {
    gtk_widget_init_template(GTK_WIDGET (self));

    gtk_window_present(GTK_WIDGET (self->parent));
}

int main(int argc, char **argv[]) {
    AdwApplication *app = adw_application_new("com.github.XtremeTHN.PyLauncher", G_APPLICATION_FLAGS_NONE);

    GError *err;
    GResource *res = g_resource_load("com.github.XtremeTHN.PyLauncher", &err);
    g_resources_register(res);
    
    return g_application_run(G_APPLICATION(app), argc, argv);
}