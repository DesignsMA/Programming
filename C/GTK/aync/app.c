#include <gtk/gtk.h>
#include <gio/gio.h>
#include <glib.h>
#include <glib-2.0>

void (* GAsyncReadyCallback) ready (
GObject* source_object,
GAsyncResult* res,
gpointer data
) {

}


static void activate (GtkApplication *app, gpointer user_data) {
        GTask *asynctask;
        asynctask = g_task_new(NULL, NULL, ready, NULL);

}


int main ( int argc, char **argv) {
    #ifdef GTK_SRCDIR
    g_chdir (GTK_SRCDIR); //cheking source dir
    #endif
    int status;
    GtkApplication *app = gtk_application_new("com.github.designsnma.gtk.AsyncTest", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    status = g_application_run( app, argc, argv);

    g_object_unref(app);
}
