import java.util.Scanner;

public class Cadenas {
    //Reemplaza todas las subcadenas de cadena que cumplan con la expresion regular `exreg`
    public static String sustituir( String exreg, String cadena , String remplazo) {
        return cadena.replaceAll(exreg, remplazo); 
    }

    public static String invertir( String cadena ) { //Un método estatico puede ser accedido sin crear una instancia de la clase
        String subcadenas[];
        subcadenas = cadena.split("\s+"); /*Divide en subcadenas usando la expresion regular "uno o más espacios empezando desde la derecha"
                                                  como delimitador*/

        String invertidas[] = new String[subcadenas.length]; //Arreglo del mismo tamaño que subcadenas | No contiene nada, todo es null

        for (int i = 0; i < subcadenas.length; i++ ) { //Invertir subcadenas y referenciar nuevas instancias en invertidas
            int n = subcadenas[i].length();
            invertidas[i] = ""; //Inicializar la subcadena invertida, sino concatena null+letra 
            for ( int z = 0; z < n ; z++ ) {
                invertidas[i] += subcadenas[i].charAt( n - z  - 1 );
            }
        }

        for (int i = 0 ; i < subcadenas.length ; i++ ) { //Concatenar las subcadenas invertidas

            //Sustituir la cadena (palabra) original con la subcadena (palabra) c de invertidas actual y concatenar en invertida
            //Esto se hace para conservar espacios y formato original de la cadena
            
            cadena = sustituir(subcadenas[i], cadena, invertidas[i]); //apuntar a la nueva cadena con la palabra invertida [i]
        }

        return cadena; //Retornar apuntador a la ultima instancia resultante de la sustitucion de todas las subcadenas con invertidas en cadena
        
    }

    public static void rombo ( String c ) {
        int n = ( c.length() <= 10 ? c.length()-1 : 9 ), filas, pivote = 0; //Limite de 10 caracteres
        filas = n*2+1; // Siempre tiene centro
        for (int i = 0; i < filas ; i++) { //Imprimir filas

            for (int j = 0; j < n; j++) { //imprimir n espacios
                System.out.print("  ");
            }

            for (int l = 0; l < pivote; l++) //imprimir de 0 a pivote -1
                System.out.print(c.charAt(l) + " ");
            System.out.print(c.charAt(pivote) + " "); // imprimir pivote
            for (int l = pivote-1; l >= 0; l--) //imprimir de pivote -1 a cero
                System.out.print(c.charAt(l) + " ");
            

            if ( i >= filas/2 )  { //si se llego al centro
                n++;
                pivote--;   
            }
            else  {
                n --;
                pivote++;
            }
            System.out.println();
        }

    }
    public static void main(String[] args) {
        Scanner sc = new Scanner( System.in );
        do {

            System.out.println("Ingrese un texto, escriba salir para parar: ");
            String s = sc.nextLine();

            if (s.equals("salir")) {
                break;
            } else {
                System.out.println("\nTexto invertido: " + invertir(s));
            }


            System.out.println();
            rombo(s);

        } while (true);

    }
}
