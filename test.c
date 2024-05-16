#include <stdio.h>

int main() {
    int N;

    // Leer N
    printf("Ingrese un número entre 0 y 9: ");
    scanf("%d", &N);

    // Validar N
    if (N < 0 || N > 9) {
        printf("El número ingresado no está en el rango permitido.\n");
        return 1; // Salir del programa con error
    }

    // Escribir la tabla de multiplicar de N
    printf("Tabla de multiplicar de %d:\n", N);
    for (int i = 1; i <= 10; i++) {
        printf("%d x %d = %d\n", N, i, N * i);
    }

    return 0; // Salir del programa con éxito
}