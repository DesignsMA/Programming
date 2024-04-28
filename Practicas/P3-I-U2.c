
#include <stdio.h>
#include <string.h>

#define MAX 20

typedef struct 
{
    char n[30];
}Nombres;

typedef struct 
{
    Nombres nombres[MAX];
    int inscritos[MAX], butacas[MAX],repetidos[MAX], j;
}Salon;

typedef struct 
{
    Salon aula;
    
}Salida;


int busqueda(int arreglo[],int val, int fin) { //Busca un valor en un arreglo y retorna su indice +1

    for (int i = 0; i < fin; i++)
    {
        if (arreglo[i] == val)
            return i+1; //Retorna el número en la lista
    }
    return -1;
    
}

Salon inscribir(Salon aula, int n) {
    int existe = 0; //booleano de existencia

    for (int i=0;i<n;i++) 
    {

        do
        {
            existe = 0;
            printf("Alumno %d\t|\tMatricula (1010-1200): ", i+1);
            fflush(stdin);
            scanf("%d", &aula.inscritos[i]);

            if (busqueda(aula.inscritos, aula.inscritos[i],i) > -1) 
            {
                existe = 1;
                printf("\nColoque otra matricula\n");
            }

        } while ( existe || !(aula.inscritos[i] >=1010 && aula.inscritos[i] <=1200) );
                //Mientras la matricula exista y no sea de formato 1010-1200

        aula.butacas[i] = -1; // a su vez se inicializa en -1 las butacas

        printf("\nNombre: ");
        fflush(stdin);
        scanf("%s[^\n]", aula.nombres[i].n);
        printf("\n");
    }

    return aula;
}

Salon entrada(Salon aula, int inicio, int fin, int lim)
{
    int n, existe, repite, matricula;


    for (int i = inicio ; i<fin ; i++) {
        do
        {
            existe = 0, repite = -1;
            printf("Alumno %d\t|\tMatricula (1010-1200): ", i+1);
            fflush(stdin);
            scanf("%d", &matricula);

            existe = busqueda(aula.inscritos,matricula,lim); //retorna el no. de lista del alumno

            if (existe == -1) 
                printf("\nNo existe esa matricula\n");
            
            if (existe > -1) //Si existe la matricula
            {
                repite = busqueda(aula.repetidos,matricula,lim);
                if ( repite == -1) 
                {
                    aula.repetidos[aula.j] = matricula;
                    aula.j++;
                }
                else
                    printf("\nYa existe esa matricula\n");
            }
            
        } while ( existe == -1 || repite > -1);
                //Mientras la matricula no exista u  ocupe una plaza que ya tiene
        
        aula.butacas[i] = existe; //asignar en la butaca i el no. de lista del alumno
    }

    return aula;
}

int asistencias(Salon aula, int temprano, int tarde, int n){
    int j, i=0;
    char texto[20];
    strcpy(texto,"Temprano");

    printf("\n\t\tREPORTE DE ASISTENCIA\n\t\tAlumnos Inscritos: %d", n);
    printf("\nLlegada    \tNo. de butaca\tNo. de lista\tMatricula\tNombre\n");
    
    for (i = 0; i < temprano+tarde; i++){
        j = aula.butacas[i]-1; //obtener indice de butacas
        if ( i >= temprano)
            strcpy(texto,"Tarde");

        printf("%-9s\t\t%d\t\t%d\t%d\t\t%s\n",texto,i+1 , j+1, aula.inscritos[j], aula.nombres[j].n);
    }

    for (int m = 0; m < n; m++)
        if ( busqueda(aula.butacas,m+1,n) == -1) //Si no se encuentra su no. de lista
            printf("No llego \t\t-\t\t%d\t%d\t\t%s\n",m+1, aula.inscritos[m], aula.nombres[m].n);
        
}

int main()  {
    int tarde, temprano, n, repetidos[MAX], j=0;
    Salon aula;
    aula.j =0;
    
    do
    {
        printf("\nIntroduzca los alumnos a inscribir\t|\tCupo: %d\n: ", MAX);
        scanf("%d", &n);
    } while ( n < 1 || n > MAX);

    aula = inscribir(aula,n); //Se inscriben los estudiantes

    printf("\nIntroduzca cuantos alumnos llegaron a tiempo\n");
    scanf("%d", &temprano);
    aula = entrada(aula,0,temprano,n); //Estudiantes que llegaron temprano

    printf("\nIntroduzca cuantos alumnos llegaron tarde\n");
    scanf("%d", &tarde);
    aula = (entrada(aula,temprano,temprano+tarde,n)); //Estudiantes que llegaron tarde

    asistencias(aula,temprano, tarde, n);

    do
    {
    } while (!(getchar() =='s'));
    return 0;
}