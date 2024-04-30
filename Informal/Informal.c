/*El alumno usará el lenguaje C con DEVCPP para el desarrollo de un
programa que lee N (entero entre 1 y 20) y lo valida. Después debe leer N
datos y después:
a) Imprimir el promedio.
b) Imprimir el Máximo.
c) Imprimir el Mínimo*/

#include <stdio.h>
int main(){
    int n, i, prom, aux, suma, min, max;
    prom=0, suma=0, aux=0, max=0, min=0;
    printf("\nDeme el valor de n: \n");
    scanf("%d", &n);
    if( n>=1 && n<=20 ){
        printf("\nn es valido\n");
        printf("\nDeme los datos: \n");
        for( i=0; i<n; i++){
            printf("\nDeme el dato %d\n", i+1);
            scanf("%d", &aux);
            suma += aux;
            if( aux >= max ){
                max=aux;
            }
            if( i==0 ){
                min=aux;
            }
            if(min >= aux){
                min=aux;
            }
        }    
        prom=suma/n;
        printf("\nEl promedio es: %d\n", prom);
        printf("\nEl max es: %d\n", max);
        printf("\nEl min es: %d\n", min); 
    }
    else{
        printf("\nNo valido\n");
    }
}