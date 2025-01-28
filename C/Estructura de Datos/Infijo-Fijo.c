#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>  // Para usar isdigit

typedef struct {
    char *datos;
    int tope;
    int capacidad;
} Pila;

void inicializar(Pila *stack, int capacidad) {
    stack->datos = (char*)malloc(sizeof(char) * capacidad);
    if (stack->datos == NULL) {
        printf("\nError al reservar espacio.\n");
        exit(EXIT_FAILURE);
    }
    stack->tope = -1; // La pila está vacía
    stack->capacidad = capacidad;
}

int estaVacia(Pila *stack) {
    return stack->tope == -1;
}

void realocar(void** ptr, int nsize) {
    char *temp = (char *)realloc(*ptr, nsize * sizeof(char));
    if (temp == NULL) {
        printf("\nError al reservar espacio.\n");
        free(*ptr); // Liberar la memoria original antes de salir
        exit(EXIT_FAILURE);
    } else {
        *ptr = temp; // Asignar el nuevo bloque de memoria al apuntador original
    }
}

void push(Pila *stack, char var) {
    if (stack->tope == (stack->capacidad - 1)) {
        stack->capacidad *= 2;
        realocar((void*)&stack->datos, stack->capacidad);
    }
    stack->datos[++stack->tope] = var;
}

char pop(Pila *stack) {
    if (estaVacia(stack)) {
        printf("La pila se encuentra vacía\n");
        exit(EXIT_FAILURE);
    }
    return stack->datos[stack->tope--];
}

char verTope(Pila *stack) {
    if (estaVacia(stack)) {
        printf("La pila se encuentra vacía\n");
        exit(EXIT_FAILURE);
    }
    return stack->datos[stack->tope];
}

int precedencia(char op) {
    switch (op) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        default:
            return 0;
    }
}

void postfija(char cad[]) {
    int i = 0, u = 0;
    char resultado[100];
    Pila stack;
    inicializar(&stack, 5);

    while (cad[i] != '\0') {
        if (isdigit(cad[i])) {
            resultado[u++] = cad[i];
        } else if (cad[i] == '(') {
            push(&stack, cad[i]);
        } else if (cad[i] == ')') {
            while (!estaVacia(&stack) && verTope(&stack) != '(') {
                resultado[u++] = pop(&stack);
            }
            if (!estaVacia(&stack) && verTope(&stack) == '(') {
                pop(&stack); // Sacar el '(' de la pila
            }
        } else if (cad[i] == '+' || cad[i] == '-' || cad[i] == '*' || cad[i] == '/') {
            while (!estaVacia(&stack) && precedencia(verTope(&stack)) >= precedencia(cad[i])) {
                resultado[u++] = pop(&stack);
            }
            push(&stack, cad[i]);
        }
        i++;
    }

    while (!estaVacia(&stack)) {
        resultado[u++] = pop(&stack);
    }

    resultado[u] = '\0'; // Terminar la cadena resultado
    printf("\nResultado: %s\n", resultado);

    free(stack.datos); // Liberar memoria ocupada
}

int main() {
    char cadena[100];
    int opc;

    do {
        printf("\nIntroduce una expresion matemática: ");
        scanf("%s", cadena); // Leer una cadena
        postfija(cadena);

        printf("\nIntroduce -1 para salir, cualquier otro numero para continuar: ");
        scanf("%d", &opc);
    } while (opc != -1);

    return 0;
}