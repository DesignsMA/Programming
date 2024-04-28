#include <stdio.h>
#include <malloc.h>
#include <string.h>

typedef struct 
{
    int d,m,a;
}Fecha;
//Cada miembro de una enumeracion tiene un numero, miembro 1 = 0, miembro n = n-1
enum meses {ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE};

void comprobarFecha(Fecha *pf) {
    int *pd,*pm,*pa, limFebrero; //apuntadores para cambios especificos
    pd = (*pf).d, pm = (*pf).m, pa = (*pf).a; //asignando direcciones

    *pa = *pa >=1960 && *pa <= 2024? *pa : 1960; //Checa si el anio esta entre 1960-2024
    
    if ( !(*pd > 0 && *pd <= 31) ) // Si el dia no es valido
        *pd = 1; //asignar 1

    switch ((enum meses) *pm-1) // CAST para que C interprete el número como una constante (mes)
    {
        case ENERO: 
                    case MARZO: case ABRIL: //Si es un mes correcto
                    case MAYO: case JUNIO: case JULIO: 
                    case AGOSTO: case SEPTIEMBRE: case OCTUBRE:
                    case NOVIEMBRE: case DICIEMBRE:
                    break;
        
        case FEBRERO: 
                    limFebrero = *pa % 4 == 0 ? 29 : 28; //Operador ternario que verifica si el anio es bisiesto (1960-2024)
                    if ( !(*pd > 0 && *pd <= limFebrero) ) // Si el dia no es valido
                        *pd = 1; //asignar 1
                    break;
        default:
                    *pm = 1; //Si el mes no existe, asignar 1
                    break;
    }
}

void convertirFecha(Fecha f) {
    //Arreglo de punteros a caracter, cada puntero apunta a la dirección del primer caracter de cada cadena
    //https://www.geeksforgeeks.org/array-of-pointers-in-c/
    char *meses[] = { "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre" }; 
    printf("\n%02d de %s de %d", f.d, meses[f.m-1], f.a);
}

int main () {
    Fecha f, *pf;
    pf =  (Fecha*) malloc(sizeof(Fecha)); //Reserva memoria para el apuntador a fecha
    pf = &f; //Asigna la direccion de fecha al puntero
   
    do
    {
        printf("\nIngrese el dia, mes y anio en el formato: d/m/a: ");
        fflush(stdin);
        /*se realiza un cast de apuntador para que C sepa que se coloca una direccion de memoria
        un struct reserva memoria por secciones dependiendo del tipo de dato
        su direccion inicial apunta al primer elemento, por ello sumamos el tamanio del tipo de dato
        entero (4 bytes) para acceder correctamente al siguiente elemento, primero se accede
        a la direccion de memoria de dia, despues mes, despues anio*/
        scanf("%d/%d/%d", pf,pf+4,pf+8); 
        comprobarFecha(pf);
        convertirFecha(f);
        printf("\n\nPara salir ingrese 's': ");
        fflush(stdin);
    } while ( getchar() != 's');

}
