#include <math.h>
#include <stdio.h>
/*Retorna la razon en que se componen los intereses
 n anios, i tasa de interes, m periodos por anio
*/

double mensual (double n, double i, int m) {
    double razon, factor;
    factor = 1 + (i/m);
    razon = 12 * (pow(factor,m*n) - 1)/i;
    return(razon);
}

double diaria (double n, double i, int m) {
    double razon, factor;
    factor = 1 + (i/m);
    razon = (pow(factor,m*n) - 1) / (pow(factor,m*12) - 1);
    return(razon);
}

double continua (double n, double i, int m) {
    double razon;
    razon = (exp(i*n) - 1) / (exp(i*12) - 1);
    return(razon);
}

void tabla ( double (*funcion)(double n, double i, int m), double a, int m, double n) {
    double i,f;
    int cont;
    printf("\nTASA DE INTERES\tCANTIDAD FUTURA\n\n");
    for (cont = 1; cont <= 20; cont++)
    {
        i = 0.01 * cont;
        f = a * (*funcion)(n,i,m);
        printf("             %2d\t%.2f\n", cont, f);
    }
}

int main () {
    int m;
    double n,a;
    char frec;
    printf("\nIntroduzca el capital inicial: ");
    scanf("%lf", &a);
    printf("\nIntroduzca el numero de anios: ");
    scanf("%lf", &n);
    printf("\nIntroduzca la frecuencia de composicion (M, D, C): ");
    scanf(" %c", &frec);
    do
    {
        switch (frec)
        {
        case 'M':
            do 
            {
                printf("\nIntroduzca el numero de periodos de composicion anual 1-12\n1 - ANUAL | 2 - SEMESTRAL | 4 - TRIMESTRAL | 12 - MENSUAL\n: ");
                scanf("%d", &m);
            } while (m < 1 && m >12);
            tabla(mensual, a, m, n);
            break;

        case 'D':
            m = 360;
            tabla(diaria, a, m, n);
            break;

        case 'C':
            m = 0;
            tabla(continua, a, m, n);
            break;
        
        default:
            break;
        }
    } while (frec != 'M' && frec != 'D' && frec != 'C');
    

}