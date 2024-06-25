
#include <stdio.h>
#define APERTURA 8
#define CIERRE 20
#define limP 8

typedef struct 
{
 int hi,mi,hf,mf;
}Horario;

typedef struct 
{
    Horario horario;
    char nombre[20];
}Pelicula;

typedef struct 
{
 Pelicula peliculas[limP];
}Funcion;

typedef struct
{
    Funcion funcion;
    int i, pos[limP];
}Salida;

int comprobacion(Pelicula peliculas[], int i, int pelis) {
    if ( pelis > 0) 
    { //Si Hay más de una pelicula
        for ( int j = 0; j < pelis; j++) //Para todo el arreglo
        {
            if (j != i)
            {           // Verifica si el horario de la pelicula i se encuentra antes del inicio de la pelicula j
                if (!( peliculas[i].horario.hf < peliculas[j].horario.hi || (peliculas[i].horario.hf == peliculas[j].horario.hi && peliculas[i].horario.mf < peliculas[j].horario.mi) ||
                        // Verifica si el horario de la pelicula i se encuentra despues del final de la pelicula j
                     ( peliculas[i].horario.hi > peliculas[j].horario.hf || (peliculas[i].horario.hi == peliculas[j].horario.hf && peliculas[i].horario.mi > peliculas[j].horario.mf))  ))
                {
                    printf("\nLos horarios de la pelicula introducida se superponen a %s\n", peliculas[j].nombre);
                    return 0;
                }
            }
        }
    }                                                
    return 1;
}

int validarHoras(Pelicula pelicula) {
    int duracion = (pelicula.horario.hf-pelicula.horario.hi)*60 +(pelicula.horario.mf-pelicula.horario.mi);      
    if ( (pelicula.horario.hi >= APERTURA && pelicula.horario.hi <= CIERRE && pelicula.horario.mi  >=0 && pelicula.horario.mi <=59 &&
          pelicula.horario.hf >= APERTURA && pelicula.horario.hf <= CIERRE && pelicula.horario.mf >=0 && pelicula.horario.mf<=59 && duracion > 1 ) )
          return 1;

    printf("Error en horarios, no puedes colocar minutos mayores a 59 o menores a 0 ni horas fuera de las de trabajo.\n");
    return 0;

}

int imprimirCartelera(Funcion funcion, int n, int pos[]) {
    printf("- - - - - - - - - - - - - - - -CARTELERA- - - - - - - - - - - - - - - -\n");
    for (int i = 0; i <= n; i++)
    {
        printf("%d. %-30s\t %02d:%02d \t %02d:%02d\n", i+1, funcion.peliculas[pos[i]].nombre, funcion.peliculas[pos[i]].horario.hi, 
                funcion.peliculas[pos[i]].horario.mi, funcion.peliculas[pos[i]].horario.hf, funcion.peliculas[pos[i]].horario.mf); 
                //El formato 02 de manera parecida a %0.2 en lugar de 2 decimales //lo imprime con 2 enteros
    }
    printf("- - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - -\n");
}

Salida cartelera(Funcion funcion) {
	int i = 0, opc, pos[limP]= {0,1,2,3,4,5,6,7};
    Salida out,in;
    do
    {
        printf("\n1. Ingresar Pelicula\n2. Visualizar peliculas\n-1. Salir\n");
        scanf("%d", &opc);
        switch (opc)
        {

        case 1:
        if(i < limP) 
        {
            printf("\nNombre de la pelicula %d: ", i+1);
            fflush(stdin);
            scanf("%s",funcion.peliculas[i].nombre);
            printf("\n\t\tHoy abrimos a las %d:00 y Cerramos a las %d:00", APERTURA, CIERRE);
	        do 
            {   
	        	printf("\nHora inicial (formato H:M): ");
	        	scanf("%d:%d",&funcion.peliculas[i].horario.hi, &funcion.peliculas[i].horario.mi);
	        	printf("\nHora final (formato H:M): ");
	        	scanf("%d:%d",&funcion.peliculas[i].horario.hf, &funcion.peliculas[i].horario.mf);
                printf("\n");
	        } while ( !validarHoras(funcion.peliculas[i]) || !comprobacion(funcion.peliculas, i, i) );
        i++;
        } 
        else
            printf("\nSolo %d peliculas por día permitidas.\n", limP);
        break;

        case 2: 
        imprimirCartelera(funcion, i-1,pos);
        break;

        default:
            break;
        }
        
    } while ( opc != -1);

    out.funcion = funcion;
    out.i = i-1;
	return(out);
}

