
/* Crear programa que lea dos  variables y lanze un error  si son negativas
 * , no sean un número,  almacenar en v1 y v2,
 * dividir v1 entre v2 en un metodo estatico llamado dividir que  acepte
 * a v1 y v2 como parametros, lanzar EXCEPCION PERSONALIZADA si la division se realiza
 * entre cero
  */
import java.util.Scanner;
import java.util.InputMismatchException;

/* Excepcion personalizada
   Una excepcion es un tipo de error VERIFICADO que requiere
   que se indique a java de  su lanzamiento por medio de throws
   o captura por medio de un catch
 */

class NumerosNegativosException extends Exception {
    public NumerosNegativosException(String mensaje) {
        super(mensaje);
    }
}

public class tests {

    public static void dividir(double v1, double v2) {
        try {
            double res = v1 / v2;
            System.out.println("El cociente es: " + res);

        } catch (ArithmeticException e) {
            System.out.println("No se puede dividir por cero.");
        }

    }

    public static void main(String[] args) {
        double v1, v2;
        Scanner scanner = new Scanner(System.in);
        // leer variables

        try {

            System.out.println("Dato 1: ");
            v1 = scanner.nextDouble();
            scanner.nextLine();

            System.out.println("Dato 2: ");
            v2 = scanner.nextDouble();
            scanner.nextLine();

            if (v1 < 0 || v2 < 0) {
                throw new NumerosNegativosException("No se permiten numeros negativos.");

            }

            dividir(v1, v2);

        } catch (NumerosNegativosException e) {
            System.out.println(e.getMessage());
        } catch (InputMismatchException e) {
            System.out.println("Se esperaba un numero decimal, ingrese una entrada valida.");
        }

        scanner.close();
    }
}
