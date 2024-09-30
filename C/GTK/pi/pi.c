#include <gtk/gtk.h>
#include <gresource.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <malloc.h>
#include <unistd.h> // for usleep()
#include <gmp.h>
//Function to create the gtk window

typedef struct {
    GtkEntry *input;  // Replace InputType with the actual type of 'input'
    GtkLabel *label;
} CallbackData;

typedef struct {
    GtkEntry *input;  // Replace InputType with the actual type of 'input'
    GtkEntry *precision;  // Replace InputType with the actual type of 'input'
    GtkLabel *label;
    GtkButton *bt;
} CallbackDataPrecise;

void f(mpf_t result, const mpf_t x, int precision) {
    mpf_t temp;
    mpf_init2(temp, precision);
    
    // Calculate x^2
    mpf_pow_ui(temp, x, 2);         // temp = x^2
    
    mpf_t one; 
    mpf_init_set_ui(one, 1); // Initialize one to 1
    mpf_sub(temp, one, temp); // temp = 1 - x^2

    // Calculate sqrt(1 - x^2)
    mpf_sqrt(result, temp);        // result = sqrt(1 - x^2)

    // Clear the temporary variable
    mpf_clear(one);
    mpf_clear(temp);
}

char *trapeze(long int n, int precision) {
    mp_exp_t mp_exponent;
    char *str, *mpf_str, c, *substr;
    mpf_t h, sum, result, x1, x2, f_x1, f_x2, a, b;
    clock_t start, end;
    double cpu_time_used;
    int chunk_size = (n < 10000) ? 1 : n / 10000; // Set chunk size

    start = clock();
    mpf_init2(a, precision);
    mpf_init2(b, precision);
    mpf_init2(result, precision);
    mpf_init2(sum, precision);
    mpf_init(h);
    mpf_init(x1);
    mpf_init(x2);
    mpf_init2(f_x1, precision);
    mpf_init2(f_x2, precision);

    // Limits
    mpf_set_si(a, -1);
    mpf_set_si(b, 1);
    // h = (b - a) / n
    mpf_sub(h, b, a);
    mpf_div_ui(h, h, n);
    mpf_set_ui(sum, 0);
    mpf_set_ui(result, 0); // Initialize result

    // Process in chunks
    for (long int i = 0; i < n; i += chunk_size) {
        long int end_chunk = (i + chunk_size < n) ? i + chunk_size : n;
        

        for (int j = i; j < end_chunk; j++) {
            // x1 = a + j*h
            mpf_mul_ui(x1, h, j);
            mpf_add(x1, a, x1);

            // x2 = a + (j + 1) * h
            mpf_mul_ui(x2, h, j + 1);
            mpf_add(x2, a, x2);

            // f(x1) and f(x2)
            f(f_x1, x1, precision);
            f(f_x2, x2, precision);

            // sum = (f(x1) + f(x2)) / 2 * h
            mpf_add(sum, f_x1, f_x2);
            mpf_div_ui(sum, sum, 2);
            mpf_mul(sum, sum, h);

            // Accumulate to result
            mpf_add(result, result, sum);
        }
        usleep(25000);
        g_print(".");


        // Check for user termination or update progress here if needed
        // For example: if (user_wants_to_abort) break;
    }

    mpf_mul_ui(result, result, 2); // multiply by two

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    mpf_str = mpf_get_str(NULL, &mp_exponent, 10, 0, result);
    str = (char *)malloc(strlen(mpf_str) + 50);
    substr = (char *)malloc(strlen(mpf_str));

    if (substr == NULL) {
        free(mpf_str);
        return NULL; // Error handling
    }

    c = mpf_str[0];
    strcpy(substr, (char *)mpf_str + 1);
    snprintf(str, strlen(mpf_str) + 50, "Aproximación: %c.%s\nTiempo de ejecución: %.35fs", c, substr, cpu_time_used);

    // Clear memory
    mpf_clear(h);
    mpf_clear(sum);
    mpf_clear(result);
    mpf_clear(x1);
    mpf_clear(x2);
    mpf_clear(f_x1);
    mpf_clear(f_x2);
    mpf_clear(a);
    mpf_clear(b);
    free(mpf_str);
    free(substr);
    return str; // Return the formatted string
}



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

