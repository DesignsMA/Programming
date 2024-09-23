#include <gtk/gtk.h>
#include <gresource.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <malloc.h>
#include<conio.h>
//Function to create the gtk window

typedef struct {
    GtkEntry *input;  // Replace InputType with the actual type of 'input'
    GtkLabel *label;
} CallbackData;

char *arquimedesfunc(long int n) {
    // Allocate memory for the output string
    char *str = malloc(256 * sizeof(char)); // Adjust size as needed
    if (str == NULL) {
        return NULL; // Handle memory allocation failure
    }

    clock_t start, end;
    double cpu_time_used;
    start = clock(); // Start timing

    long double r = 1; // Radius
    long double A = 4 * sqrt(2) * r; // Perimeter of the inscribed polygon
    long double B = 8 * r;
    long double m = 4; // Number of sides of the polygons

    while (m * 2 <= n) { // Loop until the number of sides exceeds n
        B = 2 * A * B / (A + B); // Calculate the perimeters
        A = sqrt(A * B);
        m = m * 2; // Double the number of sides
    }

    long double pi = (A / (2 * r) + B / (2 * r)) / 2; // Calculate π
    long double err = fabsl(A / (2 * r) - B / (2 * r)) / 2; // Calculate error

    end = clock(); // End timing
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    sprintf(str, "Aproximación: %.34Lf\nError: %.34Lf\nTiempo de ejecución: %.34f s", pi, err, cpu_time_used);
    return str; // Return the formatted string
}

// Don't forget to free the allocated memory later

static void arquimedes ( CallbackData *data) {
  //Create a new window
  const char *str = gtk_editable_get_text( GTK_EDITABLE(data->input));
  gtk_label_set_label(data->label, str);
  char *endptr;
  long int num;
   // Convert the string to a long integer
   //string, auxiliar string to compare, base
  num = strtol(str, &endptr, 10);
    if (endptr == str) {
      gtk_label_set_label(data->label, "No es un numero :c");
   } else if (*endptr != '\0') {
      gtk_label_set_label(data->label, "Caracter invalido");
   } else {
    char *result = arquimedesfunc(num);
    gtk_label_set_label(data->label, result);
    free(result);
   }

}

char *basileaSeries(long int n) {
    // Allocate memory for the output string
    char *str = malloc(256 * sizeof(char)); // Adjust size as needed
    if (str == NULL) {
        return NULL; // Handle memory allocation failure
    }

    clock_t start, end;
    double cpu_time_used;
    start = clock(); // Start timing

    long double S=0;  //suma total de los términos y la inicializo a 0.

    for (int i=0; i<n; i++) {  // Bucle, recorre todo los naturales hasta N.
        S=S+ 1/pow(i+1,2);     // En cada vuelta se añade a S el siguiente término.
    }
    
    long double pi=sqrt(6*S);       // Se calcula pi.

    end = clock(); // End timing
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    sprintf(str, "Aproximación: %.34Lf\nTiempo de ejecución: %.34f s", pi, cpu_time_used);
    return str; // Return the formatted string
}

char *newtonSeries(long int n) {
    // Allocate memory for the output string
    char *str = malloc(256 * sizeof(char)); // Adjust size as needed
    if (str == NULL) {
        return NULL; // Handle memory allocation failure
    }

    clock_t start, end;
    double cpu_time_used;
    start = clock(); // Start timing

    long double pi = 0.0;

    // Calculate pi using the arctangent series
    for (long int i = 0; i < n; i++) {
        long double term = (1.0 / (2 * i + 1)) * (i % 2 == 0 ? 1 : -1);
        pi += term;
    }
    pi *= 4; // Multiply by 4 to get pi

    end = clock(); // End timing
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    sprintf(str, "Aproximación: %.34Lf\nTiempo de ejecución: %.34f s", pi, cpu_time_used);
    return str; // Return the formatted string
}

static void basilea ( CallbackData *data ) {

  const char *str = gtk_editable_get_text( GTK_EDITABLE(data->input));
  gtk_label_set_label(data->label, str);
  char *endptr;
  long int num;
   // Convert the string to a long integer
   //string, auxiliar string to compare, base
  num = strtol(str, &endptr, 10);
    if (endptr == str) {
      gtk_label_set_label(data->label, "No es un numero :c");
   } else if (*endptr != '\0') {
      gtk_label_set_label(data->label, "Caracter invalido");
   } else {
    char *result = basileaSeries(num);
    gtk_label_set_label(data->label, result);
    free(result);
   }

}

static void newton ( CallbackData *data ) {
  const char *str = gtk_editable_get_text( GTK_EDITABLE(data->input));
  gtk_label_set_label(data->label, str);
  char *endptr;
  long int num;
   // Convert the string to a long integer
   //string, auxiliar string to compare, base
  num = strtol(str, &endptr, 10);
    if (endptr == str) {
      gtk_label_set_label(data->label, "No es un numero :c");
   } else if (*endptr != '\0') {
      gtk_label_set_label(data->label, "Caracter invalido");
   } else {
    char *result = newtonSeries(num);
    gtk_label_set_label(data->label, result);
    free(result);
   }

}

static void activate(GtkApplication *app, gpointer user_data) {
    
    GResource *res = gresource_get_resource(); //accesing get_resource fun from header
    gresource_register_resource(); //registering resource to access its files
    // Creating gtk app
    // Load the UI data into the builder

    GtkBuilder *builder = gtk_builder_new();
    gtk_builder_add_from_resource(builder, "/com.github.designsnma/gtk/PI/main.ui", NULL);

    GObject *window = gtk_builder_get_object( builder , "window");
    gtk_window_set_application(GTK_WINDOW(window), app);

    GObject *input = gtk_builder_get_object( builder, "input");

    GObject *label = gtk_builder_get_object( builder, "lb1");
    gtk_label_set_label(GTK_LABEL(label), "... Coloque el número de series o polígonos ...");

    CallbackData *data = g_malloc(sizeof(CallbackData));
    data->input = GTK_ENTRY(input);
    data->label = GTK_LABEL(label);

    GObject *bt1 = gtk_builder_get_object( builder, "bt1");
    g_signal_connect_swapped (bt1, "clicked", G_CALLBACK (arquimedes), data);

    GObject*bt2 = gtk_builder_get_object( builder, "bt2");
    g_signal_connect_swapped (bt2, "clicked", G_CALLBACK (basilea), data);

    GObject *bt3 = gtk_builder_get_object( builder, "bt3");
    g_signal_connect_swapped (bt3, "clicked", G_CALLBACK (newton), data);


    gtk_widget_set_visible (GTK_WIDGET (window), TRUE);
    GtkCssProvider *css = gtk_css_provider_new(); //initializing
    gtk_css_provider_load_from_resource(css, "/com.github.designsnma/gtk/PI/ui.css");
    gtk_style_context_add_provider_for_display(gdk_display_get_default(), GTK_STYLE_PROVIDER(css), GTK_STYLE_PROVIDER_PRIORITY_USER); //set css as default style for display

    
    gtk_window_present(GTK_WINDOW(window)); //show the window
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
  gresource_unregister_resource();
  g_resource_unref(gresource_get_resource());
  g_object_unref (app); //Freeing memory of our app object

  return status;
}
 