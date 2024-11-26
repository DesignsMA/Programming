#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <gmp.h>
#include <stdlib.h>
#define PRECISION 256

char *format_mpf_to_decimal(char *mantissa, mp_exp_t exponent, char *other, short int decimal) {
    size_t len = strlen(mantissa);
    size_t len2 = strlen(other);
    char *formatted;

    // Si el exponente es negativo o 0
    if ( decimal == 0 ) {
        // Aseguramos que el punto decimal se coloque entre el primer y segundo dígito
        formatted = malloc(len + 2 + len2);  // Espacio para el punto y 'other'
        if (!formatted) return NULL;

        // Colocar el punto entre los primeros dos dígitos
        strncpy(formatted, mantissa, 1); // Copiar el primer dígito
        formatted[1] = '.'; // Insertar el punto
        strcpy(formatted + 2, mantissa + 1); // Copiar el resto de la mantisa
        strcat(formatted, other); // Concatenar 'other'
    }
    // Si el exponente es negativo
    else {
        // Colocamos un 0. antes de la mantisa
        formatted = malloc(len + 3 + len2); // Espacio para "0." y 'other'
        if (!formatted) return NULL;

        // Colocar "0." al inicio
        if  (mantissa[0] == '-') {
        mantissa[0]='.';
        sprintf(formatted, "-0%s", mantissa);
        } else {
            sprintf(formatted, "0.%s", mantissa);
        }
        strcat(formatted, other); // Concatenar 'other'
    }

    return formatted;
}




void serieArctan(int signo,  mpf_t serieParcial, unsigned long int n) { //Da el termino N
    mpf_t temp, temp2; //flotantes de alta  PRECISION
    mpf_init2(temp, PRECISION);
    mpf_init2(temp2, PRECISION);

    mpf_set_si(temp, signo); //asignar 1  o -1
    mpf_set_ui(temp2, n); //temp2 <- n
    mpf_mul_ui(temp2, temp2, 2); //temp2 <- 2n
    mpf_add_ui(temp2, temp2, 1);  //temp2 <- 2n + 1
    mpf_div(temp, temp, temp2);  //temp <- -1^n / 2n + 1
    mpf_mul_ui(temp, temp, 4); //temp <- temp*4
    mpf_add(serieParcial, serieParcial, temp); //serieParcial  <- serieParcial+temp
    mpf_clear(temp2); //Limpieza  de memoria
    mpf_clear(temp);
}

// Función principal de la serie de Taylor para calcular pi
char *serieTaylor(unsigned long int n) {
    mp_exp_t mp_exponent;
    int signo = 1;
    mpf_t serieParcial;

    const char *pi_100_digits = 
        "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679";

    mpf_t pi;
    mpf_init2(pi, PRECISION);

    // Configurar el valor de pi
    if (mpf_set_str(pi, pi_100_digits, 10) != 0) {
        fprintf(stderr, "Error al inicializar el valor de pi.\n");
        return NULL;
    }
    mpf_init2(serieParcial, PRECISION);

    for (unsigned long int i = 0; i <= n; i++) { 
        serieArctan(signo, serieParcial, i);
        signo = -signo;
    }

    mpf_sub(pi, serieParcial, pi);  // pi - serieParcial -> El error

    // Convertir serieParcial y pi a cadenas
    char *mpf_str = mpf_get_str(NULL, &mp_exponent, 10, 0, serieParcial);
    char *mpf_str2 = mpf_get_str(NULL, &mp_exponent, 10, 0, pi);

    // Formatear con punto decimal y concatenar el error
    char *formatted_serieParcial = format_mpf_to_decimal(mpf_str, mp_exponent, "\nError: ",  0);
    char *formatted_error = format_mpf_to_decimal(mpf_str2, mp_exponent, "", 1);

    // Concatenar serieParcial y error
    char *final_result = malloc(strlen(formatted_serieParcial) + strlen(formatted_error) + 1);
    if (final_result) {
        strcpy(final_result, formatted_serieParcial);
        strcat(final_result, formatted_error);
    }

    // Limpiar memoria
    mpf_clear(serieParcial);
    free(mpf_str);
    free(mpf_str2);
    free(formatted_serieParcial);
    free(formatted_error);

    return final_result; // Retorna la cadena con formato
}

int main() {
    clock_t inicio, fin;
    double tiempo;
    int estatus;

    unsigned long int n;

    do {
        do
        {
            printf("\nNumero de terminos a calcular, coloque cero para terminar: ");
            estatus = scanf("%lu", &n);
            if (estatus != 1) {
                // Si no se lee un número entero correctamente
                printf("Error: No se ingresó un número entero válido.\n");
            }
            while (getchar() != '\n');  // Lee y descarta caracteres hasta el fin de línea
        } while ( estatus != 1);
        
        if (n == 0) return 0;

        inicio = clock();
        char *serieParcial = serieTaylor(n);
        fin = clock();
        tiempo = ((double)(fin - inicio)) / CLOCKS_PER_SEC;

        printf("\nAproximacion:\n%s\nTiempo en completar: %.5f segundos\n", serieParcial, tiempo);
        free(serieParcial);
    } while (n != 0);

    return 0;
}