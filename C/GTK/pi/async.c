#include <glib.h>
#include <gio/gio.h>

typedef struct {
    int result;
    GError *error;
} MyResult;

// This is a synchronous function we want to run asynchronously
int compute_something(int input) {
    g_print("\ncompute something...");
    g_usleep(2000000); // Simulate a time-consuming computation (2 seconds)
    return input * input; // Example computation
}

// This is the function that will be executed asynchronously
static void perform_computation(GTask *task, gpointer source_object, gpointer task_data, GCancellable *cancellable) {
    int input = GPOINTER_TO_INT(task_data);
    MyResult *result = g_new(MyResult, 1);

    // Call the synchronous function
    result->result = compute_something(input);
    result->error = NULL;

    // Return the result to the GTask
    g_task_return_pointer(task, result, (GDestroyNotify)g_free);
}

// This is the callback to handle the result of the GTask
static void on_computation_finished(GObject *source_object, GAsyncResult *res, gpointer user_data) {
    /*g_task_propagate_pointer() is a GLib function that retrieves the result of a GTask once
     it has finished executing. Here's how it works:*/
    MyResult *result = g_task_propagate_pointer(G_TASK(res), NULL);

    if (result->error) {
        g_printerr("Error occurred: %s\n", result->error->message);
        g_clear_error(&result->error);
    } else {
        g_print("Computed result: %d\n", result->result);
    }

    g_free(result);
}

int main() {
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);

    // Create a GTask to perform the computation asynchronously
    GTask *task = g_task_new(NULL, NULL, on_computation_finished, NULL);
    g_task_set_source_tag(task, (gpointer) main);
    g_task_set_task_data(task, GINT_TO_POINTER(8), NULL);
    g_task_run_in_thread(task, perform_computation); // Example input

    g_main_loop_run(loop);

    g_object_unref(task);
    g_main_loop_unref(loop);
    return 0;
}
