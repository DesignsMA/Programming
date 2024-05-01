#include <time.h> //generar semilla en base a tiempo
#include <stdio.h>
#include <stdlib.h> // funciones rand
#include <malloc.h>
#include <unistd.h> //Para usar sleep(), usleep() (FUNCIONA EN LINUX, MAC Y ANDROID)
typedef struct NODO {
	char uid[8]; //ABC-789\0
	int urgencia, operaciones;
	struct NODO *sig;
}NODO;

void systemCLS() {
    #ifdef _WIN32 //Si es windows
        system("cls"); //ejecuta comando (no necesita libreria)
    #else //Si no, usar clear (linux y mac)
        system("clear"); //ejecuta comando (no necesita libreria)
    #endif
}

void imprimeLista(NODO *ap){
    printf("\n------------------------------------------------------");
	while(ap!=NULL) {
		printf("\nUrgencia: %d | Operaciones: %d | UID: %s", ap->urgencia, ap->operaciones, ap->uid);
		ap=ap->sig;
	}
	printf("\n------------------------------------------------------\n\n");
} 

/*Recibe un apuntador al primer caracter de una cadena, la modifica y genera un
codigo de forma ABC-123 donde las letras y numeros son aleatorias en base a la 
semilla generada por el tiempo, recibe como  parametro un apuntador a un arreglo
de caracteres de forma &uid[0].
*/
void  uid ( char *uid) {
    int min = 65, max = 90, i = 0;
    printf("\nRegistrando en la lista");
    for(int i = 0; i < 10; i++) 
    {
        usleep(100000); //Pausa por 100000 microsegundos, 0.1 segundos, USAMOS USLEEP porque Sleep es exclusivo de windows
        printf(".");
    } //pausa de un segundo (10 *0.1 = 1)
    
    srand(time(NULL));//se genera la semilla
    for(i; i < 3; i++) 
        uid[i] = rand() % (max - min + 1) + min; 

    uid[i] = '-';
    i++;

    for(i; i < 7; i++)
        uid[i] = rand() % ('9' - '1' + 1) + '1';
    
}
	
NODO *creaNodo (int urgencia, int operaciones) {
	NODO *nuevo;
	nuevo=(NODO *)malloc(sizeof(NODO));
    /*TENEMOS QUE LEER URGENCIA Y OPERACIONES EN EL MENU, ASI PODEMOS VOLVER A METER EL NODO SI AUN TIENE OPERACIONES*/
	if (nuevo != NULL) {
		nuevo->urgencia=urgencia;
        nuevo->operaciones=operaciones;
        uid(&nuevo->uid[0]); //se envia el apuntador al primer caracter
		nuevo->sig=NULL;
	}
	return nuevo;
}
	
NODO *insertaUrgencia(NODO *ap, int urgencia, int operaciones) {
	NODO *aux, *nuevo;	
	nuevo=creaNodo(urgencia,operaciones);
	if (nuevo == NULL) return ap;
	if (ap==NULL) {
		ap=nuevo;
	}
	else {
			aux = ap;

			/*Verifica por primera vez si la raiz (primer elemento) es mayor o menor, los ordena de manera correspondiente,
			como tambien puede ocurrir si al ultimo colocamos un elemento mas urgente debemos hacer esos cambios (se elimino la
			dependencia de que aux->sig sea NULL)*/
			if (aux->urgencia > nuevo->urgencia &&( aux == ap))
			{
				nuevo->sig = aux;
				ap = nuevo;
				return ap;				
			}
			/*Si la raiz es menor o igual al nuevo nodo, que la raiz apunte al nuevo nodo (a la derecha)
			 SOLO DEBEMOS REALIZAR ESTOS CAMBIOS CUANDO SOLO HAY UN NODO, los otros casos parecidos se manejan
			 en el while*/
			else if ( aux->urgencia <= nuevo->urgencia &&( aux == ap) && aux->sig == NULL)
			{
				aux->sig = nuevo;
				return ap;
			}	

			/*Mientras no se haya llegado al final de la lista*/
			while(aux != NULL) 
            {
				if (aux->sig != NULL) /*Solo si no se han alcanzado los ultimos dos nodos */ 
				{
					/*Busca por lugares de la forma ( menor o igual a nuevo (X) mayor a nuevo ) en X se inserta el nodo*/
					if ( aux->urgencia <= nuevo->urgencia && ( aux->sig->urgencia > nuevo->urgencia ))
					{
						nuevo->sig = aux->sig;
						aux->sig = nuevo;
						return ap;
					}
				}
				else /*Si no, significa que no encontro ninguna cola correspondiente, es decir es menos urgente que todos los anteriores
					   , lo coloca al final*/
				{
					aux->sig = nuevo;
					nuevo->sig = NULL;
					return ap;
				}
				aux=aux->sig; //se recorre al siguiente nodo
			}
		}
	return ap;
}

