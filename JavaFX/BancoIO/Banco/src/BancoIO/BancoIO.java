package BancoIO;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.InputMismatchException;
import java.util.Scanner;

/* https://www.geeksforgeeks.org/file-class-in-java/ | Notas manejo de archivos */
/*
• public static void leerArchivo(String nombreArchivo, Banco banco) 
Este método debe crear un objeto Scanner que lea del archivo cuyo nombre se especifica en el 
paso de parámetros. Mientras haya datos, el método leerArchivo() debe invocar 
repetidamente al método leerCuenta(), el cual regresará un objeto de tipo CuentaBancaria. El 
método leerArchivo() deberá agregar la cuenta bancaria al banco proporcionado en el paso de 
parámetros. 

• public static CuentaBancaria leerCuenta(Scanner sc) 
Este método se usará para leer los datos de una cuenta bancaria. Se debe recibir por 
parámetros un objeto de tipo Scanner, con el cual se leerá el número de cuenta (int) y el 
balance (double) del archivo. Este método deberá crear un nuevo objeto de tipo 
CuentaBancaria y retornarlo al método que lo invocó. */
public class BancoIO {

    public static void leerArchivo(String nombreArchivo, Banco banco) {
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
            Alert a = new Alert(AlertType.Warning);
            a.setTitle("Error");
            a.setContentText("Datos erroneos");
            a.showAndWait();
            return new CuentaBancaria(0, 0);
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
    }

}