static void setLabel( CallbackData *data, char*(*funcptr)(long int) ) { // pointer to function with arguments n and return type char *
  const char *str = gtk_editable_get_text( GTK_EDITABLE(data->input));
  char *endptr;
  long int num;
   // Convert the string to a long integer
   //string, auxiliar string to compare, base
  num = strtol(str, &endptr, 10);
    if (endptr == str) {
      gtk_label_set_text(data->label, "No es un numero :c");
   } else if (*endptr != '\0') {
      gtk_label_set_text(data->label, "Caracter invalido");
   } else {
    char *result = (*funcptr)(num);
    gtk_label_set_text(data->label, result);
    free(result);
   }
}

static void arquimedes ( CallbackData *data) {
  setLabel(data, &arquimedesfunc);
}

static void basilea ( CallbackData *data ) {
  setLabel(data, &basileaSeries);
}

static void newton ( CallbackData *data ) {
  setLabel(data, &newtonSeries);
}

static int trapezes ( CallbackDataPrecise *data ) {
  const char *str = gtk_editable_get_text( GTK_EDITABLE(data->input));
  const char *str2 = gtk_editable_get_text( GTK_EDITABLE(data->precision));
  gtk_widget_set_sensitive( GTK_WIDGET(data->bt), FALSE);
  char *endptr;
  long int num = strtol(str, &endptr, 10);

    if (endptr == str) {
        gtk_label_set_text(data->label, "No es un numero :c");
        return 0;
    } 
    if (*endptr != '\0') {
        gtk_label_set_text(data->label, "Caracter invalido");
        return 0;
    }

    int num2 = strtol(str2, &endptr, 10);
    if (endptr == str2 || num2 < 256 || num2%2 != 0) {
        gtk_label_set_text(data->label, "La precisión debe ser mayor a 256 y multiplo de 2");
        return 0;
    }
    if (*endptr != '\0') {
        gtk_label_set_text(data->label, "Caracter invalido");
        return 0;
    }

    if ( num < 1 ) num = 1;
    if ( num2 < 256 ) num = 256;

    char *result = trapeze(num, num2);
    gtk_label_set_text(data->label, result);
    // Use a timer to re-enable the button after 2 seconds
    g_timeout_add(1000, (GSourceFunc)gtk_widget_set_sensitive, data->bt);
    free(result);

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

    GObject *grid = gtk_builder_get_object( builder , "grid");
    gtk_window_set_application(GTK_WINDOW(window), app);

    GObject *input = gtk_builder_get_object( builder, "input");
    gtk_entry_set_placeholder_text( GTK_ENTRY(input), "Particiones, polígonos o series a calcular");

    GObject *label = gtk_builder_get_object( builder, "lb1");

    CallbackData *data = g_malloc(sizeof(CallbackData));
    data->input = GTK_ENTRY(input);
    data->label = GTK_LABEL(label);

    GObject *bt1 = gtk_builder_get_object( builder, "bt1");
    g_signal_connect_swapped (bt1, "clicked", G_CALLBACK (arquimedes), data);

    GObject*bt2 = gtk_builder_get_object( builder, "bt2");
    g_signal_connect_swapped (bt2, "clicked", G_CALLBACK (basilea), data);

    GObject *bt3 = gtk_builder_get_object( builder, "bt3");
    g_signal_connect_swapped (bt3, "clicked", G_CALLBACK (newton), data);

    GObject *precision = gtk_builder_get_object( builder, "input2");
    gtk_widget_set_size_request( GTK_WIDGET(precision), 120, 20);
    gtk_entry_set_placeholder_text( GTK_ENTRY(precision), "Precisión | Trapecios");

    GObject *bt4 = gtk_builder_get_object( builder, "bt4");

    CallbackDataPrecise *data2 = g_malloc(sizeof(CallbackDataPrecise));
    data2->input = GTK_ENTRY(input);
    data2->precision = GTK_ENTRY(precision);
    data2->label = GTK_LABEL(label);
    data2->bt = GTK_BUTTON(bt4);

    g_signal_connect_swapped (bt4, "clicked", G_CALLBACK (trapezes), data2);

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
 