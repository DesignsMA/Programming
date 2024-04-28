

#include <stdio.h>
#include <stdlib.h>

#define APERTURA 8
#define CIERRE 20
#define limP 8

typedef struct 
{                               //2 BLOQUES DE 8 bits con 13 duplicados (cols)
    unsigned char butacas[2][13]; //13 Col, 16 filas (16 bits)
}Sala;


typedef struct 
{
 int hi,mi,hf,mf;
}Horario;

typedef struct 
{
    Horario horario;
    Sala sala;
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

//FUNCIONES PARA LA LECTURA DE LA CARTELERA
int comprobacion(Pelicula peliculas[], int i, int pelis) {
    if ( pelis > 0) {
        for ( int j = 0; j < pelis; j++)
        {
            if (j != i)
            {
                if (!(  peliculas[i].horario.hf < peliculas[j].horario.hi ||
                        (peliculas[i].horario.hf == peliculas[j].horario.hi // Verifica si el horario de la pelicula i se encuentra antes del inicio de la pelicula j
                     && peliculas[i].horario.mf < peliculas[j].horario.mi) 
                     || (
                     peliculas[i].horario.hi > peliculas[j].horario.hf ||
                     (peliculas[i].horario.hi == peliculas[j].horario.hf // Verifica si el horario de la pelicula i se encuentra despues del final de la pelicula j
                     && peliculas[i].horario.mi > peliculas[j].horario.mf))  )) {

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
                    
    if ( (pelicula.horario.hi >= APERTURA && pelicula.horario.hi <= CIERRE
        && pelicula.horario.mi  >=0 && pelicula.horario.mi <=59 &&            
        pelicula.horario.hf >= APERTURA && pelicula.horario.hf <= CIERRE && 
        pelicula.horario.mf >=0 && pelicula.horario.mf<=59 
        && duracion > 58 && duracion < 230) ) 
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

Salida nuevaPelicula(Funcion funcion,int i) {
    Salida out;
    if(i <= 5) {
        printf("\nNombre de la pelicula %d: ", i+1);
        fflush(stdin);
        gets(funcion.peliculas[i].nombre);

            printf("\n\t\tHoy abrimos a las %d:00 y Cerramos a las %d:00", APERTURA, CIERRE);
	        do {   
                printf("\n- - - - - - -Solo se aceptaran peliculas de 1-3hrs con 50 minutos- - - - - - -\n");
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

    out.funcion = funcion;
    out.i = i;
    return out;
}

Salida eliminarPelicula(Funcion funcion,int i) {
    int n;
    Salida out;
    printf("\nIntroduce que pelicula deseas eliminar: ");
    fflush(stdin);
    scanf("%d", &n);
    fflush(stdin);
    if (n-1 >= 0 && n-1 <=i) {
        for (int j = n-1; j < i; j++)
        {
            funcion.peliculas[j] = funcion.peliculas[j+1];
        }
        i--;
        printf("\nPelicula Eliminada\n");
    }
    else
        printf("\nPelicula no existente\n");

    out.funcion = funcion;
    out.i = i;
    return out;
}

Salida modificarPelicula(Funcion funcion,int i) {
    int n, opc2 = 0;
    Salida out;
    printf("\nIntroduce que pelicula deseas modificar: ");
    fflush(stdin);
    scanf("%d", &n);
    if (n-1 >= 0 && n-1 <=i) {
        do {
             printf("\n1. Nombre \t2. Horarios \t -1. Salir\n");
             scanf("%d", &opc2);
             switch (opc2)
             {
                case 1:
                        printf("\nNuevo nombre de la pelicula %d: ", n);
                        fflush(stdin);
                        gets(funcion.peliculas[n-1].nombre);
                        break;
                case 2:
     
                        printf("\nHoy abrimos a las %d:00 y Cerramos a las %d:00", APERTURA, CIERRE);
                        do
	                    {   
	                    	printf("\nNueva Hora inicial (formato H:M): ");
	                    	scanf("%d:%d",&funcion.peliculas[n-1].horario.hi, &funcion.peliculas[n-1].horario.mi);
	                    	printf("\nNueva Hora final (formato H:M): ");
	                    	scanf("%d:%d",&funcion.peliculas[n-1].horario.hf, &funcion.peliculas[n-1].horario.mf);
	                    } while ( !validarHoras(funcion.peliculas[n-1]) || !comprobacion(funcion.peliculas, n-1, i));
                        break;

                default:
                    break;
             }

        } while (opc2 != -1);
    }
    else 
        printf("\nPelicula no existente\n");

    out.funcion = funcion;
    return out;
}

Salida cartelera(Funcion funcion) {
	int i = 0, opc, opc2 =0,pos[limP]= {0,1,2,3,4,5,6,7};
    Salida out,in;
    do
    {
        printf("\n1. Ingresar Pelicula\n2. Eliminar Pelicula\n3. Cambiar datos de una pelicula\n4. Cartelera\n-1. Salir\n");
        scanf("%d", &opc);
        switch (opc)
        {

        case 1:
              in = nuevaPelicula(funcion,i);
              funcion = in.funcion;
              i = in.i;
            break;
        
        case 2:
              imprimirCartelera(funcion, i-1,pos);
              in = eliminarPelicula(funcion,i);
              funcion = in.funcion;
              i = in.i;
            break;


        case 3:
              imprimirCartelera(funcion, i-1,pos);
              in = modificarPelicula(funcion,i);
              funcion = in.funcion; 
            break;

        case 4: 
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

//Funciones para la compra de boletos

Sala inicializarAsientos(Sala sala) {
    int byte, fil, col;
    for ( fil = 0; fil < 16; fil++) {
        for ( col = 0; col < 13; col++)
        {
          byte = (fil <= 8 ? 0 : 1);
          sala.butacas[byte][col] = 0;
        }
    }

    return sala;
    }

int imprimirAsientos(Sala sala){
    int masc = 128, fil, col, byte;
    for ( fil = 0; fil < 16; fil++)
    {
        byte = fil / 8;
        for ( col = 0; col < 13; col++)
        {
          if (col == 0)
             printf("%d\t",fil+1);

          if ( sala.butacas[byte][col] & masc >> (fil % 8) )
             printf("O\t");
          else
             printf("-\t");
        }
        printf("\n");
        
    }

    printf("\n \t");
    for (int i = 1; i <= 13; i++)
        printf("%d\t",i);

	return 0;
}

int imprimirBoleto(int f, int c, Pelicula peli) {
    printf("\n- - - - - - - - - - - - - -GUARDE SU BOLETO- - - - - - - - - - - - - -\n");
    printf("TICKET $70.00\nPELICULA: %s\nFUNCION: %02d:%02d Llegue 5 minutos antes\n",peli.nombre,peli.horario.hi, peli.horario.mi);
    printf("Asiento : Fila %d Columna %d\n",f,c);
    printf("- - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - -\n");
}

Salida ordenamientoInsercion(Pelicula peliculas[], int n)
{
    Pelicula actual;
    Salida out;
    int i, j, posI;

    for ( int m = 0; m <= n; m++)
          out.pos[m] = m;
    
    for (i = 1; i <= n; i++) {   //USUALMENTE SE ORDENA UN ARREGLO, EN ESTE CASO SOLO ORDENAREMOS EL ARREGLO DE POSICIONES
                                 //PERO AL MOVER SUS ELEMENTOS, DEBEMOS TAMBIEN CAMBIAR LAS POSICIONES DE LAS PELICULAS A COMPARAR
                                 //COMO SI EN REALIDAD ORDENARAMOS EL ARREGLO DE PELICULAS PERO SIN MODIFICARLO
        actual = peliculas[out.pos[i]]; 
        posI = out.pos[i];
        j = i - 1;

        while (j >= 0 && ( peliculas[out.pos[j]].horario.hi > actual.horario.hi || 
              ( (peliculas[out.pos[j]].horario.hi == actual.horario.hi) && (peliculas[out.pos[j]].horario.mi > actual.horario.mi) ) ) )
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
    int inicio = 0, fin = i, mitad = (inicio + fin)/2, intentos;

    //SI PELICULA DE EN MEDIO ES IGUAL AL HORARIO QUE SE BUSCA
    if ( peliculas[ pos[mitad] ].horario.hi == busqueda.hi && peliculas[ pos[mitad] ].horario.mi == busqueda.mi ) 
        return mitad;

    while ( !(peliculas[ pos[mitad] ].horario.hi == busqueda.hi && peliculas[ pos[mitad] ].horario.mi == busqueda.mi) && intentos < 23 ) //MIENTRAS NO SE HAYA ENCONTRADO LA PELICULA
    {
        if ( busqueda.hi < peliculas[ pos[mitad] ].horario.hi ) // SI busqueda SE ENCUENTRA A LA IZQUIERDA DE LOS HORARIOS
        {
            fin = mitad -1; //SE COLOCA EL FIN ANTES DE LA MITAD DEL ARREGLO
        }
        else {
            inicio = mitad+1; // SE COLOCA EL INCIIO DESPUES DE LA MITAD DEL ARREGLO
        }
        mitad = (inicio + fin)/2;
        intentos++;          //AUMENTAMOS INTENTOS PARA EVITAR BUCLES INFINITOS
    }
    
    if ( intentos < 23)
       return mitad;
    else
       return -1;
    
}

int main() {
    Funcion funcion;     
    Salida entrada = cartelera(funcion), pos; //ACTUALIZACIÓN DE DATOS
    Horario busqueda;
	int i , j, opc, opc2, fil, col, masc = 128,n, ocupado = 0, r;
    i = entrada.i;

    funcion = entrada.funcion; 

    for (int j = 0; j <= i; j++)
        funcion.peliculas[j].sala = inicializarAsientos(funcion.peliculas[j].sala); //INICIALIZANDO VARIABLES ESPECIALES

    pos = ordenamientoInsercion(funcion.peliculas,i);   //ORDENAMIENTO POR HORA
    
    printf("\t\t|Bienvenido a cineFCC|\n");

    do {
        printf("\n-1. Salir\t0.Buscar por horario\t1.Comprar Boleto\n");
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
                printf("\nSe encontro: %s a las %02d:%02d\n", funcion.peliculas[pos.pos[r]].nombre, funcion.peliculas[pos.pos[r]].horario.hi, funcion.peliculas[pos.pos[r]].horario.mi );
            }
            else
                printf("\nLa pelicula no se encuentra en cartelera.\n");
        break;

        case 1:
            imprimirCartelera(funcion, i, pos.pos);
            printf("\nIntroduzca la pelicula donde se asignara una butaca: ");
            fflush(stdin);
            scanf("%d", &n);

            if (n-1 >= 0 && n-1 <=i) {
                n = pos.pos[n-1]+1; //ASIGNACION FEA PARA CORREGIR EL INDICE (1 POR LENGUAJE NATURAL, OTRO POR SER ARREGLO DE 0-N)
                do {
                    printf("\n1. Asignar butaca\n2. Liberar butaca\n3. Imprimir butacas disponibles\n-1. Salir\n ");
                    fflush(stdin);
                    scanf("%d", &opc2);
                    switch (opc2)
                    {
                       case 1: imprimirAsientos(funcion.peliculas[n-1].sala);
                               do
                               {
                                   printf("\nEn que fila (1-16) y columna (1-13) formato(F-C): ");
                                   fflush(stdin);
                                   scanf("%d-%d",&fil, &col);
                                   ocupado = 1;
                                   if ( (funcion.peliculas[n-1].sala.butacas[(fil-1)/8][col-1] & masc>>((fil-1)%8) ) == masc>>((fil-1)%8) ) 
                                    {
                                        ocupado = 0;
                                        printf("\nYa existe un asiento ocupado\n");
                                    }

                                          //falso si correcto                                 // verdadero si incorrecto
                               } while ( !(fil >= 1 && fil <= 16 && col >= 1 && col <= 13) || ocupado == 0 );

                               if (fil <= 8)
                                   funcion.peliculas[n-1].sala.butacas[0][col-1] |= masc>>fil-1; 
                               else
                                   funcion.peliculas[n-1].sala.butacas[1][col-1] |= masc>>fil-9;

                               printf("Se ha registrado la butaca en %d-%d\n",fil,col);
                               imprimirBoleto(fil,col,funcion.peliculas[n-1]);
                               break;

                       case 2: imprimirAsientos(funcion.peliculas[n-1].sala);
                               do
                               {
                                   printf("\nEn que fila (1-16) y columna (1-13) formato(F-C): ");
                                   fflush(stdin);
                                   scanf("%d-%d",&fil, &col);
                               } while ( !(fil >= 1 && fil <= 16 && col >= 1 && col <= 13) );

                               if (fil <= 8)
                                   funcion.peliculas[n-1].sala.butacas[0][col-1] &= 127>>fil-1; 
                               else
                                   funcion.peliculas[n-1].sala.butacas[1][col-1] &= 127>>fil-9;

                               printf("Se ha eliminado la butaca en %d-%d",fil,col);

                               break;

                       case 3:
                               imprimirAsientos(funcion.peliculas[n-1].sala);
                               break;

                       default:
                           break;
                    }
                }while(opc2 != -1);

            } 
            else
                printf("\nPelicula no existente\n");
            break;

            default:
                break;
            }


    } while (opc != -1);
    
    
}
