#include <gtk/gtk.h>
/*Stores the drawing made by the user*/
static cairo_surface_t *surface = NULL; //Pointer to cairo surface https://www.cairographics.org/manual/cairo-cairo-surface-t.html

static double start_x;
static double start_y;

static void
clear_surface (void)
{
  cairo_t *cr;

  cr = cairo_create (surface);

  cairo_set_source_rgb (cr, 1, 1, 1);
  cairo_paint (cr);

  cairo_destroy (cr);
}

/* Create a new surface of the appropriate size to store our scribbles */
static void
resize_cb (GtkWidget *widget,
           int        width,
           int        height,
           gpointer   data)
{
  if (surface)
    {
      cairo_surface_destroy (surface);
      surface = NULL;
    }

  if (gtk_native_get_surface (gtk_widget_get_native (widget)))
    {
      surface = gdk_surface_create_similar_surface (gtk_native_get_surface (gtk_widget_get_native (widget)),
                                                    CAIRO_CONTENT_COLOR,
                                                    gtk_widget_get_width (widget),
                                                    gtk_widget_get_height (widget));

      /* Initialize the surface to white */
      clear_surface ();
    }
}


/* Draw a rectangle on the surface at the given position */
/* Redraw the screen from the surface. Note that the draw
 * callback receives a ready-to-be-used cairo_t that is already
 * clipped to only draw the exposed areas of the widget
 */
static void
draw_cb (GtkDrawingArea *drawing_area,
         cairo_t        *cr,
         int             width,
         int             height,
         gpointer        data)
{
  cairo_set_source_surface (cr, surface, 0, 0); //
  cairo_paint (cr); //painting func
}

static void
draw_brush (GtkWidget *widget,
            double     x,
            double     y)
{
    /*A #cairo_t contains the current state of the rendering device,
including coordinates of yet to be drawn shapes.

Cairo contexts, as #cairo_t objects are named, are central to
cairo and all drawing with cairo is always done to a #cairo_t
object.

Memory management of #cairo_t is done with
cairo_reference() and cairo_destroy().*/
  cairo_t *cr;

  /* Paint to the surface, where we store our state */
  cr = cairo_create (surface);

  cairo_rectangle (cr, x - 3, y - 3, 6, 6); //saving coordinates of a rectangle, substract -3 to position it on the center
  cairo_fill (cr); //fill rectangle

  cairo_destroy (cr); //destroy saved state

  /* Now invalidate the drawing area. */
  gtk_widget_queue_draw (widget);
}

static void
drag_begin (GtkGestureDrag *gesture,
            double          x,
            double          y,
            GtkWidget      *area)
{
    start_x = x;
    start_y = y;

    draw_brush (area, x, y); //draw on given area at given point
}

static void
drag_update (GtkGestureDrag *gesture,
             double          x,
             double          y,
             GtkWidget      *area)
{
    draw_brush (area, start_x + x, start_y + y); // draw on drag trail
}

static void
drag_end (GtkGestureDrag *gesture,
          double          x,
          double          y,
          GtkWidget      *area)
{
  draw_brush (area, start_x + x, start_y + y); //draw final point
}

static void pressed (GtkGestureClick *gesture,
         int              n_press,
         double           x,
         double           y,
         GtkWidget       *area)
{
    clear_surface();
    gtk_widget_queue_draw( area ); //redraw area after cleaning surface at given point
}

static void close_window ( void ) {
    if ( surface ) //If surface cointains something
        cairo_surface_destroy( surface );
}

static void activate ( GtkApplication *app, gpointer *user_data) {
    GtkWidget *window;
    GtkWidget *frame;
    GtkWidget *drawing_area;
    GtkGesture *drag;
    GtkGesture *press;

    window = gtk_application_window_new( app );
    gtk_window_set_title( GTK_WINDOW( window), "GTK Paint");
    g_signal_connect( window, "clear", G_CALLBACK( close_window ), NULL);

    frame = gtk_frame_new( NULL );
    gtk_window_set_child(GTK_WINDOW (window), frame);

    drawing_area = gtk_drawing_area_new();
    gtk_widget_set_size_request( drawing_area, 640, 360 ); //setting size

    gtk_frame_set_child( GTK_FRAME(frame), drawing_area);
    gtk_drawing_area_set_draw_func( GTK_DRAWING_AREA( drawing_area ), draw_cb, NULL, NULL);

    g_signal_connect_after( drawing_area, "resize", G_CALLBACK ( resize_cb ), NULL);

    drag = gtk_gesture_drag_new(); //In single gesture drag, set left mouse as button
    gtk_gesture_single_set_button (GTK_GESTURE_SINGLE (drag), GDK_BUTTON_PRIMARY);
    gtk_widget_add_controller (drawing_area, GTK_EVENT_CONTROLLER (drag)); // adds an event controller
    g_signal_connect (drag, "drag-begin", G_CALLBACK (drag_begin), drawing_area);
    g_signal_connect (drag, "drag-update", G_CALLBACK (drag_update), drawing_area);
    g_signal_connect (drag, "drag-end", G_CALLBACK (drag_end), drawing_area);

    press = gtk_gesture_click_new();
    gtk_gesture_single_set_button (GTK_GESTURE_SINGLE (press), GDK_BUTTON_SECONDARY); //In a single gesture, set right mouse as button
    gtk_widget_add_controller( drawing_area, GTK_EVENT_CONTROLLER( press ));
     
    g_signal_connect (press, "pressed", G_CALLBACK (pressed), drawing_area);

    gtk_window_present( GTK_WINDOW(window) );

}

int main (int    argc, char **argv) {
    GtkApplication *app = gtk_application_new("com.github.designsnma.gtk.paint", G_APPLICATION_DEFAULT_FLAGS);
    int status;
    g_signal_connect(app, "activate", G_CALLBACK (activate), NULL);
    status = g_application_run( G_APPLICATION(app), argc, argv); //running app
    g_object_unref(app); //freeing memory
    return status;

}