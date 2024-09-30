#include <glib.h>
#include <stdio.h>

gboolean timeout_callback(gpointer data) //gets called every 10 ms
{
    static int i = 0;
    
    i++;
    g_print("timeout_callback called %d times\n",i);
    
    if(10 == i)
    {
        g_main_loop_quit((GMainLoop*)data);
        return FALSE;
    }
	
    return TRUE;
}

int main()
{
    GMainLoop *loop = NULL;
    GMainContext *context;
    GSource *source;
    int id;
    /*

Attach the Source: This function associates the GSource (the timeout source) with the specified GMainContext. By attaching it, you're telling the GLib event loop to monitor this source for events.
Event Monitoring: Once attached, the main loop will check the source at regular intervals to see if it should trigger (in this case, if the timeout has elapsed).
Return Value: The function returns an ID that identifies the source within the context. This ID can be used for later operations on the source, like removing it or checking its status.

GMainContext: This is a structure used to manage and dispatch events in a GLib application. It provides a way to handle asynchronous operations and callbacks.
Purpose: The GMainContext allows multiple sources (like timeouts, file descriptors, etc.) to be managed together in a single main loop. It helps in organizing and scheduling when each source should be checked for activity.
Thread Safety: Contexts can be used in multi-threaded applications, allowing different threads to have their own event loops and sources.*/
    //create a new time-out source, triggers every 100000 ms
    source = g_timeout_source_new(10); //

    //create a context
    context = g_main_context_new();//to allow associate new thread

    //attach source to context to check source at regular intervals
    id = g_source_attach(source,context);
 
    //create a main loop with context, false so it doesnt starts
    loop = g_main_loop_new(context,FALSE);
	
    //set the callback for this source or function to be called every timeout, loop is send as data
    g_source_set_callback (source,timeout_callback,loop,NULL);
	
    g_main_loop_run (loop);//run 
    
    g_main_loop_unref (loop);//unreference memory related to loop
     
    return 0;
}