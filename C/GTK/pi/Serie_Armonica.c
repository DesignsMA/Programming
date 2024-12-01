#include <stdio.h>
#include <time.h>
#include <string.h>
#include <gmp.h>
#include <stdlib.h>
#include <pthread.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int id;
    unsigned long int  inicio;
    unsigned long int  fin;
    int precision;
}ThreadData; //Datos de un  hilo

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

void f(mpf_t result, unsigned long int n, int precision) { //Da el termino N
    mpf_t temp; //flotantes de alta  precision
    if ( n!=0) {
        mpf_init2(temp, precision);
        mpf_set_ui(temp, 1); //asignar 1 
        mpf_div_ui(temp, temp, n);  //temp <- 1/N
        mpf_add(result, result, temp); //result  <- result+temp
        mpf_clear(temp);
    }
}


void *serieArmonica(void *arg) { //Da el termino N
    ThreadData *datos = (ThreadData*)arg; //puntero a los datos
    mpf_t *result_ptr = malloc(sizeof(mpf_t));
    mpf_init2(*result_ptr, datos->precision); //inicializar contenido  de apuntador a mpf

    for (unsigned long int i = datos->inicio; i <= datos->fin; i++) { //Calculo de la sumatoria
        f(*result_ptr,  i, datos->precision); //calcular  termino y sumar
    }
    //se calcula la suma parcial de inicio  a fin
    pthread_exit((void *)result_ptr);
}

char *serieTaylor(unsigned long int n, int precision) {
    mp_exp_t mp_exponent;
    char *str, *mpf_str, c, *substr;
    int inicio=0, fin =0;
    mpf_t result;

    clock_t start, end;
    double cpu_time_used;

    pthread_t *hilos = malloc(NUM_THREADS * sizeof(pthread_t)); /*Alojar memoria de los hilos*/
    ThreadData *hilo_dato = malloc(NUM_THREADS * sizeof(ThreadData)); /*alojar datos  de hilos*/
    void *retval;
    unsigned long int n_por_hilo = n / NUM_THREADS; // Número de términos por hilo
    unsigned long int resto = n % NUM_THREADS;      // Términos restantes

    mpf_init2(result, precision);

    for (int i = 0; i < NUM_THREADS; i++) {
        hilo_dato[i].inicio = i * n_por_hilo;           // Inicio de la tarea para este hilo
        hilo_dato[i].fin = (i + 1) * n_por_hilo - 1;    // Fin de la tarea para este hilo

        if (i == NUM_THREADS - 1) {
            hilo_dato[i].fin += resto; // Asignar el resto al último hilo
        }

        hilo_dato[i].precision = precision;

        // Crear el hilo
        int rc = pthread_create(&hilos[i], NULL, serieArmonica, (void *)&hilo_dato[i]);
        if (rc) {
            printf("Error creando hilo %d\n", i);
            exit(-1);
        }
    }

    start = clock(); //Empezar a contar reloj
    // Esperar que todos los hilos terminen
    for (int i = 0; i < NUM_THREADS; i++) {
        void *retval;
        pthread_join(hilos[i], &retval);

        mpf_t *seriecalculada = (mpf_t *)retval;
        pthread_mutex_lock(&mutex); // Bloquear antes de acceder a `result`
        mpf_add(result, result, *seriecalculada);
        pthread_mutex_unlock(&mutex);
        mpf_clear(*seriecalculada);
        free(seriecalculada);
    }
    pthread_mutex_destroy(&mutex); // Liberar mute
    free(hilos);
    free(hilo_dato);
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
            printf("\nPrecision: %d\n", precision);
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
            fprintf(file, "%s\nPrecision: %d", result, precision); //Escribir datos en archivo
            fclose(file);
            free(result);
        }
        else printf("\nDatos erroneos");

        /* code */
    } while ( n != 0);
}