NODO *leerDatos(NODO *raiz) {
	int urgencia = 0, operaciones = 0;
    /*A menor valor, mayor urgencia*/
	while(urgencia<1 || urgencia>4)
    {
		printf("Seleccione su nivel de urgencia:\n1. Mucha\n2. Algo\n3. Poca\n4. Ninguna\nOpcion: ");
		fflush(stdin);
		scanf("%d", &urgencia);
		systemCLS();
	}
    /*Se permiten mas de 3 operaciones, cuando tiene mas de 3 se resta y se vuelve a formar con misma urgencia y operaciones-3*/
	while(operaciones<1)
    {
		printf("Operaciones a realizar (Minimo 1), solo se atienden 3 a la vez, te volveras a formar si existen pendientes: ");
		fflush(stdin);
		scanf("%d", &operaciones);
		systemCLS();
	}
    /*TENEMOS QUE LEER URGENCIA Y OPERACIONES EN EL MENU, ASI PODEMOS VOLVER A METER EL NODO SI AUN TIENE OPERACIONES*/
    raiz = insertaUrgencia(raiz,urgencia,operaciones);
	return raiz;
}

NODO *eliminarNodo(NODO *raiz) { //Solo borra un nodo (el primero) y actualiza la lista
	NODO *aux;
	if(raiz == NULL)
    {
		printf("\nNo hay clientes en la fila\n");
		sleep(1); //pausa de un segundo
		return raiz;
	} 
    else
    {
		aux = raiz; //se guarda la raiz
		raiz = raiz->sig; // raiz pasa a ser el siguiente
		free(aux);
        printf("\nCliente atendido\n");
		sleep(1);
	}
	return raiz;
}

NODO *atenderCliente(NODO *raiz) {
    int urgencia, operaciones; //Para hacer logs y verificaciones
    if (raiz != NULL)
    {
        operaciones = raiz->operaciones;
        urgencia = raiz->urgencia;
        if ( operaciones-3 > 0 ) 
		{
			insertaUrgencia(raiz, urgencia, operaciones - 3); //Volver a formar si tiene operaciones pendientes
			printf("\nVolviendo a formar\n");
			usleep(500000); //espera 0.5 segundos
			systemCLS();
		}
		
        /*Instrucciones para guardar logs y eliminar el nodo*/
	}
	raiz = eliminarNodo(raiz);
    return raiz;
}

int main() {
	NODO *raiz;
    char opcion;
	raiz=NULL;

    do //Ejecutar instruccion primero
    { //Instruccion compuesta
        imprimeLista(raiz);
		printf("\t\t  Menu\n1. Nuevo cliente\t2. Atender cliente\n3. Salir\nOpcion: ");
        fflush(stdin);
        opcion = getchar();
        systemCLS(); //Funcion personalizada, funciona en todos los OS
		switch(opcion){
		case '1':
			raiz = leerDatos(raiz);
			break;
			
		case '2':
			raiz= atenderCliente(raiz);
			break;
		default: //Si no se elige una opcion valida, volver a iterar
			break;
		}
		systemCLS(); //Funcion personalizada, funciona en todos los OS
    } while ( opcion != '3'); //Seguir repitiendo mientras no se haya elegido salir

	return 0;
}
