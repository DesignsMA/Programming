#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <windows.h>

void  uid ( char *uid) {
    int min = 65, max = 90, i = 0;
    srand(time(NULL));
    for(i; i < 3; i++) {
        uid[i] = rand() % (max - min + 1) + min; 
    }
    uid[i] = '-';
    i++;
    for(i; i < 7; i++) {
        uid[i] = rand() % ('9' - '1' + 1) + '1';
    }
}

int main () {
    char string[8];
    char *sptr; //pointer to the first char
    sptr = string;
    do
    {
        uid(sptr);
        printf("uid: %s\n", string);
        sleep(2);
    } while (1);
    

}
    