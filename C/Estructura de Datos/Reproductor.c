#include <stdio.h>
#include <stdlib.h>

typedef struct Cola {
    int *canciones;  // Almacena las canciones (usamos enteros para simplificar)
    int frente;      // Índice del frente de la cola
    int final;       // Índice del final de la cola
    char ultimo;     // Indica si la última operación fue inserción ('I') o eliminación ('E')
    int capacidad;   // Capacidad actual de la cola
} Cola;

// Función para comprobar si la asignación de memoria fue exitosa
void comprobar(void *ptr) {
    if (ptr == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
}

// Función para verificar si la cola está vacía
char estaVacia(Cola *queue) {
    return (queue->final % queue->capacidad) == (queue->frente % queue->capacidad) && queue->ultimo == 'E';
}

// Función para verificar si la cola está llena
char estaLlena(Cola *queue) {
    return (queue->final % queue->capacidad) == (queue->frente % queue->capacidad) && queue->ultimo == 'I';
}

// Función para realocar memoria dinámicamente
void realocar(void **ptr, int nsize) {
    int *temp = (int *)realloc(*ptr, nsize * sizeof(int));
    if (temp == NULL) {
        printf("\nError al reservar espacio.\n");
        free(*ptr);  // Liberar la memoria original antes de salir
        exit(EXIT_FAILURE);
    } else {
        *ptr = temp;  // Asignar el nuevo bloque de memoria al apuntador original
    }
}

// Función para inicializar la cola
void inicializar(Cola *queue, int size) {
    queue->canciones = (int *)malloc(sizeof(int) * size);
    comprobar((void *)queue->canciones);
    queue->capacidad = size;
    queue->frente = queue->final = 0;
    queue->ultimo = 'E';
}

// Función para insertar una canción en la cola
void insertar(Cola *queue, int cancion) {
    if (estaLlena(queue)) {
        queue->capacidad *= 2;
        printf("\nLa cola está llena - Aumentando capacidad a %d\n", queue->capacidad);
        realocar((void *)&queue->canciones, queue->capacidad);
    }
    queue->canciones[queue->final % queue->capacidad] = cancion;
    queue->final++;
    queue->ultimo = 'I';
}

// Función para eliminar una canción de la cola
void eliminar(Cola *queue) {
    if (estaVacia(queue)) {
        printf("\nLa cola está vacía.\n");
        if (queue->capacidad > 5) {
            queue->capacidad /= 2;
            realocar((void *)&queue->canciones, queue->capacidad);
        }
        queue->frente = queue->final = 0;
    } else {
        queue->frente++;
        queue->ultimo = 'E';
    }
}

// Función para reproducir la lista de canciones
void reproducir(Cola *queue,char **canciones) {
    if (estaVacia(queue)) {
        printf("\nNo hay canciones en la lista de reproduccion.\n");
        return;
    }

    printf("\nReproduciendo lista de canciones:\n");
    int i = queue->frente;
    while (i != queue->final) {
        int cancion = queue->canciones[i % queue->capacidad];
        if (cancion == -1) {
            printf("Cancion dañada o inexistente - Saltando a la siguiente...\n");
        } else {
            printf("Reproduciendo cancion: %d | %s\n", cancion, canciones[i]);
        }
        i++;
    }
    printf("Fin de la lista de reproduccion.\n");
}

// Función principal
int main() {
    Cola *queue = (Cola *)malloc(sizeof(Cola));
    comprobar(queue);
    inicializar(queue, 5);
    char *canciones[] = {
    "Bohemian Rhapsody",
    "Stairway to Heaven",
    "Hotel California",
    "Imagine",
    "Smells Like Teen Spirit",
    "Like a Rolling Stone",
    "Hey Jude",
    "Purple Haze",
    "Yesterday",
    "Let It Be"
};

    int opc, temp, num_elementos = sizeof(canciones) / sizeof(canciones[0]);;
    do {
        
        printf("\n1. Insertar cancion\n2. Eliminar cancion\n3. Reproducir lista\n4. Lista de canciones\n-1. Salir\n: ");
        scanf("%d", &opc);

        switch (opc) {
            case 1:
                printf("\nIngrese el ID de la cancion: ");
                scanf("%d", &temp);
                if (temp > num_elementos-1 || temp < 0) { 
                    temp = -1;
                }
                insertar(queue, temp);
                break;

            case 2:
                eliminar(queue);
                break;

            case 3:
                reproducir(queue, canciones);
                break;

            case 4:
                for ( int i = 0; i < num_elementos; i++)
                {
                    printf("\nId: %d | %s",i, canciones[i]);
                }
            break;

            case -1:
                printf("\nSaliendo...\n");
                break;

            default:
                printf("\nOpcion no valida.\n");
                break;
        }
    } while (opc != -1);

    free(queue->canciones);  // Liberar memoria ocupada por las canciones
    free(queue);             // Liberar memoria ocupada por la cola

    return 0;
}