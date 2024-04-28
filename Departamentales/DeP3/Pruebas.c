#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <windows.h>
#include <time.h>
#include <stdlib.h>

void uid ( char uid[10]) {
    int min = 65;
    int max = 90;
    int random_number;

    do
    {
        srand(time(NULL));
        printf("\nUID: ");
        for (int i = 0; i < 5; i++)
        {
            random_number = rand() % (max - min + 1) + min;
            printf("%c", random_number);
        }
        printf("-");
        for (int i = 0; i < 3; i++)
        {
            printf("%d\n", rand() % (9 - 1 + 1) + 1);
        }
        sleep(2);
    } while ( 1 );
    
}

#define N 15

typedef struct nodo {
	char id[50];
	int urgencia;
	int operaciones;
	struct nodo *siguiente;
}Nodo;

Nodo *crearNodo (char nombre[], int urg, int ope) {
	Nodo *nuevo;
	nuevo = (Nodo *)malloc(sizeof(Nodo));
	if (nuevo != NULL) {
		strcpy(nuevo->id, nombre);
		nuevo->urgencia = urg;
		nuevo->operaciones = ope;
		nuevo->siguiente = NULL;
	}
	return nuevo;
}

Nodo *ordenLista(Nodo *lista, char nombre[], int urgencia, int operaciones) {
	Nodo *aux, *aux2, *nuevo;
	char booleano;
	booleano = 'a';
	nuevo=crearNodo(nombre, urgencia, operaciones);
	if (nuevo == NULL) return lista;
	if (lista == NULL) {
		lista = nuevo;
	}
	else {
		aux = lista;
		aux2 = lista;
		if (urgencia != 4) {
			while (nuevo->urgencia >= aux->urgencia) {
				aux = aux->siguiente;
				if (booleano != 'a') {
					aux2 = aux2->siguiente;
				}
				else {
					booleano = 'b';
				}
			}
			if (booleano != 'a') {
				nuevo->siguiente = aux;
				aux2->siguiente = nuevo;
			}
			else {
				nuevo->siguiente = aux;
				lista = nuevo;
			}
		}
		else {
			while(aux->siguiente != NULL) {
				aux = aux->siguiente;
			}	
			aux->siguiente = nuevo;
		}
	}
	return lista;
}

void imprimeLista (Nodo *lista) {
	while (lista != NULL) {
		printf("Nombre %s, urgencia %d, operaciones %d \n", lista->id, lista->urgencia, lista->operaciones);
		lista = lista->siguiente;
	}
	printf("\n");
}

void dime(Nodo *lista, int n){
	char nombre[50], op;
	int urgencia, operaciones;
	for (int i = 0; i < n; i++){
		system("cls");
		if (lista != NULL) imprimeLista(lista);
		printf("Dame tu nombre \nR: ");
		scanf("%s", nombre);
		system("cls");
		fflush(stdin);
		printf("¿Tienes urgencia? \n1.-Si \n2.-No \nR: ");
		scanf("%c", &op);
		system("cls");
		if (op == '1') {
			printf("Dime tu numero de urgencia \n1.-Mucha urgencia \n2.-Tengo urgencia \n3.-Un poco de urgencia \nR: ");
			scanf("%d", &urgencia);
		}
		else if (op == '2') {
			urgencia = 4;
		}
		system("cls");
		printf("¿Cuantas opercaciones vas a realizar \nR: ");
		scanf("%d", &operaciones);
		lista = ordenLista(lista, nombre, urgencia, operaciones);
	}
	
	
}

int main(int argc, char *argv[]) {
	Nodo *raiz;
	raiz = NULL;
	
	dime(raiz, N);
	
	
	return 0;
}