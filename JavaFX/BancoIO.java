import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.InputMismatchException;
import java.util.Scanner;

public class BancoIO {

    public static void leerArchivo(String nombreArchivo, Banco banco) throws FileNotFoundException {
        Scanner sc;
        sc = new Scanner(new File(nombreArchivo));
        while (sc.hasNext()) { // Mientras el escaner pueda leer
            banco.agregarCuenta(leerCuenta(sc));
        }
        sc.close();
    }

    public static CuentaBancaria leerCuenta(Scanner sc) {
        // noCuenta balance
        int noCuenta;
        double balance;
        try {
            noCuenta = sc.nextInt();
            balance = sc.nextDouble();
        } catch (InputMismatchException e) {
            return new CuentaBancaria(0, 12345);
        }
        return new CuentaBancaria(balance, noCuenta);
    }

    public static void escribirArchivo(String nombreArchivo, Banco banco) {
        PrintWriter out;
        try {
            out = new PrintWriter(nombreArchivo);
        } catch (FileNotFoundException e) { // Atrapando EXCEPCION
            System.out.println("Archivo " + nombreArchivo + "  no encontrado.");
            return;
        }

        for (CuentaBancaria c : banco.getCuentas()) {
            out.format("%d %f\n", c.getNoCuenta(), c.getBalance());
        }
        out.close();
    }

}
