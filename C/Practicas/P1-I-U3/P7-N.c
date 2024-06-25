#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
int main () {
    int i = 0;
    char *x[20];
    printf (" Introducir debajo cada cadena en una línea \n \n") ;
    printf (" Escribir \'FIN\' para terminar\n \n") ;
    do
    {
        x[i] = (char *)malloc(25 * sizeof(char)); //cadena de 25 caracteres
        fflush(stdin);
        printf(": ");
        scanf("%s", x[i]);
        printf("\n%s | %010x | %d | %d\n", x[i], &x[i], i+1, sizeof(x[i]));
    } while ( strcmp(x[i++], "FIN") != 0 && i != 20);
    
}