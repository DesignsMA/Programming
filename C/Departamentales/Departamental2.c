#include <stdio.h>
#include <malloc.h>
#include <time.h>
typedef struct nodo
{
    int nLista, hi,mi; //hi = horario de inicio y mi = minuto de inicio
    struct nodo *sig; //Apuntador para el próximo nodo
}NODO;

typedef struct
{
    char nombre[20];
    int mins, matricula;//Tiempo de examen y matricula
}ALUMNO;

#define n 2 //Alumnos
#define limT 60 //DURACION EXAMEN

int comprobarNombre (char nombre[]) { //Valida que el nombre o cadena este en formato Palabra Palabra
    int i, espacios = 0;
    i = 0;
    while (nombre[i] != '\0')
    {
        if (nombre[i] >= 'A' && nombre[i] <= 'Z') //se lee una mayuscula
        {
            i++; //si existe se recorre a la siguiente letra
            while (nombre[i] != ' ') //se verifica que sean minus hasta encontrar espacios
            {
                if ((nombre[i] >= 'a' && nombre[i] <= 'z'))
                    i++;
                else if ( (nombre[i] == '\0' || nombre[i] == '\n') && (espacios >=1)) return 1;
                else return 0;
            }
            if ( nombre[i] == ' ') espacios++;
            i++;
        }
        else return 0;
    }
    return 1;
}

int busqueda(ALUMNO *pAlumnos[],int val, int fin) {
    int repeticiones = 0;
    for (int i = 0; i <= fin ; i++){
        if (pAlumnos[i]->matricula == val)
                 repeticiones++;
        if (repeticiones > 1)
            return 0;
    }
    return 1;
}

void ingresarAlumno(ALUMNO *pAlumnos[], float (*pCalificaciones)[3][n]) { 
    int error, actual = 0, j = 0;
    for (int i = 0; i < n; i++)
    {
        j = 0;
        do
        {
            printf("\nIntroduzca el nombre del alumno %d en formato Nombre Apellidos\n: ", i+1);
            fflush(stdin);
            fgets(pAlumnos[i]->nombre, sizeof(char)*20, stdin);
            error = comprobarNombre(pAlumnos[i]->nombre);
            if ( !error) printf("\nEl nombre del alumno %d no tiene el formato: Nombre Apellidos (al menos un apellido)\n", i + 1);
        } while ( !error ); 
        while (pAlumnos[i]->nombre[j] != '\n' && j < 20 ) j++;
        if ( j<20 ) pAlumnos[i]->nombre[j] = ' ';
        do
        {
            printf("\nIntroduzca la matricula del alumno %d 2020XXXXXX-2024XXXXXX\n: ", i+1);
            fflush(stdin);
            scanf("%d", &pAlumnos[i]->matricula);
            error = busqueda(pAlumnos, pAlumnos[i]->matricula,actual); //Busca si existe una matricula igual
            if (!error) printf("\nYa existe una matricula con ese numero\n");
        } while ( !(pAlumnos[i]->matricula > 2019999999 && pAlumnos[i]->matricula < 2025000000) || !error );
        
        for (int j = 0; j < 2; j++) //se ingresan solo las 2 primeras calificaciones
        {
            do
            {
                printf("\nParcial %d del alumno %s\nSolo calificaciones de 5-10: ", j+1, pAlumnos[i]->nombre);
                fflush(stdin);
                scanf("%f", &(*pCalificaciones)[j][i]); //Ingreso de los datos en la posicion apuntada por pCopia
            } while ((*pCalificaciones)[j][i] < 5.0 || (*pCalificaciones)[j][i] > 10.0);
        }
        actual++;
    }
}

