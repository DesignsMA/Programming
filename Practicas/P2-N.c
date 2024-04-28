#include <stdio.h>
#include <math.h>

int main() {
    double y, e = 2.7182818284590452354;
    int rounded;
    for (int t = 0; t < 90; t++)
    {
        y = pow(e,-0.1*t) * sin(0.5*t);
        printf("(%02d ,%+0.3f)",t, y);
    	rounded = round((y/0.02));
        if (rounded < 0)
            for (int i = 0; i < (23+rounded); i++)
                printf(" ");
        else
            for (int spaces = 0; spaces < abs(rounded)+23; spaces++) {
                    printf(" ");
                }
        printf("*\n");

        
    }
    
}