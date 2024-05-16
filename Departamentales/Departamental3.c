#include <time.h> //generar semilla en base a tiempo
#include <stdio.h>
#include <stdlib.h> // funciones rand
#include <malloc.h> 
#include <string.h>
#include <unistd.h> //Para usar sleep(), usleep() (FUNCIONA EN LINUX, MAC, ANDROID, WINDOWS)
typedef struct NODO {
	char uid[8], unico; //ABC-789\0
	int urgencia, operaciones;
	struct NODO *sig;
}NODO;

typedef struct SALIDA //Estructura de salida
{
	char id[11];
}SALIDA;

/*https://www.upgrad.com/tutorials/software-engineering/c-tutorial/macros-in-c/*/
/*Las directivas precedidas por # pertenecen al conjunto de intrucciones de preprocesador, se ejecutan
antes de la compilacion de un programa,*/

void systemCLS() {
#if defined( _WIN32) //Antes de la compilacion verifica si la constante WIN32 esta definida en el sistema
	system("cls"); //Si lo esta ejecutara esta seccion de codigo (no necesita libreria)
#else //Si no, usara clear (linux y mac, android)
	system("clear"); //Si encuentra la variable, antes de la compilacion excluira esta seccion de codigo
	//y viceversa
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
de caracteres de forma &uid[0]. */
void  uidGen(char *uid) {
	int i, j;
    printf("\nRegistrando en la lista");
    for(i = 0; i < 10; i++) {
        usleep(25000); //Pausa por 0.25 segundos, USAMOS USLEEP porque Sleep es exclusivo de windows
        printf(".");
    } 
    srand(time(NULL));//se genera la semilla, tenemos que pausar 1 segundo para que la semilla sea diferente
    for(j = 0; j < 3; j++) uid[j] = (char)( rand()%('Z' - 'A' + 1) + 'A');//genera ABC 
	uid[j] = '-';//ABC-
    j++;
    for(j; j < 7; j++) uid[j] = (char)( rand()%('9' - '1' + 1) + '1');//Limites para generar digitos entre 1-9 ABC-123
    uid[j] = '\0';//ABC-123\0
}

NODO *creaNodo (int urgencia, int operaciones, char uid[8], char unico) {
	NODO *nuevo;
	nuevo=(NODO *)malloc(sizeof(NODO));
	if (nuevo != NULL){
		nuevo->urgencia=urgencia;
		nuevo->operaciones=operaciones;
		nuevo->unico = unico; //indica si es unico o no S/N
		strcpy(nuevo->uid, uid);
		nuevo->sig=NULL;
	}
	return nuevo;
}

NODO *insertaUrgencia(NODO *ap, int urgencia, int operaciones, char uid[8], char unico) {
	NODO *aux, *nuevo;	
	nuevo=creaNodo(urgencia,operaciones, uid, unico);
	if (nuevo == NULL) return ap;
	if (ap==NULL) ap=nuevo;
	else {
		aux = ap;
		/*Verifica por primera vez si la raiz (primer elemento) es mayor o menor, los ordena de manera correspondiente,
		como tambien puede ocurrir si al ultimo colocamos un elemento mas urgente debemos hacer esos cambios (se elimino la
		dependencia de que aux->sig sea NULL)*/
		if (aux->urgencia > nuevo->urgencia &&( aux == ap)){
			nuevo->sig = aux;
			ap = nuevo;
			return ap;				
		}
		/*Si la raiz es menor o igual al nuevo nodo, que la raiz apunte al nuevo nodo (a la derecha)
		SOLO DEBEMOS REALIZAR ESTOS CAMBIOS CUANDO SOLO HAY UN NODO, los otros casos parecidos se manejan
		en el while*/
		else if ( aux->urgencia <= nuevo->urgencia &&( aux == ap) && aux->sig == NULL){
			aux->sig = nuevo;
			return ap;
		}	
		/*Mientras no se haya llegado al final de la lista*/
		while(aux != NULL){
			if (aux->sig != NULL){ /*Solo si no se han alcanzado los ultimos dos nodos */ 
				/*Busca por lugares de la forma ( menor o igual a nuevo (X) mayor a nuevo ) en X se inserta el nodo*/
				if ( aux->urgencia <= nuevo->urgencia && ( aux->sig->urgencia > nuevo->urgencia )){
					nuevo->sig = aux->sig;
					aux->sig = nuevo;
					return ap;
				}
			}
			else{
				aux->sig = nuevo; //Si no, significa que no encontro ninguna cola correspondiente, es decir 
				nuevo->sig = NULL; //es menos urgente que todos los anteriores , lo coloca al final
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
	while(urgencia<1){
		printf("Seleccione su nivel de urgencia:\n1. Mucha\n2. Algo\n3. Poca\n4 para arriba ninguna\nOpcion: ");
		fflush(stdin);
		scanf("%d", &urgencia);
		systemCLS();
	}
	/*Se permiten mas de 3 operaciones, cuando tiene mas de 3 se resta y se vuelve a formar con misma urgencia y operaciones-3*/
	while(operaciones<1 ){
		printf("Operaciones a realizar (Minimo 1), solo se atienden 3 a la vez, te volveras a formar si existen pendientes: ");
		fflush(stdin);
		scanf("%d", &operaciones);
		systemCLS();
	}
	uidGen(&uid[0]); //se envia la direccion al primer caracter
	raiz = insertaUrgencia(raiz,urgencia,operaciones, uid, 'S');
	return raiz;
}
NODO *eliminarNodo(NODO *raiz) {
	NODO *aux;
	aux = raiz; //se guarda la raiz
	raiz = raiz->sig; // raiz pasa a ser el siguiente
	free(aux);
	return raiz;
}

void generarLogTemp(NODO *raiz){
	FILE *log;
	log = fopen("temp.txt", "a+"); //abre o crea temp.txt en modo append
	fseek(log, 0, SEEK_END); //movemos el apuntador hasta el final
	if ( ftell(log) == 0) fprintf(log, "\tREPORTE DE CLIENTES\n\nUrgencia | Operaciones | ID\n\n"); //si el apuntador es cero (el archivo aun no tiene nada) colocamos la cabecera
	fprintf(log, "%03d\t   %03d\t	 %s\n", raiz->urgencia, raiz->operaciones, raiz->uid); //escribimos informacion de un cliente atendido (se coloca hasta el final)      
    fclose(log);
}

/*Funcion para realizar las operaciones al atender un cliente, (guarda datos y manda a eliminar el nodo)
Si el cliente tiene operaciones pendientes lo vuelve a formar*/
NODO *atenderCliente(NODO *raiz) {
	int urgencia, operaciones; //Para hacer logs y verificaciones
	char uid[8];
	if (raiz != NULL){
		operaciones = raiz->operaciones; //guardamos los datos para despues hacer logs
		urgencia = raiz->urgencia;
		strcpy(uid, raiz->uid); //guardar uid

		if (raiz->unico == 'S') generarLogTemp(raiz); //Si es la primera vez que pasa, colocamos en log

		if ( operaciones-3 > 0 ) //Si las operaciones exceden las 3
		{
			printf("\nVolviendo a formar\n");
			raiz = eliminarNodo(raiz);
			raiz = insertaUrgencia(raiz, urgencia, operaciones - 3, uid, 'N'); //Volver a formar si tiene operaciones pendientes, indicamos que ya paso
		}
		else raiz = eliminarNodo(raiz);
		
		printf("\nCliente atendido\n");
		usleep(500000); //espera 0.5 segundos
		systemCLS();
	} else {
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
	tmp = localtime(&t); //transformamos a tiempo local y almacenamos como struct en tmp
	strftime(salida.id, sizeof(salida.id), "%d%m%y%H%M", tmp); //formato diamesaniohoraminuto, https://www.geeksforgeeks.org/strftime-function-in-c/
	return salida;//retornamos el struct para acceder a la cadena
}

void guardarSesion(NODO *raiz) {
	FILE *sesion;
	char fileID[23];
	snprintf(fileID, sizeof(fileID), "clientes%s.bin", tiempoID().id); //generando 	//clientesdiamesanioohoraminutos.bin 23
	sesion = fopen(fileID, "wb"); //Abrir archivo en modo escritura

	if (sesion == NULL) printf("Error abriendo el archivo");
	else {
		while (raiz != NULL){ //Mientras no se llegue al final de la lista
			fwrite(&raiz->urgencia, sizeof(raiz->urgencia), 1, sesion); //Escribir bloques de memoria en el binario
			fwrite(&raiz->operaciones, sizeof(raiz->operaciones), 1, sesion);
			fwrite(&raiz->uid, sizeof(char)*7, 1, sesion);
			fwrite(&raiz->unico, sizeof(char), 1, sesion);
			raiz = raiz -> sig;
		}
	}

	fclose(sesion);//se cierra el log de la sesion
	sesion = fopen("ultimaSesion.bin", "wb"); //se almacena el nombre para acceder despues
	fwrite(fileID, sizeof(char)*23, 1, sesion);//escribimos el nombre
	fclose(sesion);
}

NODO *restablecerSesion(NODO *raiz) {
	FILE *sesion;
	int urgencia = 0, operaciones; //Lugares donde se almacenan los  bloques de memoria recuperados de un bin
	char uids[8], nombre[23], opcion, unico;
	
	printf("1. Abrir ultimo archivo\n2. Ingresar nombre especifico (revisar carpeta)\nOpcion: ");
	fflush(stdin);
	scanf("%c", &opcion);
	
	if(opcion=='1' || opcion !='2'){
		if ((sesion=fopen("ultimaSesion.bin", "rb"))!=NULL) {
			fread(nombre, sizeof(char)*23, 1, sesion); //lee la sesion anterior
			fclose(sesion);
		}
	} else{
		printf("Nombre (formato clientesdiamesaniohoraminuto): ");
		fflush(stdin);
		scanf("%s", nombre);
		strcat(nombre, ".bin");
	}	
	
	sesion = fopen(nombre,"rb"); //abrimos el archivo con el nombre introducido
	if (sesion == NULL) return raiz; 
	else do{
			urgencia = 0;
			fread(&urgencia, sizeof(urgencia), 1, sesion); //No actualizara el bloque de memoria si no lee nada
			fread(&operaciones, sizeof(operaciones), 1, sesion);
			fread(&uids, sizeof(char)*7, 1, sesion);
			fread(&unico, sizeof(char), 1, sesion);
			raiz = insertaUrgencia(raiz, urgencia, operaciones, uids, unico);

	} while ( urgencia != 0);

	fclose(sesion);
	return raiz;
}

void generarReporte() {
	char logs[22], datos[50];
	FILE *log;
	snprintf(logs, sizeof(logs), "reporte%s.txt", tiempoID().id); //creamos el id del reporte (igual que el de clientes)
	rename("temp.txt", logs); //renombramos el log temporal a su nombre final
	log = fopen(logs, "r"); //imprimimos en pantalla el log
	while (fgets(datos, 50, log) != NULL) printf("%s", datos);
	fclose(log);
}

int main() {
	NODO *raiz;
	char opcion;
	raiz=NULL;
	raiz = restablecerSesion(raiz);
	
	do{
		imprimeLista(raiz);
		printf("\tMenu\n1. Nuevo cliente\n2. Atender cliente\n3. Salir\nOpcion: ");
		fflush(stdin);
		opcion = (char) getchar();
		systemCLS(); //Funcion personalizada, funciona en todos los SO
		switch(opcion){
		case '1': raiz = leerDatos(raiz);
			break;
			
		case '2': raiz= atenderCliente(raiz);
			break;
		default: break;
		}
		systemCLS(); //Funcion personalizada, funciona en todos los SO
	} while ( opcion != '3'); //Seguir repitiendo mientras no se haya elegido salir
	
	guardarSesion(raiz); //Guardamos los nodos existentes en el binario
	if ( raiz == NULL) generarReporte(); // si se llego al final generamos reporte
	else while (raiz!=NULL) raiz = eliminarNodo(raiz); //si no liberamos memoria

	return 0;
}
	
