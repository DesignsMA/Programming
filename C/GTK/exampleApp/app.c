#include <gtk/gtk.h>
#include "exampleapp.h"

struct _ExampleApp
{
  GtkApplication parent;
};

G_DEFINE_TYPE(ExampleApp, example_app, GTK_TYPE_APPLICATION);

int main ( int argc, char *argv[] ) {
    return g_application_run( G_APPLICATION( example_appp_new() ), argc, argv); //running app class instance
}