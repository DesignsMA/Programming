#include <stdio.h>
#include <string.h>

#define MAX_LINEA 256
const char *archivo = "agenda.txt";

typedef struct{
    char nombre[50];
    char telefono[15];
    char email[50];
    char direccion[100];
} Contacto;

void limpiarBuffer(){
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

FILE* abrirArchivo(const char *archivo,int tipo) {
    FILE *agenda;
    if (tipo == 1) {
        agenda = fopen(archivo, "r");
        if (agenda == NULL) {
            printf("No se pudo abrir el archivo en modo lectura.\n");
            return NULL;
        }
    } 
    else if (tipo == 2) {
        agenda = fopen(archivo, "w");
        if (agenda == NULL) {
            printf("No se pudo crear el archivo.\n");
            return NULL;
        }
    } 
    else if (tipo == 3) {
        agenda = fopen(archivo, "a+");
        if (agenda == NULL) {
            printf("No se pudo abrir el archivo.\n");
            return NULL;
        }
    }
    else return NULL;
    return agenda;
}

void agregar(FILE *agenda){
    Contacto nuevoContacto;
    fclose(agenda);
    abrirArchivo(archivo,3);

    printf("\nIntroduzca el nombre: ");
    fgets(nuevoContacto.nombre, sizeof(nuevoContacto.nombre), stdin);
    nuevoContacto.nombre[strcspn(nuevoContacto.nombre, "\n")] = 0;

    do{
        printf("Introduzca el numero telefonico(10 digitos): ");
        fgets(nuevoContacto.telefono, sizeof(nuevoContacto.telefono), stdin);
        nuevoContacto.telefono[strcspn(nuevoContacto.telefono, "\n")] = 0;
            if (strlen(nuevoContacto.telefono) != 10) {
            printf("Debe ingresar un numero de telefono valido (10 digitos).\n");
            }
    } while (strlen(nuevoContacto.telefono)!=10);
    
    printf("Introduzca el email: ");
    fgets(nuevoContacto.email, sizeof(nuevoContacto.email), stdin);
    nuevoContacto.email[strcspn(nuevoContacto.email, "\n")] = 0;

    printf("Introduzca la direccion: ");
    fgets(nuevoContacto.direccion, sizeof(nuevoContacto.direccion), stdin);
    nuevoContacto.direccion[strcspn(nuevoContacto.direccion, "\n")] = 0;

    fprintf(agenda, "%s,%s,%s,%s\n", nuevoContacto.nombre, nuevoContacto.telefono, nuevoContacto.email, nuevoContacto.direccion);
    printf("\nContacto agregado exitosamente.\n");
    fclose(agenda);

    printf("\nPresiona Enter para continuar...\n");
    getchar();
}

void editar(FILE *agenda, int tipo, char *valorbuscado){
    char *nombre3, *telefono3, *email3, *direccion3;
    char linea[MAX_LINEA],nom[50],num[10],email[50],dir[50];
    int encontrado = 0;

    fclose(agenda);
    abrirArchivo(archivo,3);

    FILE *temp = fopen("temp.txt", "w");

    if (temp == NULL) {
        printf("Error al abrir el archivo temporal.\n");
        return;
    }

    rewind(agenda);

    while (fgets(linea, MAX_LINEA, agenda) != NULL) {
        linea[strcspn(linea, "\n")] = 0;

        nombre3 = strtok(linea, ",");
        telefono3 = strtok(NULL, ",");
        email3 = strtok(NULL, ",");
        direccion3 = strtok(NULL, ",");

        if (strcmp(nombre3, valorbuscado) != 0){
            fprintf(temp, "%s,%s,%s,%s\n", nombre3, telefono3, email3, direccion3);
        }else {
            encontrado = 1;
            
            if (tipo == 1){
                printf("\nCual es el nuevo nombre? ");
                fgets(nom,sizeof(nom),stdin);
                nom[strcspn(nom, "\n")] = 0;
                nombre3 = nom;
                fprintf(temp, "%s,%s,%s,%s\n", nombre3, telefono3, email3, direccion3);
            }else if (tipo == 2){
                printf("\nCual es el nuevo numero de telefono? ");
                fgets(num,sizeof(num),stdin);
                num[strcspn(num, "\n")] = 0;
                telefono3 = num;
                fprintf(temp, "%s,%s,%s,%s\n", nombre3, telefono3, email3, direccion3);
                limpiarBuffer();
            }else if (tipo == 3){
                printf("\nCual es el nuevo correo? ");
                fgets(email,sizeof(email),stdin);
                email[strcspn(email, "\n")] = 0;
                email3 = email;
                fprintf(temp, "%s,%s,%s,%s\n", nombre3, telefono3, email3, direccion3);
            }else if (tipo == 4){
                printf("\nCual es la nueva direccion? ");
                fgets(dir,sizeof(dir),stdin);
                dir[strcspn(dir, "\n")] = 0;
                direccion3 = dir;
                fprintf(temp, "%s,%s,%s,%s\n", nombre3, telefono3, email3, direccion3);
            }
        }
    }

    if (encontrado) {
        printf("\nContacto editado.\n");
    }else printf("Contacto no encontrado.\n");

    fclose(temp);
    fclose(agenda);

    remove("agenda.txt");
    rename("temp.txt", "agenda.txt");

    printf("\nPresiona Enter para continuar...\n");
    getchar();

}

void eliminar(FILE *agenda){
    char *nombre2, *telefono2, *email2, *direccion2;
    char linea[MAX_LINEA],nom[50],num[20];
    int encontrado = 0;

    fclose(agenda);
    abrirArchivo(archivo,3);

    FILE *temp = fopen("temp.txt", "w");

    if (temp == NULL) {
        printf("Error al abrir el archivo temporal.\n");
        return;
    }

    rewind(agenda);

    printf("\nCual es el nombre del contacto a eliminar? ");
    fgets(nom,sizeof(nom),stdin);
    nom[strcspn(nom, "\n")] = 0;

    while (fgets(linea, MAX_LINEA, agenda) != NULL){
        linea[strcspn(linea, "\n")] = 0;

        nombre2 = strtok(linea, ",");
        telefono2 = strtok(NULL, ",");
        email2 = strtok(NULL, ",");
        direccion2 = strtok(NULL, ",");

        if (strcmp(nombre2, nom) != 0){
            fprintf(temp, "%s,%s,%s,%s\n", nombre2, telefono2, email2, direccion2);
        }else encontrado = 1;
    }
    if (encontrado) {
        printf("Contacto eliminado.\n");
    }else printf("Contacto no encontrado.\n");

    fclose(temp);
    fclose(agenda);

    remove("agenda.txt");
    rename("temp.txt", "agenda.txt");

    printf("\nPresiona Enter para continuar...\n");
    getchar();
}

void buscar(FILE *agenda,int tipo){
    char linea[MAX_LINEA], nom[50],num[20];
    char *nombre, *telefono, *email, *direccion;
    int encontrado = 0;

    fclose(agenda);
    abrirArchivo(archivo,1);
    rewind(agenda);

    if (tipo == 1)
    {
        printf("\nCual es el nombre a buscar? ");
        fgets(nom,sizeof(nom),stdin);
        nom[strcspn(nom, "\n")] = 0;

        while (fgets(linea, MAX_LINEA, agenda) != NULL) {
            linea[strcspn(linea, "\n")] = 0;

            nombre = strtok(linea, ",");
            telefono = strtok(NULL, ",");
            email = strtok(NULL, ",");
            direccion = strtok(NULL, ",");

            if (strcmp(nombre, nom) == 0){
                encontrado = 1;
                printf("\nNombre: %s\nTelefono: %s\nEmail: %s\nDireccion: %s\n", nombre, telefono, email, direccion);
                break;
            }
        }
        
    }else if (tipo == 2)
    {
        do{
            printf("\nCual es el numero de telefono? ");
            fgets(num,sizeof(num),stdin);
            num[strcspn(num, "\n")] = 0;
                if (strlen(num) != 10) {
                    printf("Debe ingresar un numero de telefono valido (10 digitos).\n");
                }
        } while (strlen(num)!=10);


        while (fgets(linea, MAX_LINEA, agenda) != NULL) {
            linea[strcspn(linea, "\n")] = 0;

            nombre = strtok(linea, ",");
            telefono = strtok(NULL, ",");
            email = strtok(NULL, ",");
            direccion = strtok(NULL, ",");

            if (strcmp(telefono, num) == 0){
                encontrado = 1;
                printf("\nNombre: %s\nTelefono: %s\nEmail: %s\nDireccion: %s\n", nombre, telefono, email, direccion);
                break;
            }
        }
    }
    if (!encontrado) {
        printf("\nContacto no encontrado.\n");
    }

    fclose(agenda);
    printf("\nPresiona Enter para continuar...\n");
    getchar();
}

void listar(FILE *agenda){
    char linea[MAX_LINEA];
    char *nombre, *telefono, *email, *direccion;

    fclose(agenda);
    abrirArchivo(archivo,1);
    rewind(agenda);

    while (fgets(linea, MAX_LINEA, agenda) != NULL) {
        linea[strcspn(linea, "\n")] = 0;

        nombre = strtok(linea, ",");
        telefono = strtok(NULL, ",");
        email = strtok(NULL, ",");
        direccion = strtok(NULL, ",");

        printf("\nNombre: %s\n", nombre);
        printf("Telefono: %s\n", telefono);
        printf("Email: %s\n", email);
        printf("Direccion: %s\n", direccion);
    }
    fclose(agenda);
    printf("\nPresiona Enter para continuar...\n");
    getchar();
}

void menuEditar(FILE *agenda){

    char opcion;
    char nom[50];

    printf("\nCual es el nombre del contacto que quiere editar? ");
    fgets(nom,sizeof(nom),stdin);
    nom[strcspn(nom, "\n")] = 0;

    do{
        printf("\nCual es el campo que quiere editar?\n\n");
        printf("1. Nombre.\n");
        printf("2. Telefono.\n");
        printf("3. Email.\n");
        printf("4. Direccion.\n");
        printf("5. Regresar al menu anterior.\n");
        printf("\nElija una opcion: ");
        char entrada[10];
        fgets(entrada, sizeof(entrada), stdin);

        if (strlen(entrada)!=2){
            printf("\nDebe ingresar solo un digito\n");
            printf("\nPresiona Enter para continuar...\n");
            getchar();
            continue;
        }

        opcion = entrada[0];

        switch (opcion){
            case '1':
                editar(agenda,1,nom);
                return;
            case '2':
                editar(agenda,2,nom);
                return;
            case '3':
                editar(agenda,3,nom);
                return;
            case '4':
                editar(agenda,4,nom);
                return;
            case '5':
                printf("\n\n");
                return;
            default:
                printf("Opcion no valida.\n");
                printf("\nPresiona Enter para continuar...\n");
                getchar();
                break;
            }
    } while (opcion!='3');
}

void menuBusqueda(FILE *agenda){

    char opcion;

    do{
        printf("\nComo quiere buscar el contacto?\n");
        printf("1. Nombre.\n");
        printf("2. Telefono.\n");
        printf("3. Menu anterior.\n");
        printf("\nElija una opcion: ");
        char entrada[10];
        fgets(entrada, sizeof(entrada), stdin);

        if (strlen(entrada)!=2){
            printf("\nDebe ingresar solo un digito\n");
            printf("\nPresiona Enter para continuar...\n");
            getchar();
            continue;
        }

        opcion = entrada[0];

        switch (opcion){
            case '1':
                buscar(agenda,1);
                return;
            case '2':
                buscar(agenda,2);
                return;
            case '3':
                printf("\n\n");
                break;
            default:
                printf("\nOpcion no valida.\n");
                printf("\nPresiona Enter para continuar...\n");
                getchar();
                break;
        }
    } while (opcion!='3');
}

void menuPrincipal(FILE *agenda){

    char opcion;

    do{
        printf("\nMenu principal\n");
        printf("1. Agregar nuevo contacto.\n");
        printf("2. Editar contacto.\n");
        printf("3. Eliminar contacto.\n");
        printf("4. Buscar contacto.\n");
        printf("5. Listar contactos.\n");
        printf("6. Salir del programa.\n");
        printf("Elija una opcion: ");

        char entrada[10];
        fgets(entrada, sizeof(entrada), stdin);

        if (strlen(entrada)!=2){
            printf("\nDebe ingresar solo un digito\n");
            printf("\nPresiona Enter para continuar...\n");
            getchar();
            continue;
        }

        opcion = entrada[0]; 
        
        switch (opcion){
            case '1':
                agregar(agenda);
                break;
            case '2':
                menuEditar(agenda);
                break;
            case '3':
                eliminar(agenda);
                break;
            case '4':
                menuBusqueda(agenda);
                break;
            case '5':
                listar(agenda);
                break;
            case '6':
                printf("\nSaliendo del programa. Adios!");
                break;
            default:
                printf("\nOpcion no valida.\n");
                printf("\nPresiona Enter para continuar...\n");
                getchar();
                break;
        }
    } while (opcion!='6');
}

int main(){

    printf("Bienvenido a tu agenda!\n");

    FILE *agenda = fopen(archivo, "r");
    if (agenda == NULL) {
        agenda = fopen(archivo, "w");
        if (agenda == NULL) {
            printf("No se pudo abrir ni crear el archivo.\n");
            return 1;
        }
        printf("Archivo creado exitosamente.\n");
        menuPrincipal(agenda);
    } else {
        menuPrincipal(agenda);
        }
    fclose(agenda);
    return 0;
} 
