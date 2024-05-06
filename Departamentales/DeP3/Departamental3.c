#include <time.h> //generar semilla en base a tiempo
#include <stdio.h>
#include <stdlib.h> // funciones rand
#include <malloc.h>
#include <string.h>
#include <unistd.h> //Para usar sleep(), usleep() (FUNCIONA EN LINUX, MAC Y ANDROID, WINDOWS)
typedef struct NODO {
	char uid[8]; //ABC-789\0
	int urgencia, operaciones;
	struct NODO *sig;
}NODO;
typedef struct SALIDA //Estructura de salida
{
	char id[11];
}SALIDA;

void systemCLS() {
    #if defined( _WIN32) //Si es windows
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
void  uidGen(char *uid) {
    int min = 65, max = 90, i = 0;//limites para generar letras entre A-Z
    printf("\nRegistrando en la lista");
    for(int i = 0; i < 10; i++) 
    {
        usleep(3333); //Pausa por 100000 microsegundos, 0.1 segundos, USAMOS USLEEP porque Sleep es exclusivo de windows
        printf(".");
    } //pausa de un segundo (10 *0.1 = 1)
    srand(time(NULL));//se genera la semilla, tenemos que pausar 1 segundo para que la semilla sea diferente
    for(i; i < 3; i++) 
        uid[i] = rand() % (max - min + 1) + min; 

    uid[i] = '-';
    i++;

    for(i; i < 7; i++)
        uid[i] = rand() % ('9' - '1' + 1) + '1';//Limites para generar digitos entre 1-9
    uid[i] = '\0';
}
	
NODO *creaNodo (int urgencia, int operaciones, char uid[8]) {
	NODO *nuevo;
	nuevo=(NODO *)malloc(sizeof(NODO));
	if (nuevo != NULL) {
		nuevo->urgencia=urgencia;
        nuevo->operaciones=operaciones;
		strcpy(nuevo->uid, uid);
		nuevo->sig=NULL;
	}
	return nuevo;
}
	
NODO *insertaUrgencia(NODO *ap, int urgencia, int operaciones, char uid[8]) {
	NODO *aux, *nuevo;	
	nuevo=creaNodo(urgencia,operaciones, uid);
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
/*Funcion que lee los datos de un cliente, con esos datos manda a introducir en la lista y la actualiza*/
NODO *leerDatos(NODO *raiz) {
	int urgencia = 0, operaciones = 0;
	char uid[8];
    /*A menor valor, mayor urgencia*/
	while(urgencia<1)
    {
		printf("Seleccione su nivel de urgencia:\n1. Mucha\n2. Algo\n3. Poca\n4 para arriba ninguna\nOpcion: ");
		fflush(stdin);
		scanf("%d", &urgencia);
		systemCLS();
	}
    /*Se permiten mas de 3 operaciones, cuando tiene mas de 3 se resta y se vuelve a formar con misma urgencia y operaciones-3*/
	while(operaciones<1 )
    {
		printf("Operaciones a realizar (Minimo 1), solo se atienden 3 a la vez, te volveras a formar si existen pendientes: ");
		fflush(stdin);
		scanf("%d", &operaciones);
		systemCLS();
	}
	uidGen(&uid[0]); //se envia el apuntador al primer caracter
    raiz = insertaUrgencia(raiz,urgencia,operaciones, uid);
	return raiz;
}
/*Funcion que tal cual dice su nombre, solo borra un nodo y actualiza la lista
 (el primer nodo en la lista)*/
NODO *eliminarNodo(NODO *raiz) {
	NODO *aux;
	aux = raiz; //se guarda la raiz
	raiz = raiz->sig; // raiz pasa a ser el siguiente
	free(aux);
	return raiz;
}
/*Funcion para realizar las operaciones al atender un cliente, (guarda datos y manda a eliminar el nodo)
  Si el cliente tiene operaciones pendientes lo vuelve a formar*/
NODO *atenderCliente(NODO *raiz) {
    int urgencia, operaciones; //Para hacer logs y verificaciones
	char uid[8];
    if (raiz != NULL)
    {
        operaciones = raiz->operaciones; //guardamos los datos para despues hacer logs
        urgencia = raiz->urgencia;
		strcpy(uid, raiz->uid); //guardar uid
        if ( operaciones-3 > 0 ) //Si las operaciones exceden las 3
		{
			printf("\nVolviendo a formar\n");

			raiz = eliminarNodo(raiz);
			raiz = insertaUrgencia(raiz, urgencia, operaciones - 3, uid); //Volver a formar si tiene operaciones pendientes
		}
		else raiz = eliminarNodo(raiz);
        /*Instrucciones para guardar logs*/
		printf("\nCliente atendido\n");
		usleep(500000); //espera 0.5 segundos
		systemCLS();


	} else if(raiz == NULL)
    {
		printf("\nNo hay clientes en la fila\n");
		sleep(1); //pausa de un segundo
	} 
    return raiz;
}

SALIDA tiempoID() {
	SALIDA salida;
	struct tm *tmp ; //structura con datos del  tiempo (separados)
	time_t t; //variable donde el tiempo se almacena en entero
	time(&t); //obtenemos el tiempo actual
	tmp = localtime(&t); //transformamos a tiempo local y almacenamos separado en tmp
	strftime(salida.id, sizeof(salida.id), "%d%m%y%H%M", tmp); //formato diamesaniohoraminuto
	return salida;
}
void guardarSesion(NODO *raiz) {
	FILE *sesion;
	char fileID[23];
	snprintf(fileID, sizeof(fileID), "clientes%s.bin", tiempoID().id); //generando 	//clientesdiamesañohoraminutos.bin 23
	sesion = fopen(fileID, "wb"); //Abrir archivo en modo escritura
	if (sesion == NULL) printf("Error abriendo el archivo");
	else
	{
		while (raiz != NULL)
		{
			fwrite(&raiz->urgencia, sizeof(raiz->urgencia), 1, sesion);
			fwrite(&raiz->operaciones, sizeof(raiz->operaciones), 1, sesion);
			fwrite(&raiz->uid, sizeof(char)*8, 1, sesion);
			raiz = raiz -> sig;
		}
	}
	fclose(sesion);
}

NODO *restablecerSesion(NODO *raiz) {
	FILE *sesion;
	int urgencia = 0, operaciones; //Lugares donde se almacenan los  bloques de memoria recuperados de un bin
	char uids[8];
	sesion = fopen("lastSession.bin", "rb"); //Abrir archivo en modo lectura    
	if (sesion == NULL) return raiz; 
	else 
	{
		do
		{
			fread(&urgencia, sizeof(urgencia), 1, sesion); //No actualizara el bloque de memoria si no lee nada
			fread(&operaciones, sizeof(operaciones), 1, sesion);
			fread(&uids, sizeof(char)*8, 1, sesion);
			if ( urgencia == 0 ) break;
			raiz = insertaUrgencia(raiz, urgencia, operaciones, uids);
			urgencia = 0;
		} while (1);
	}
	fclose(sesion);
	return raiz;
}

int main() {
	NODO *raiz;
    char opcion;
	raiz=NULL;
	
	raiz = restablecerSesion(raiz);

    do //Ejecutar instruccion primero
    { //Instruccion compuesta
        imprimeLista(raiz);
		printf("\tMenu\n1. Nuevo cliente\n2. Atender cliente\n3. Salir\nOpcion: ");
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

	guardarSesion(raiz);
	while (raiz!=NULL)
		raiz = eliminarNodo(raiz);
	

	return 0;
}
