#include <gtk/gtk.h>
#include <resources.h>
//Function to create the gtk window
static void arquimedes ( GtkWidget *button, gpointer data ) {

}

static void basilea ( GtkWidget *button, gpointer data ) {

}

static void newton ( GtkWidget *button, gpointer data ) {

}

static void activate(GtkApplication *app, gpointer user_data) {
    
    GResource *res = resources_get_resource(); //accesing get_resource fun from header
    g_resources_register(res); //registering resource to access its files
    // Creating gtk app
    // Load the UI data into the builder
    GtkCssProvider *css= gtk_css_provider_new(); //initializing
    gtk_css_provider_load_from_resource(css, "/com.github.designsnma/gtk/PI/ui.css");
    /* select builder widgets with */
    gtk_style_context_add_provider_for_display(gdk_display_get_default(), GTK_STYLE_PROVIDER(css), GTK_STYLE_PROVIDER_PRIORITY_USER); //set css as default style for display

    GtkBuilder *builder = gtk_builder_new();
    gtk_builder_add_from_resource(builder, "/com.github.designsnma/gtk/PI/main.ui", NULL);
    
    GObject *window = gtk_builder_get_object( builder , "window");
    gtk_window_set_application(GTK_WINDOW(window), app);

    GObject *button = gtk_builder_get_object( builder, "button1");
    g_signal_connect_swapped (button, "clicked", G_CALLBACK (arquimedes), NULL);

    button = gtk_builder_get_object( builder, "button2");
    g_signal_connect_swapped (button, "clicked", G_CALLBACK (basilea), NULL);

    button = gtk_builder_get_object( builder, "button3");
    g_signal_connect_swapped (button, "clicked", G_CALLBACK(newton), NULL );

    button = gtk_builder_get_object (builder, "button4");
    g_signal_connect_swapped (button, "clicked", G_CALLBACK ( gtk_window_close), window);

    gtk_widget_set_visible (GTK_WIDGET (window), TRUE);
    
    /* We do not need the builder any more */
    g_object_unref (builder);
}

int main (int    argc, char **argv)
{
  #ifdef GTK_SRCDIR
  g_chdir (GTK_SRCDIR); //cheking source dir
  #endif
  GtkApplication *app; //Pointer to gtk application object
  int status; //Status
  app = gtk_application_new ("com.github.designsnma.gtk.PI", G_APPLICATION_DEFAULT_FLAGS); //Instantiating GtkApplication class, ( name, flags)
  //   Instance | SignalName | Function pointer to G_Callback | Data of c_handler calls
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL); /*the activate signal is connected to the activate() function above the main() function. The activate signal will be sent when your application is launched with g_application_run() on the line below. The g_application_run() also takes as arguments the pointers to the command line arguments counter and string array; this allows GTK to parse specific command line arguments that control the behavior of GTK itself. The parsed arguments will be removed from the array, leaving the unrecognized ones for your application to parse.*/
  status = g_application_run (G_APPLICATION (app), argc, argv); //The activate signal is sent when g_application_run is executed, a window is generated and returns a status
  /*When the window is closed, (f.e by pressing X) a status code is saved in 'status' inside
  the main loop*/
  g_object_unref (app); //Freeing memory of our app object

  return status;
}