void imprimirListaAlumnos (ALUMNO *pAlumnos[], float (*pCalificaciones)[3][n] ) {
    int tiempo = 0;
    printf("\nNombre              No. lista\tMatricula\tTiempo\t|  1  |  2  |  3  |\n");
    
    for (int i = 0; i < n; i++)
    {
        if (pAlumnos[i]->mins > 0 && pAlumnos[i]->mins <=60) tiempo = pAlumnos[i]->mins;
        printf("\n%-20s        %d\t%d\t%d\t", pAlumnos[i]->nombre, i+1, pAlumnos[i]->matricula, tiempo );
        for (int j = 0; j < 3; j++) 
        {
            if ( (*pCalificaciones)[j][i] >= 5.0 && (*pCalificaciones)[j][i] <= 10.0)
                printf("  %.1f ",(*pCalificaciones)[j][i]);
            else printf("  -.- ");
        }
        tiempo = 0;
    }
    printf("\n");
}

NODO *creaNodo (int nLista, int hi, int mi) { //crea un nodo
	NODO *nuevo; //define el nodo
	nuevo = (NODO *)malloc(sizeof(NODO)); //Aloja memoria para el nuevo nodo, a su vez le asigna la direccion donde fue reservada
	if (nuevo != NULL) { //Si no existio error de asignación
		nuevo->nLista=nLista;
        nuevo->hi=hi;
        nuevo->mi=mi;
		nuevo->sig=NULL;
	}
	return nuevo;//Retorna nodo
}

NODO *eliminaNodo (NODO *raiz, int nLista) { 
    NODO *aux, *ant;
    if ( raiz != NULL ) {
        aux = raiz;
        if (raiz->nLista == nLista) {
            raiz=raiz->sig;
            free(aux);
        }
        else {
            aux = raiz;
            ant = raiz;
            while ( aux != NULL ) {
                if ( aux->nLista == nLista ) break;
                ant = aux;
                aux = aux->sig;
            }
            if ( aux == NULL ) return NULL;
            ant->sig=aux->sig;
            free(aux);
        }
    }
    return raiz;
}

int buscar (NODO *raiz, int nLista, int opc) { 
    NODO *copia;
    copia = raiz;
    while (copia != NULL)
    {
        if (copia->nLista == nLista) {
            if (opc == 1)
                return copia->hi;
            else if (opc == 2)
                return copia->mi;
            else return 0;
        }
        copia = copia ->sig;
    }
    return 0;
}

NODO *finalizar (NODO *raiz, float (*pCalificaciones)[3][n] ) { 
    NODO *ant;
    while (raiz != NULL)
    {
        ant = raiz;
        (*pCalificaciones)[2][raiz->nLista] = 5;
        raiz = raiz ->sig;
        free(ant);

    }
    return raiz;
}

NODO *insertaAlInicio(NODO *ap, int nLista, int hi, int mi) { //recibe la lista y los datos para insertar el nuevo nodo
	NODO *aux, *nuevo;
	
	nuevo=creaNodo(nLista,hi,mi); //Crea el nodo
	if (nuevo == NULL) return ap; //Si el nodo fue creado erroneamente
	aux=ap; //se almacena temporalmente el nodo original
	ap=nuevo; // se sustituye el primero con el nuevo (direccion de memoria)
	nuevo->sig=aux; //el nuevo apunta al nodo original
	return ap; //se retorna el nuevo nodo insertado que apunta al nodo original
}
/* Raiz = NULL | NUEVO1 = 200 => RAIZ = 200 -> NULL | NUEVO2 = 420 => RAIZ = 420 -> 200 -> NULL | */

NODO *inicializarExamen (int exhI, int exmI, int exhF, int exmF, NODO *raiz, int nLista)  {
    int hi, mi;
    do
    {
        printf("\nSe inician examenes a partir de las %02d:%02d\nA que hora comenzo el examen el alumno\nFormato (H:M): ", exhI, exmI);
        fflush(stdin);
        scanf("%d:%d", &hi, &mi);
    } while ( hi < exhI || ( hi == exhI && mi < exmI ) || (hi > exhF || ( hi == exhF && mi > exmF )) || mi > 59 || mi < 0); //mientras hora no valida
     return insertaAlInicio(raiz,nLista,hi,mi);
}

