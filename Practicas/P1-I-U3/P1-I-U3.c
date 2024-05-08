#include <stdio.h>

void cifrar(int clave, char entrada[50], FILE *salida) 
{
    FILE *entradaP;
    char actual;
    int distancia;
    entradaP = fopen(entrada, "r");

    if ( entradaP == NULL ) {
        printf("No existe el archivo de cifrado\n");
    } 
    else {
        while (feof(entradaP) == 0)
        {
            actual = fgetc(entradaP);
            if ( actual >= 'a' && actual <= 'z') {
                distancia = (clave-('z'-actual));
                actual = (actual+clave > 'z' ? 'a' + distancia-1 : actual + clave);
            }
            else if (actual >= 'A' && actual <= 'Z') {
                distancia = (clave-('Z'-actual));
                actual = (actual+clave > 'Z' ? 'A' + distancia-1 : actual + clave);
            }

            if ( actual >= 32 && actual <= 255)
                putc(actual, salida);

        }
    }
    fclose(salida);
    fclose(entradaP);
}

void descifrar(int clave, char entrada[50], FILE *salida) 
{
    FILE *entradaP;
    char actual;
    int distancia;
    entradaP = fopen(entrada, "r");


    if ( entradaP == NULL ) {
        printf("No existe el archivo de descifrado\n");
    } 
    else {
        while (feof(entradaP) == 0)
        {
            actual = fgetc(entradaP);
            if ( actual >= 'a' && actual <= 'z') {
                distancia = (clave-(actual-'a'));
                actual = (actual-clave < 'a' ? 'z' - (distancia-1) : actual - clave);
            }
            else if (actual >= 'A' && actual <= 'Z') {
                distancia = (clave-(actual- 'A'));
                actual = (actual-clave < 'A' ? 'Z' - (distancia-1) : actual - clave);
            }
            
            if ( actual >= 32 && actual <= 255)
                putc(actual, salida);
        }
    }
    fclose(salida);
    fclose(entradaP);
}

int main () 
{
    FILE *salida, *salida2;
    salida = fopen("salida.txt", "w");
    salida2 = fopen("salida2.txt", "w");
    cifrar(5,"entrada.txt", salida);
    descifrar(5,"salida.txt", salida2);
}
