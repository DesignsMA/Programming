#include <time.h>
#include <stdlib.h>
#include <malloc.h>
#include <unistd.h> //Para usar sleep()

typedef struct nodo {
	int dato;
	struct nodo *sig;
}NODO;

/*Recibe un apuntador al primer caracter de una cadena, la modifica y genera un
  codigo de forma ABC-123 donde las letras y numeros son aleatorias en base a la 
  semilla generada por el tiempo
*/
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

void imprimeLista(NODO *ap){
	while(ap!=NULL) {
		printf("\nDato: %d", ap->dato);
		ap=ap->sig;
	}
	printf("\nFin\n\n");
} 
NODO *creaNodo (int dato) {
	NODO *nuevo;
	nuevo=(NODO *)malloc(sizeof(NODO));
	if (nuevo != NULL) {
		nuevo->dato=dato;
		nuevo->sig=NULL;
	}
	return nuevo;
}

NODO *insertaFinal(NODO *ap, int d) {
	NODO *aux, *nuevo;
	
	nuevo=creaNodo(d);
	if (nuevo == NULL) return ap;
	if (ap==NULL) {
		ap=nuevo;
	}
	else {
		aux=ap;
		while(aux->sig != NULL) {
			aux=aux->sig;
		}	
		aux->sig=nuevo;
	}
	return ap;
}

NODO *insertaAlInicio(NODO *ap, int d) {
	NODO *aux, *nuevo;
	
	nuevo=creaNodo(d);
	if (nuevo == NULL) return ap;
	aux=ap;
	ap=nuevo;
	nuevo->sig=aux;
	return ap;
}

int cuentaNodos(NODO *ap){
	int c;
	
	c=0;
	while (ap!=NULL) {
		ap=ap->sig;
		c++;
	}
	return c;
}
	
int main() {
	NODO *raiz, *raiz1;

	printf("\n Primera lista");
	raiz=NULL;
}