NODO *finalizarExamen(int nLista, NODO *raiz, ALUMNO *pAlumnos[n], int exhF, int exmF, float (*pCalificaciones)[3][n] ) {
    int hf, mf, hi, mi;
    float calf;
    hi = buscar(raiz, nLista, 1);
    mi = buscar(raiz, nLista, 2);
    do
    {
        printf("\nA que hora termino el examen el alumno Formato (H:M)\nSi termino despues de  las %02d:%02d, no sera registrado: ", exhF, exmF);
        fflush(stdin);
        scanf("%d:%d", &hf, &mf);
        if ( (hf > exhF || ( hf == exhF && mf > exmF ))) return raiz;
    } while ( hf < hi || ( hf == hi && mf < mi ) || ( mf > 59 || mf < 0 ) ); //mientras hora no valida
    do
    {
        printf("\nEscriba la calificacion del 3er parcial (5-10)\n: ");
        fflush(stdin);
        scanf("%f", &calf);
    } while ( calf < 5.0 || calf > 10.0);
    
    (*pCalificaciones)[2][nLista] = calf;
    pAlumnos[nLista]->mins = (hf-hi)*60 +(mf-mi);
    return eliminaNodo(raiz, nLista);
}

int main() {
    int exhI, exmI, opc, opc2, exhF, exmF, ocupados[n]; 
    float calificaciones[3][n], (*pCalificaciones)[3][n] = &calificaciones;  //3 calificaciones por alumno, de n alumnos fila, apunta a TODO el arreglo bidimensional
    ALUMNO *pAlumnos[n];
    NODO *entradas;
    
	time_t rawtime, endtime; //apuntador al tiempo
    struct tm *timeinfo; //struct de tiempo
    entradas = NULL; //raiz en null
    
    for (int i = 0; i < n; i++) 
    {
        pAlumnos[i] = (ALUMNO*) malloc(sizeof(ALUMNO));
        ocupados[i] = i;
    }

    ingresarAlumno(pAlumnos, pCalificaciones);
    
    time(&rawtime); //actualiza el tiempo
    timeinfo = localtime(&rawtime); //llena el struct
    endtime =  (time_t) rawtime + limT*60;
    exhI = timeinfo->tm_hour;
   	exmI = timeinfo->tm_min;
    timeinfo = localtime(&endtime); //llena el struct
    exhF = timeinfo->tm_hour;
    exmF = timeinfo->tm_min;
    printf("\n\n\tSe inicio el examen a las %02d:%02d, finaliza a las %02d:%02d", exhI, exmI, exhF, exmF);
    do
    {
        imprimirListaAlumnos(pAlumnos, pCalificaciones);
        printf("\n1. Inicializar un examen\t2.Finalizar un examen\t-1. Salir\n: ");
        fflush(stdin);
        scanf("%d", &opc);
        switch (opc)
        {
            case 1:
                printf("\nIngrese el numero de lista del alumno\n: ");
                fflush(stdin);
                scanf("%d", &opc2);
                if ( ocupados[opc2-1] == opc2-1) {
                    entradas = inicializarExamen(exhI,exmI,exhF,exmF,entradas,opc2-1);
                    ocupados[opc2-1] = -1;
                }
                else printf("\nEl alumno esta en examen o ya ha terminado, o bien no existe\n");
               break;
            
            case 2:
                printf("\nIngrese el numero de lista del alumno\n: ");
                fflush(stdin);
                scanf("%d", &opc2);
                if ( ocupados[opc2-1] == -1) {
                    entradas = finalizarExamen(opc2-1, entradas, pAlumnos, exhF, exmF, pCalificaciones);
                    ocupados[opc2-1] = -2;
                }
                else printf("\nEl alumno ya finalizo, o aun no ha comenzado, o bien no existe\n");
                break;

            default: break;
        }
    } while (opc != -1);
    entradas = finalizar(entradas, pCalificaciones);
    imprimirListaAlumnos(pAlumnos, pCalificaciones);
    do
    {
        printf("\nIntroduce 1 para salir\n: ");
        scanf("%d", &opc);
    } while ( opc != 1);
    
}
