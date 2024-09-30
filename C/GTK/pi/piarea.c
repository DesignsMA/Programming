#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <malloc.h>
#include <unistd.h> // for usleep()
#include <string.h>
#include <gmp.h>

#include <stdlib.h>

void clear_screen() {
    #ifdef _WIN32
        system("cls"); // Windows
    #else
        system("clear"); // Unix/Linux
    #endif
}

void f(mpf_t result, const mpf_t x, int precision) {
    mpf_t temp;
    mpf_init2(temp, precision);
    
    // Calculate x^2
    mpf_pow_ui(temp, x, 2);         // temp = x^2
    
    mpf_t one; 
    mpf_init_set_ui(one, 1); // Initialize one to 1
    mpf_sub(temp, one, temp); // temp = 1 - x^2

    // Calculate sqrt(1 - x^2)
    mpf_sqrt(result, temp);        // result = sqrt(1 - x^2)

    // Clear the temporary variable
    mpf_clear(one);
    mpf_clear(temp);
}

char *trapeze(long int n, int precision) {
    mp_exp_t mp_exponent;
    char *str, *mpf_str, c, *substr;
    mpf_t h, sum, result, x1, x2, f_x1, f_x2, a, b;
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    mpf_init2(a, precision);
    mpf_init2(b, precision);
    mpf_init2(result, precision);
    mpf_init2(sum, precision);
    mpf_init(h);
    mpf_init(x1);
    mpf_init(x2);
    mpf_init2(f_x1, precision);
    mpf_init2(f_x2, precision);

    // Limits
    mpf_set_si(a, -1);
    mpf_set_si(b, 1);
    // h = (b - a) / n
    mpf_sub(h, b, a);
    mpf_div_ui(h, h, n);
    mpf_set_ui(sum, 0);
    mpf_set_ui(result, 0); // Initialize result

    for (long int i = 0; i < n; i++) {
        // x1 = a + i*h
        mpf_mul_ui(x1, h, i);
        mpf_add(x1, a, x1);
        // x2 = a + (i + 1) * h
        mpf_mul_ui(x2, h, i + 1);
        mpf_add(x2, a, x2);
        // f(x1) and f(x2)
        f(f_x1, x1, precision);
        f(f_x2, x2, precision);
        // sum = (f(x1) + f(x2)) / 2 * h
        mpf_add(sum, f_x1, f_x2);
        mpf_div_ui(sum, sum, 2);
        mpf_mul(sum, sum, h);
        // Accumulate to result
        mpf_add(result, result, sum);
        usleep(10);
        printf(".");
        clear_screen();
    }

    mpf_mul_ui(result, result, 2); // multiply by two

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    mpf_str = mpf_get_str(NULL, &mp_exponent, 10, 0, result);
    str = (char *)malloc(strlen(mpf_str) + 50);
    substr = (char *)malloc(strlen(mpf_str));

    if (substr == NULL) {
        free(mpf_str);
        return NULL; // Error handling
    }

    c = mpf_str[0];
    strcpy(substr, (char *)mpf_str + 1);
    snprintf(str, strlen(mpf_str) + 50, "Aproximacion: %c.%s\nTiempo de ejecucion: %.35f s", c, substr, cpu_time_used);

    // Clear memory
    mpf_clear(h);
    mpf_clear(sum);
    mpf_clear(result);
    mpf_clear(x1);
    mpf_clear(x2);
    mpf_clear(f_x1);
    mpf_clear(f_x2);
    mpf_clear(a);
    mpf_clear(b);
    free(mpf_str);
    free(substr);
    return str; // Return the formatted string
}

int main() {
    long int n;
    int precision;
    do
    {
        printf("Numero de particiones (n) (-1 para salir): ");
        scanf("%ld", &n);
        printf("\nPrecision decimal (mayor que 256 bits y divisible entre 2): ");
        scanf("%d", &precision);
        

        if ( n >=1 && precision >=256 && precision%2==0) {
            printf("\nArchivo output.txt siendo generado...");
            char *result = trapeze(n, precision);
            printf("\n%s", result);
            if (result == NULL) {
                fprintf(stderr, "Error ocurrido durante la ejecución.\n");
                return EXIT_FAILURE;
            }

            // Write the result to a text file
            FILE *file = fopen("output.txt", "w");
            if (file == NULL) {
                fprintf(stderr, "Error de apertura de archivo output.txt.\n");
                free(result);
                return EXIT_FAILURE;
            }

            fprintf(file, "%s\n", result);
            fclose(file);
            free(result);
        }
        else printf("\nDatos erroneos");

        /* code */
    } while ( n != -1);
}