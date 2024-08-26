package Banco; //Carpeta (paquete)
public class Banco { //Clase principal

    public static void main ( String [] args) {
        //Instancia de la clase CuentaBancaria (Objetos)
        Cuenta c1 = new Cuenta(); //Identidad
        Cuenta c2 = new Cuenta("Juan Capulin");
        c1.setSaldo(9999);
        c1.setTitular("Paco Antonio");
        System.out.println(c1.getNumeroCuenta());
        System.out.println(c1.getTitular());
        System.out.println(c1.getSaldo());
        System.out.println(c1.toString());

        c2.datosCuenta(); //Estado
        c2.depositar(140.5f); //Comportamiento
        c2.retirar(150.0f);
        c2.retirar(100.0f);
        c2.datosCuenta(); //Comportamiento

    }
}