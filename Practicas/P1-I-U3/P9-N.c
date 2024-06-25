#include <stdio.h>
#include <math.h>
#include <malloc.h>
#include <ctype.h>
double def(double value){
    return value;
    }

int order(double (*func)(double value), double *x, int n, char type){
    int i,j;
    double temp;
    /*EXTERNAL ITERATOR*/
    for ( i = 0; i < n-1 ; i++) {
        /*INTERNAL ITERATOR*/
        for ( j = i+1; j < n; j++) {
            /*ASCENDENT | DESCENDENT*/
            if (func(*(x+i)) > func(*(x+j)) && type != 'D') { //Defaults to ascendent
                temp = *(x+i);
                *(x+i) = *(x+j);
                *(x+j) = temp;
            } else if (func(*(x+i)) < func(*(x+j)) && type == 'D') {
                temp = *(x+i);
                *(x+i) = *(x+j);
                *(x+j) = temp;
            }
        }
    }
    return 0;
}

int main () {
    int n,i;
    char opc;
    double *x;
    printf("\nEnter the number of values to order: ");
    scanf("%d", &n);
    x = (double *) malloc(n * sizeof(double)); //Allocating space in memory

    for(i = 0; i<n ; i++) {
        printf("\nEnter the value %d: ", i+1);
        scanf("%lf", x+i);
    }
    printf("\nOrder by absolute value? (Y/N): ");
    do
    {
        printf("\n: ");
        opc = toupper(getchar());
    } while (opc != 'Y' && opc != 'N');

    printf("\nOrder type\n\'A\' For ascendent\t\'D\' For descendent\n: ");
    fflush(stdin);
    if (opc == 'Y') order(fabs, x, n, toupper(getchar()) );
    else order(def, x, n, toupper(getchar()) );

    for (i = 0; i < n; i++)
    {
        printf("\nValue %d: %.02lf", i+1, *(x+i));
    }
    

    
}