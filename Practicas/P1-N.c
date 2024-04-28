#include <stdio.h>

int main() {
    int pivot = 1, sideState = 1, rowSize = 1,auxpivot;
    for ( int rows = 0; rows < 10; rows++)
    {
        auxpivot = pivot;
        for (int i = 0; i <= (10-pivot); i++) {
            printf(" ");
        }
        for (int i = 0; i < rowSize; i++ ) 
        {
            if (auxpivot == rowSize ) sideState = -1;
            if(auxpivot < 10) {
                printf("%d", auxpivot);
            } else printf("%d", auxpivot-10);
            
            auxpivot += sideState;
        }
        printf("\n");
        sideState = 1;
        rowSize += 2;
        pivot++;
        
    }
}