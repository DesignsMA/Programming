#include <stdio.h>
#include <time.h>
#include <string.h>
#include <mpfr.h>
#include <gmp.h>
#include <malloc.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

/*
    LIBS
    https://www.mpfr.org/faq.html
    https://gmplib.org/manual/
    
*/

typedef struct {
    int id;
    mpz_t inicio;
    mpz_t fin;
    mpfr_t *result;
    int precision;
} ThreadData; //Datos de un hilo

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

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; // Mutex global


void f(int signo, mpfr_t result, mpz_t n, int precision) {
    mpfr_t temp, temp2;
    mpfr_init2(temp, precision);
    mpfr_init2(temp2, precision);

    mpfr_set_si(temp, signo, MPFR_RNDN); // -1^n
    mpfr_set_z(temp2, n, MPFR_RNDN); // -1^n/(2n+1)
    mpfr_mul_ui(temp2, temp2, 2, MPFR_RNDN);
    mpfr_add_ui(temp2, temp2, 1, MPFR_RNDN);
    mpfr_div(temp, temp, temp2, MPFR_RNDN);
    mpfr_mul_ui(temp, temp, 4, MPFR_RNDN);

    /*
        Race condition

        La variable result es compartida por todos los hilos, por lo que si varios hilos intentan modificarla al mismo tiempo,
        se puede producir una condición de carrera. Para evitar esto, se utiliza un mutex para bloquear la variable result
        mientras se modifica, de manera que solo un hilo pueda modificarla a la vez.

        Solo  aplica  cuando  se  modifica  la  variable  compartida  result,  no  para  la  variable  local  temp.

    */
    // Bloqueamos el mutex antes de modificar result
    pthread_mutex_lock(&mutex); //mutual exclusion

    mpfr_add(result, result, temp, MPFR_RNDN);  // Actualizamos result de manera segura

    // Liberamos el mutex después de modificar result
    pthread_mutex_unlock(&mutex);

    mpfr_clear(temp2);
    mpfr_clear(temp);
}

void *serieArctan(void *arg) {
    ThreadData *datos = (ThreadData *)arg;
    mpz_t i;
    
    mpz_init_set(i, datos->inicio);

    // Determinar el signo inicial basado en el índice inicial
    int signo = (mpz_tstbit(i, 0) == 1) ? -1 : 1;

    mpfr_t *result_ptr = datos->result; // Usar directamente el resultado en el arreglo
    mpfr_init2(*result_ptr, datos->precision);
    mpfr_set_ui(*result_ptr, 0, MPFR_RNDN);

    // Iterar dentro del rango asignado
    // No procesa fin, solo hasta fin - 1, fin se procesa por otro hilo
    while (mpz_cmp(i, datos->fin) < 0) { // i < fin, si i es menor que fin, se sigue ejecutando, si no, se detiene
        f(signo, *result_ptr, i, datos->precision);
        signo = -signo;  // Alternar signo
        mpz_add_ui(i, i, 1);  // Incrementar índice
    }
    gmp_printf("\n\nHilo %d: Inicio: %Zd, Fin: %Zd, Resultado parcial: %.Ff\n", datos->id, datos->inicio, datos->fin, **result_ptr);
    mpz_clear(i);
    pthread_exit(NULL);  // No retornamos nada porque usamos el arreglo compartido
}