Salida ordenamientoInsercion(Pelicula peliculas[], int n)
{
    Pelicula actual;
    Salida out;
    int i, j, posI;

    for ( int m = 0; m <= n; m++) //Se inicializan los indices de posiciones
          out.pos[m] = m;
    
    for (i = 1; i <= n; i++) 
    { 
        actual = peliculas[out.pos[i]]; 
        posI = out.pos[i];
        j = i - 1;

        while (j >= 0 && ( peliculas[out.pos[j]].horario.hi > actual.horario.hi || ( (peliculas[out.pos[j]].horario.hi == actual.horario.hi) && (peliculas[out.pos[j]].horario.mi > actual.horario.mi) ) ) )
        {
            out.pos[j + 1] = out.pos[j];
            j -= 1;
        }
        out.pos[j + 1] = posI;
    }

    return out;
}

//       Peliculas, Horario a buscar, Indice global, Vector de posiciones
int busquedaBinaria(Pelicula peliculas[], Horario busqueda, int i, int pos[]) { 
    int inicio = 0, fin = i, mitad = (inicio + fin)/2, intentos = 0;
    //SI PELICULA DE EN MEDIO ES IGUAL AL HORARIO QUE SE BUSCA
    if ( peliculas[ pos[mitad] ].horario.hi == busqueda.hi && peliculas[ pos[mitad] ].horario.mi == busqueda.mi )
        return mitad;

    while ( !(peliculas[ pos[mitad] ].horario.hi == busqueda.hi && peliculas[ pos[mitad] ].horario.mi == busqueda.mi) && inicio <= fin ) //MIENTRAS NO SE HAYA ENCONTRADO LA PELICULA O NO SE ENCUENTRE
    {
        if ( busqueda.hi < peliculas[ pos[mitad] ].horario.hi || busqueda.hi == peliculas[ pos[mitad] ].horario.hi && busqueda.mi < peliculas[ pos[mitad] ].horario.mi ) // SI EL HORARIO DE BUSQUEDA SE ENCUENTRA A LA IZQUIERDA DE LOS HORARIOS
        {
            fin = mitad -1; //SE COLOCA EL FIN ANTES DE LA MITAD DEL ARREGLO
        }
        else
        {
            inicio = mitad+1; // SE COLOCA EL INCIIO DESPUES DE LA MITAD DEL ARREGLO
        }
        mitad = (inicio + fin)/2;
        intentos++;          //AUMENTAMOS INTENTOS PARA EVITAR BUCLES INFINITOS
    }
    

    if ( inicio <= fin)
       return mitad;
    else
       return -1;
    
}

int main() {
    Funcion funcion;     
    Salida entrada = cartelera(funcion), pos; //ACTUALIZACIÓN DE DATOS
    Horario busqueda;
	int i = entrada.i ,opc, r;
    funcion = entrada.funcion; 

    pos = ordenamientoInsercion(funcion.peliculas,i);   //ORDENAMIENTO POR HORA
    
    printf("\t\t|Bienvenido a cineFCC|\n");
    imprimirCartelera(funcion,i,pos.pos);

    do {
        printf("\n-1. Salir\t0.Buscar por horario\n");
        fflush(stdin);
        scanf("%d", &opc);
        switch (opc)
        {
        case 0: 
            printf("\nHora inicial de la pelicula a buscar (formato H:M): ");
            scanf("%d:%d",&busqueda.hi, &busqueda.mi);
            r = busquedaBinaria(funcion.peliculas, busqueda, i, pos.pos);
            if (  r >= 0 ) 
            {
                printf("\n\tSe encontro: %s a las %02d:%02d\n", funcion.peliculas[pos.pos[r]].nombre, funcion.peliculas[pos.pos[r]].horario.hi, funcion.peliculas[pos.pos[r]].horario.mi );
            }
            else
                printf("\nNo hay peliculas a proyectar en esa hora.\n");
        
        default:
        break;
        }

    } while (opc != -1);
    
}
