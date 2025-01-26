#include <stdio.h>
#define MAX 100

// Estructura para representar un nodo
typedef struct Nodo {
    int dato;
    int sig; // Índice del siguiente nodo en el arreglo
} Nodo;

// Arreglo estático para la lista
Nodo lista[MAX];
int cabeza = -1; // Índice del primer nodo (-1 indica lista vacía)
int libre = 0;   // Índice del primer nodo disponible

// Función para inicializar la lista estática
void inicializarLista() {
    for (int i = 0; i < MAX - 1; i++) {
        lista[i].sig = i + 1; // Apunta al siguiente índice disponible
    }
    lista[MAX - 1].sig = -1; // Último nodo no tiene siguiente
}

// Función para insertar un nodo al inicio
void insertaInicio(int valor) {
    if (libre == -1) {
        printf("Error: No hay espacio disponible en la lista.\n");
        return;
    }

    int nuevo = libre;       // Toma el índice del nodo libre
    libre = lista[libre].sig; // Actualiza el índice libre al siguiente

    // Asigna el valor al nuevo nodo y lo enlaza al inicio de la lista
    lista[nuevo].dato = valor;
    lista[nuevo].sig = cabeza;

    // El nuevo nodo será la nueva cabeza de la lista
    cabeza = nuevo;
}

// Función para insertar un nodo en una posición específica
void insertaMedio(int valor, int pos) {
    if (libre == -1) {
        printf("Error: No hay espacio disponible en la lista.\n");
        return;
    }

    // Verificar si la posición es válida
    if (pos < 0) {
        printf("Error: La posición no es válida.\n");
        return;
    }

    // Tomar un nodo libre
    int nuevo = libre;       // Toma el índice del nodo libre
    libre = lista[libre].sig; // Actualiza el índice libre al siguiente

    // Asignar el valor al nuevo nodo
    lista[nuevo].dato = valor;

    // Caso especial: insertar al inicio (pos == 0)
    if (pos == 0) {
        lista[nuevo].sig = cabeza; // El nuevo nodo apunta a la cabeza actual
        cabeza = nuevo;            // La nueva cabeza es el nuevo nodo
        return;
    }

    // Insertar el nuevo nodo en la posición `pos`
    lista[nuevo].sig = lista[pos].sig;
    lista[pos].sig = nuevo;
}

// Función para insertar un nodo al final
void insertaFinal(int valor) {
    if (libre == -1) {
        printf("Error: No hay espacio disponible en la lista.\n");
        return;
    }

    int nuevo = libre;       // Toma el índice del nodo libre
    libre = lista[libre].sig; // Actualiza el índice libre al siguiente

    // Asignar el valor al nuevo nodo
    lista[nuevo].dato = valor;
    lista[nuevo].sig = -1; // Este nodo será el último

    if (cabeza == -1) {
        // Si la lista está vacía, el nuevo nodo será la cabeza
        cabeza = nuevo;
    } else {
        // Recorrer la lista para encontrar el último nodo
        int actual = cabeza;
        while (lista[actual].sig != -1) {
            actual = lista[actual].sig;
        }
        lista[actual].sig = nuevo; // Enlaza el nuevo nodo al final
    }
}

// Función para borrar el nodo final
int borrarFinal() {
    if (cabeza == -1) {
        printf("Error: La lista está vacía.\n");
        return -1;
    }

    int actual = cabeza;

    // Si solo hay un nodo
    if (lista[actual].sig == -1) {
        int datoEliminado = lista[actual].dato;
        cabeza = -1; // La lista queda vacía
        return datoEliminado;
    }

    // Recorrer hasta el penúltimo nodo
    while (lista[lista[actual].sig].sig != -1) {
        actual = lista[actual].sig;
    }

    // Eliminar el último nodo
    int datoEliminado = lista[lista[actual].sig].dato; // Dato del último nodo
    lista[actual].sig = -1; // Actualiza el penúltimo nodo para que sea el último
    return datoEliminado;
}

// Función para buscar un elemento en la lista
int buscarElemento(int valorBuscado) {
    int actual = cabeza;
    while (actual != -1) {
        if (lista[actual].dato == valorBuscado) {
            return actual; // Retorna el índice del nodo encontrado
        }
        actual = lista[actual].sig;
    }
    return -1; // Retorna -1 si no encuentra el valor
}

// Función para borrar el nodo al inicio
void borraInicio() {
    if (cabeza == -1) {
        printf("Error: La lista ya está vacía.\n");
        return;
    }

    int nodoEliminado = cabeza;
    cabeza = lista[cabeza].sig; // Actualiza la cabeza al siguiente nodo
    lista[nodoEliminado].sig = libre; // Libera el nodo eliminado
    libre = nodoEliminado;
}

// Función para borrar un nodo en una posición específica
void borraMedio(int pos) {
    if (cabeza == -1) {
        printf("Error: La lista está vacía.\n");
        return;
    }

    // Verificar si la posición es válida
    if (pos < 0 || pos > MAX - 1) {
        printf("Error: La posición no es válida.\n");
        return;
    }

    int anterior = cabeza;
    int actual = cabeza;

    // Recorrer la lista hasta encontrar el nodo en la posición `pos`
    while (actual != pos) {
        anterior = actual;
        actual = lista[actual].sig;
    }

    // Caso especial: borrar el primer nodo
    if (pos == cabeza) {
        borraInicio();
        return;
    }

    // Caso especial: borrar el último nodo
    if (lista[actual].sig == -1) {
        borrarFinal();
        return;
    }

    // Eliminar el nodo en la posición `pos`
    lista[anterior].sig = lista[actual].sig;
    lista[actual].sig = libre; // Libera el nodo eliminado
    libre = actual;
}

// Función para imprimir la lista
void imprimirLista() {
    int actual = cabeza;
    while (actual != -1) {
        printf("%d -> ", lista[actual].dato);
        actual = lista[actual].sig;
    }
    printf("NULL\n");
}

// Función principal
int main() {
    inicializarLista(); // Inicializa la lista estática

    insertaMedio(700, 0);
    insertaFinal(5);
    insertaFinal(10);
    insertaFinal(15);
    insertaInicio(69);

    printf("Lista después de las inserciones: ");
    imprimirLista();

    int valorABuscar = 10;
    int encontrado = buscarElemento(valorABuscar);
    if (encontrado != -1) {
        printf("Elemento %d encontrado en el nodo %d.\n", valorABuscar, encontrado);
    } else {
        printf("Elemento %d no encontrado en la lista.\n", valorABuscar);
    }

    int eliminado = borrarFinal();
    if (eliminado != -1) {
        printf("Nodo eliminado con valor: %d\n", eliminado);
    }

    printf("Lista después de eliminar el nodo final: ");
    imprimirLista();

    printf("Lista después de insertar al inicio: ");
    insertaInicio(69);
    imprimirLista();

    insertaFinal(70);
    imprimirLista();

    insertaMedio(71, buscarElemento(70));
    imprimirLista();

    insertaMedio(72, buscarElemento(69));
    imprimirLista();

    insertaMedio(72, buscarElemento(5));
    imprimirLista();

    borraInicio();
    imprimirLista();

    insertaInicio(728);
    imprimirLista();

    borraMedio(buscarElemento(728));
    imprimirLista();

    borraMedio(buscarElemento(71));
    imprimirLista();

    borraMedio(buscarElemento(5));
    imprimirLista();

    insertaMedio(111, buscarElemento(10));
    imprimirLista();

    return 0;
}