#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <gmp.h>
#include <stdlib.h>
#define NUM_THREADS 4  // Numero de hilos

typedef struct {
    int id;
    int inicio;
    int fin;
} ThreadData; //Datos de un  hilo

void clear_screen() {
    #ifdef _WIN32
        system("cls"); // Windows
    #else
        system("clear"); // Unix/Linux
    #endif
}

#ifdef _WIN32
    #include <windows.h>
    #define NUM_THREADS ({ \
        SYSTEM_INFO sysinfo; \
        GetSystemInfo(&sysinfo); \
        sysinfo.dwNumberOfProcessors; \
    })
#elif defined(__linux__)
    #include <unistd.h>
    #define NUM_THREADS sysconf(_SC_NPROCESSORS_ONLN)
#else
    #error "Unsupported platform"
#endif
/*
    Serie de taylor para tangente
    de n = 0 a inf
    (-1)^n*x^(2n+1)
    _______________
        2n+1
    
    Evaluada arctan(1) = PI/4
    = sumatoria de n = 0 a inf
       (-1)^n
    _______________
        2n+1
*/

void f(int signo,  mpf_t result, unsigned long int n, int precision) { //Da el termino N
    mpf_t temp, temp2; //flotantes de alta  precision
    mpf_init2(temp, precision);
    mpf_init2(temp2, precision);

    mpf_set_si(temp, signo); //asignar 1  o -1
    mpf_set_ui(temp2, n); //temp2 <- n
    mpf_mul_ui(temp2, temp2, 2); //temp2 <- 2n
    mpf_add_ui(temp2, temp2, 1);  //temp2 <- 2n + 1
    mpf_div(temp, temp, temp2);  //temp <- -1^n / 2n + 1
    mpf_mul_ui(temp, temp, 4); //temp <- temp*4
    mpf_add(result, result, temp); //result  <- result+temp
    mpf_clear(temp2); //Limpieza  de memoria
    mpf_clear(temp);
}

char *serieTaylor(unsigned long int n, int precision) {
    mp_exp_t mp_exponent;
    char *str, *mpf_str, c, *substr;
    int signo = 1;
    mpf_t result;

    clock_t start, end;
    double cpu_time_used;

    pthread_t *hilos = malloc(NUM_THREADS * sizeof(pthread_t)); /*Alojar memoria de los hilos*/
    ThreadData *hilo_dato = malloc(NUM_THREADS * sizeof(ThreadData));

    int n_por_hilo = n / NUM_THREADS; // Número de términos por hilo
    int resto = n % NUM_THREADS; // Términos restantes si no son divisibles de manera exacta
    
    int inicio = 0;
    for (int i = 0; i < NUM_THREADS; i++) { //Por cada hilo
        hilo_dato[i].id = i;
        hilo_dato[i].inicio = inicio;

        // Si el hilo no es el último, se le asignan n_por_hilo términos
        if (i < (NUM_THREADS-1)) {
            hilo_dato[i].fin = inicio + n_por_hilo; // Un término más para los primeros `remainder` hilos
        } else {
            hilo_dato[i].fin = inicio + n_por_hilo + resto;
        }

        inicio = hilo_dato[i].fin + 1; // iniciar desde  el  ultimo n

        // Crear el hilo
        int rc = pthread_create(&threads[i], NULL, calculate_series, (void *)&thread_data[i]);
        if (rc) {
            printf("Error creating thread %d\n", i);
            exit(-1);
        }
    }

    // Esperar que todos los hilos terminen
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(hilos[i], NULL);
    }

    // Liberar memoria
    free(threads);
    free(thread_data);

    start = clock(); //Empezar a contar reloj

    mpf_init2(result, precision);
    for (unsigned long int i = 0; i < n; i++) { //Calculo de la sumatoria
        f(signo, result,  i, precision); //calcular  termino y sumar
        signo = -signo;
    }
    end = clock(); //Terminar reloj
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;  // Calcular el tiempo
    mpf_str = mpf_get_str(NULL, &mp_exponent, 10, 0, result); //Convierte result a cadena
    str = (char *)malloc(strlen(mpf_str) + 50);
    substr = (char *)malloc(strlen(mpf_str));

    if (substr == NULL) {
        free(mpf_str);
        return NULL;
    }

    c = mpf_str[0]; //Primer número
    strcpy(substr, (char *)mpf_str + 1);
    snprintf(str, strlen(mpf_str) + 50, "%c.%s\nTiempo de ejecucion: %.15f m", c, substr, cpu_time_used/60.0);

    mpf_clear(result);
    free(mpf_str);
    free(substr);
    return str; // Retorna la cadena con formato
}

int main() {
    unsigned long int n;
    int precision, i;
    do
    {
        printf("\nNumero de particiones (n) (0 para salir): ");
        scanf("%lu", &n);
        if (  n == 0 ) return 0;
        printf("\nPrecision decimal (mayor que 256 bits y divisible entre 2): ");
        scanf("%d", &precision);
        clear_screen();
        if ( n >=1 && precision >=256 && precision%2==0) {
            char *result = serieTaylor(n, precision);
            char *pi100 = (char*)malloc(150 * sizeof(char)); 
            strcpy(pi100, "\nPrimeros 100 digitos:\n3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 58209 74944 59230 78164 06286 20899 86280 34825 34211 7067\n");
            printf("Aproximacion:\n%c%c", result[0], result[1]);
            for ( i = 2; i < strlen(result); i++) {
                for (int n = 0; n < 5 && i < strlen(result); n++) {
                    putchar(result[i]);
                    i++;
                }
                i--;
                if (result[i] < '0' || result[i] > '9') break; //
                printf(" "); // Espacios entre digitos
            }
            for ( i+=1 ; i < strlen(result); i++ ) putchar(result[i]); //imprimir datos restantes
            printf("\nPrecision: %d\n%s", precision, pi100);
            if (result == NULL) {
                fprintf(stderr, "Error ocurrido durante la ejecución.\n");
                return EXIT_FAILURE;
            }

            // Escribir a archivo
            FILE *file = fopen("output.txt", "a+");
            if (file == NULL) {
                fprintf(stderr, "Error de apertura de archivo output.txt.\n");
                free(result);
                return EXIT_FAILURE;
            }
            free(pi100);
            fprintf(file, "%s\nPrecision: %d", result, precision); //Escribir datos en archivo
            fclose(file);
            free(result);
        }
        else printf("\nDatos erroneos");

        /* code */
    } while ( n != 0);
}