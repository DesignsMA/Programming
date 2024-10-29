#include <stdio.h>
#include <stdlib.h>
#include <time.h>
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

void f(mpf_t result,  mpf_t x, int precision) {
    mpf_t temp, temp2;
    mpf_init2(temp, precision);
    mpf_init2(temp2, precision);
    
    // Calculate 2 / (1 + x^2)
    mpf_set_ui(temp, 2);
    mpf_pow_ui(temp2, x, 2);
    mpf_add_ui(temp2, temp2, 1);
    mpf_div(result, temp, temp2);  // result = 2 / (x^2 + 1)

    mpf_clear(temp2);
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
    mpf_init2(h, precision);
    mpf_init2(x1, precision);
    mpf_init2(x2, precision);
    mpf_init2(f_x1, precision);
    mpf_init2(f_x2, precision);

    // Limits
    mpf_set_si(a, -1);
    mpf_set_si(b, 1);
     // h = (b - a) / n
    mpf_sub(h, b, a);
    mpf_div_ui(h, h, n);
    mpf_set_ui(sum, 0);

    for (long int i = 0; i < n; i++) { //sumar partes
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

    }
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
    snprintf(str, strlen(mpf_str) + 50, "%c.%s\nTiempo de ejecucion: %.15f m", c, substr, cpu_time_used/60.0);
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
    int precision, i;
    do
    {
        printf("\nNumero de particiones (n) (-1 para salir): ");
        scanf("%ld", &n);
        printf("\nPrecision decimal (mayor que 256 bits y divisible entre 2): ");
        scanf("%d", &precision);
        

        if ( n >=1 && precision >=256 && precision%2==0) {
            char *result = trapeze(n, precision);
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
                printf(" "); // Print space after each group of 6
            }
            for ( i+=1 ; i < strlen(result); i++ ) putchar(result[i]);
            printf("\nPrecision: %d\n%s", precision, pi100);
            if (result == NULL) {
                fprintf(stderr, "Error ocurrido durante la ejecución.\n");
                return EXIT_FAILURE;
            }

            // Write the result to a text file
            FILE *file = fopen("output.txt", "w+");
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
    } while ( n != -1);
}