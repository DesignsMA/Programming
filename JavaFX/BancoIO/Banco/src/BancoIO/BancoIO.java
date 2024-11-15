package BancoIO;

import java.io.File;
import java.io.PrintWriter;
import java.util.Scanner;
import java.io.FileNotFoundException;

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
        noCuenta = sc.nextInt();
        balance = sc.nextDouble();
        return new CuentaBancaria(balance, noCuenta);
    }

    public static void escribirArchivo(String nombreArchivo, Banco banco) throws FileNotFoundException {
        PrintWriter out;
        out = new PrintWriter(nombreArchivo);
        for (CuentaBancaria c : banco.getCuentas()) {
            out.format("%d %f\n", c.getNoCuenta(), c.getBalance());
        }
        out.close();
    }

}