char *serieTaylor(mpz_t n, int precision) {
    mp_exp_t mp_exponent;
    char *str, *mpfr_str, c, *substr;
    mpfr_t result;
    mpz_t n_por_hilo, inicio, fin, resto;
    mpz_inits(n_por_hilo, inicio, fin, resto, NULL);

    clock_t start, end;
    double cpu_time_used;

    pthread_t *hilos = (pthread_t *)malloc(NUM_THREADS * sizeof(pthread_t));
    ThreadData *hilo_dato = (ThreadData *)malloc(NUM_THREADS * sizeof(ThreadData));
    mpfr_t *resultados_parciales = (mpfr_t *)malloc(NUM_THREADS * sizeof(mpfr_t)); //arreglo de resultados parciales

    mpz_fdiv_q_ui(n_por_hilo, n, NUM_THREADS);
    unsigned long int resto_ui = mpz_fdiv_r_ui(resto, n, NUM_THREADS);

    mpfr_init2(result, precision);
    mpfr_set_ui(result, 0, MPFR_RNDN);

    // Crear hilos
    for (int i = 0; i < NUM_THREADS; i++) {
        mpz_set_ui(inicio, i); // i
        mpz_mul(inicio, inicio, n_por_hilo); // i * n_por_hilo
        mpz_add(fin, inicio, n_por_hilo); // i * n_por_hilo + n_por_hilo

        if (i == NUM_THREADS - 1) {
            mpz_add_ui(fin, fin, resto_ui);
        }

        mpz_init_set(hilo_dato[i].inicio, inicio);
        mpz_init_set(hilo_dato[i].fin, fin);
        hilo_dato[i].precision = precision;
        hilo_dato[i].id = i;
        hilo_dato[i].result = &resultados_parciales[i]; // Asociar el resultado parcial al apuntaodor
        gmp_printf("Hilo %d: Intervalo [%Zd-%Zd)\n", i, hilo_dato[i].inicio, hilo_dato[i].fin);

        int rc = pthread_create(&hilos[i], NULL, serieArctan, (void *)&hilo_dato[i]);
        if (rc) {
            printf("Error creando hilo %d\n", i);
            exit(-1);
        }
    }

    // Esperar a que terminen los hilos
    start = clock();
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(hilos[i], NULL);
        mpfr_add(result, result, resultados_parciales[i], MPFR_RNDN); // Sumar resultado parcial
        mpfr_clear(resultados_parciales[i]); // Limpiar cada resultado parcial
        mpz_clears(hilo_dato[i].inicio, hilo_dato[i].fin, NULL);
    }

    free(resultados_parciales);
    free(hilos);
    free(hilo_dato);

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    mpfr_str = mpfr_get_str(NULL, &mp_exponent, 10, 0, result, MPFR_RNDN);
    str = (char *)malloc(strlen(mpfr_str) + 50);
    substr = (char *)malloc(strlen(mpfr_str));

    c = mpfr_str[0];
    strcpy(substr, mpfr_str + 1);
    snprintf(str, strlen(mpfr_str) + 50, "%c.%s\nTiempo de ejecucion: %.15f m", c, substr, cpu_time_used / 60.0);

    mpz_clears(n_por_hilo, inicio, fin, resto, NULL);
    mpfr_clear(result);
    free(mpfr_str);
    free(substr);
    return str;
}

void print_formatted_pi(const char *pi_str) {
    printf("Aproximacion:\n%c%c", pi_str[0], pi_str[1]);
    for (size_t i = 2; i < strlen(pi_str); i++) {
        for (int n = 0; n < 5 && i < strlen(pi_str); n++) {
            putchar(pi_str[i]);
            i++;
        }
        i--;
        if (pi_str[i] < '0' || pi_str[i] > '9') { 
            printf("%s", pi_str + i+1);
            break;
        }
        printf(" ");
    }
    printf("\n");
}

int main() {
    mpz_t n;
    mpz_init(n);
    int precision;

    char *pi100 = "\nPrimeros 100 digitos de PI:\n3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 58209 74944 59230 78164 06286 20899 86280 34825 34211 7067\n";

    do {
        printf("\nNumero total de particiones (n) (0 para salir): ");
        gmp_scanf("%Zd", n);
        if (mpz_cmp_ui(n, 0) == 0) break;

        printf("\nPrecision decimal (mayor que 256 bits y divisible entre 2): ");
        scanf("%d", &precision);

        clear_screen();

        if (mpz_cmp_ui(n, 1) >= 0 && precision >= 256 && precision % 2 == 0) {
            char *result = serieTaylor(n, precision);
            print_formatted_pi(result);

            printf("Precision: %d\n%s", precision, pi100);

            FILE *file = fopen("output.txt", "a+");
            if (file) {
                fprintf(file, "Resultado:\n%s\nPrecision: %d\n%s", result, precision, pi100);
                fclose(file);
            } else {
                fprintf(stderr, "Error de apertura de archivo output.txt.\n");
            }

            free(result);
        } else {
            printf("\nDatos erroneos\n");
        }
    } while (mpz_cmp_ui(n, 0) != 0);

    mpz_clear(n);
    return 0;
}
