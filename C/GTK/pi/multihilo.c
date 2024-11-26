#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Función que ejecutará cada hilo
void *calcular_suma(void *arg) {
    int n = *(int *)arg; // El número de términos a sumar
    int suma = 0;
    for (int i = 1; i <= n; i++) {
        suma += i;
    }
    // Retornar la suma como puntero
    int *resultado = malloc(sizeof(int));
    *resultado = suma;
    pthread_exit((void *)resultado);
}

int main() {
    int n_hilos = 3; // Número de hilos
    int terminos[] = {5, 10, 15}; // Términos a calcular por cada hilo
    pthread_t hilos[n_hilos];
    void *retval;
    int suma_total = 0;

    // Crear los hilos
    for (int i = 0; i < n_hilos; i++) {
        if (pthread_create(&hilos[i], NULL, calcular_suma, &terminos[i]) != 0) {
            perror("Error al crear el hilo");
            return 1;
        }
    }

    // Esperar a que los hilos terminen y sumar sus resultados
    for (int i = 0; i < n_hilos; i++) {
        if (pthread_join(hilos[i], &retval) != 0) {
            perror("Error al esperar al hilo");
            return 1;
        }
        int *resultado = (int *)retval;
        printf("El hilo %d retornó la suma: %d\n", i + 1, *resultado);
        suma_total += *resultado;
        free(resultado); // Liberar la memoria asignada en el hilo
    }

    printf("La suma total de todos los hilos es: %d\n", suma_total);

    return 0;
}
