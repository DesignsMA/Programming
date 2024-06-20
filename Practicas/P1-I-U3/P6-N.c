#include <stdio.h>
#include <malloc.h>
typedef struct NODE
{
    short remainder;
    struct NODE *to;
} NODE;

NODE *newNode(short remainder) {
    NODE *newNode = (NODE *)malloc(sizeof(NODE));
    if (newNode == NULL)
    {
        printf("Error: Couldn't assign space in memory\n");
        return NULL;
    }
    newNode->remainder = remainder;
    newNode->to = NULL;
    return newNode;
}

NODE *lifo(NODE *root, short remainder) {
    NODE *node = newNode(remainder);
    if (node == NULL) return NULL;
    node->to = root;
    root = node;
    return root;
}

void hexadecimal(int dec) {
    char hexa[16] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'A', 'B', 'C', 'D', 'E', 'F'};
    int quotient = dec;
    NODE *remainders = NULL, *aux;
    do
    {
        remainders = lifo(remainders, quotient%16);
        quotient = quotient/16;
    } while ( quotient >= 16);
    printf("%c", hexa[quotient]);

    while (remainders != NULL)
    {
        printf("%c", hexa[remainders->remainder]);
        aux = remainders;
        remainders = remainders->to;
        free(aux);
    }
}

void baseChanger(int dec, int base) {
    char bases[16] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     'A', 'B', 'C', 'D', 'E', 'F'};
    int quotient = dec;
    NODE *remainders = NULL, *aux;
    do
    {
        remainders = lifo(remainders, quotient%base);
        quotient = quotient/base;
    } while ( quotient >= base);
    
    printf("%c", bases[quotient]);
    while (remainders != NULL)
    {
        printf("%c", bases[remainders->remainder]);
        aux = remainders;
        remainders = remainders->to;
        free(aux);
    }
}

int main() {
    int dec, custom = 0;
    do
    {
        printf("Enter a decimal number: ");
        scanf("%d", &dec);
        while ( custom < 2)
        {
            fflush(stdin);     
            printf("Enter a custom system conversion number: ");
            scanf("%d", &custom);
        }
        hexadecimal(dec);
        printf(" Hex |\t");
        baseChanger(dec,8);
        printf(" Oct |\t");
        baseChanger(dec,2);
        printf(" Bin |\t");
        baseChanger(dec,custom);
        printf(" Custom\n");
        fflush(stdin);
        custom = 0;     
    } while (getchar() != 'x');
}