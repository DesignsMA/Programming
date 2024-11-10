import java.util.InputMismatchException;
import java.util.Scanner;

public class ExcepcionesCuentaBancaria {
    static Scanner sc = new Scanner(System.in);

    private static int obtenerOpcionUsuario() {
        int opcion = 0;
        try {
            do {
                opcion = -1;
                System.out.println("Opciones Menú:");
                System.out.println("0) Salir");
                System.out.println("1) Crear nueva cuenta");
                System.out.println("2) Depositar cuenta actual");
                System.out.println("3) Retirar cuenta actual");
                System.out.println("4) Buscar cuenta");
                System.out.println("5) Imprimir todas las cuentas");

                System.out.print("Digita tu opción(0 - 5): ");
                opcion = sc.nextInt();

                if (opcion < 0 || opcion > 5)
                    System.out.println("Opción inválida");
            } while (opcion < 0 || opcion > 5);
        } catch (InputMismatchException e) {
            System.out.println("Debes introducir un entero.");
            sc = new Scanner(System.in);
        }
        return opcion;
    }

    private static double obtenerCantidad() {
        boolean flag;
        double opc = 0;
        do {
            flag = false;
            try {
                System.out.print("Cantidad : ");
                opc = sc.nextDouble();
            } catch (InputMismatchException e) {
                System.out.println("No es un número");
                sc = new Scanner(System.in);
                flag = true;
            }
        } while (flag);
        return opc;
    }

    private static int obtenerNoCuenta() {
        boolean flag;
        int opc = 0;
        do {
            flag = false;
            try {
                System.out.print("No Cuenta : ");
                opc = sc.nextInt();
            } catch (InputMismatchException e) {
                System.out.println("No es un entero");
                sc = new Scanner(System.in);
                flag = true;
            }
        } while (flag);
        return opc;
    }

    public static void main(String[] args) {
        Banco banco = new Banco(10);
        CuentaBancaria cuenta = null;
        double cantidad;
        int noCuenta, opcion;

        do {
            opcion = obtenerOpcionUsuario();

            switch (opcion) {
                case 1:
                    try {
                        cantidad = obtenerCantidad();
                        noCuenta = obtenerNoCuenta();
                        cuenta = new CuentaBancaria(cantidad, noCuenta); // Lanza error
                        banco.agregarCuenta(cuenta); // Codigo inalcanzable en error
                        System.out.println("Información cuenta: " + cuenta + "\n");

                    } catch (IllegalArgumentException e) {
                        System.out.println("ERROR: " + e.getMessage());
                    }
                    break;
                case 2:
                    try {
                        cantidad = obtenerCantidad();
                        cuenta.depositar(cantidad);
                        System.out.println("Información de la cuenta: " + cuenta + "\n");
                    } catch (IllegalArgumentException e) {
                        System.out.println("ERROR: " + e.getMessage());
                    } catch (NullPointerException e2) {
                        System.out.println("ERROR:  No existe la cuenta. Busque o cree una cuenta");
                    }
                    break;
                case 3:
                    try {
                        cantidad = obtenerCantidad();
                        cuenta.retirar(cantidad);
                        System.out.println("Información de la cuenta: " + cuenta + "\n");
                    } catch (IllegalArgumentException e) {
                        System.out.println("ERROR: " + e.getMessage());
                    } catch (NullPointerException e2) {
                        System.out.println("ERROR:  No existe la cuenta. Busque o cree una cuenta");
                    } catch (RuntimeException e3) {
                        System.out.println("ERROR: " + e3.getMessage());
                    }
                    break;
                case 4:
                    noCuenta = obtenerNoCuenta();
                    CuentaBancaria b = banco.buscarCuenta(noCuenta);
                    if (b != null) {
                        cuenta = b; // Sustituye cuenta
                        System.out.println("Información cuenta: " + cuenta + "\n");
                    } else {
                        System.out.println("\n*****ERROR*****: Cuenta bancaria " + noCuenta + " no encontrada!\n");
                    }
                    break;

                case 5:
                    System.out.print("\n\nLas cuentas: \n" + banco + "\n\n");
                    break;
            }
        } while (opcion != 0);
        System.out.println("\n\nHasta luego!");
    }
}
