package Banco; //Carpeta (paquete)
import java.util.Scanner;

public class Banco { //Clase principal

    public static void main () {
        Scanner in = new Scanner( System.in );
        String nombre;

        //Instancia de la clase CuentaBancaria (Objetos)
        Cuenta c1 = new Cuenta(); //Identidad
        Cuenta c2;
        c1.setSaldo(9999);
        c1.setTitular("Paco Antonio");
        System.out.println(c1.getNumeroCuenta());
        System.out.println(c1.getTitular());
        System.out.println(c1.getSaldo());
        System.out.println(c1.toString());

        System.out.println("Ingrese el nombre del titular de la cuenta: ");
        nombre = in.nextLine();
        c2 = new Cuenta(nombre); //objeto
        c2.datosCuenta(); //Estado
        c2.depositar(); //Comportamiento
        c2.retirar();
        c2.datosCuenta(); //Comportamiento

        in.close();
    }
}