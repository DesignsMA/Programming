package Banco; //Paquete
import java.util.Date;
import java.text.SimpleDateFormat;
import java.util.Scanner;

public class Cuenta { //Clase
    //Atributos
    private int numeroCuenta;
    private String titular;
    private double saldo;
    private static int actual; //Se conserva entre instancias

    //Constructores 

    //Constructor por defecto
    public Cuenta () { 
        numeroCuenta = numCuenta();
        titular = "John Doe";
        saldo = 0;
        actual++;
    }

    //Constructor por parametros
    public Cuenta (String Titular) { 
        numeroCuenta = numCuenta(); // Dandole formato a la fecha actual y guardando numero de cuenta
        this.titular = Titular;
        saldo = 0;
        actual++;
    }

    //Getters | Accedentes | Acceden

    public int getNumeroCuenta () { return numeroCuenta; };
    public String getTitular () { return titular; };
    public double getSaldo () { return saldo; };

    //Setters | Mutadores | Modifican

    public void setTitular (String t) { titular = t;}
    public void setSaldo (double s) { saldo = s;}

    //Métodos definidos por el usuario

    public int numCuenta () {
        Date fecha = new Date();
        SimpleDateFormat idFormato = new SimpleDateFormat("ddMMyykkmm" + actual);
        return Integer.parseInt( idFormato.format(fecha) );// Dandole formato a la fecha actual y guardando numero de cuenta
    }
    
    //Comportamiento

    public void depositar () {
        Scanner in = new Scanner( System.in );
        double cantidad;
        do
        {
            System.out.println("Ingrese la cantidad a depositar (Mínimo $1): ");
            cantidad = in.nextDouble(); //Leer numero de doble precision | No se manejan errores
        } while ( cantidad <= 1.0 );
        saldo += cantidad;
        System.out.println("Deposito exitoso");
        in.close();
    }

    public void retirar () {
        if ( saldo > 1.0) {
            Scanner in = new Scanner( System.in );
            double cantidad;
            do
            {
                System.out.println("Ingrese la cantidad a retirar (Mínimo $1): ");
                cantidad = in.nextDouble(); //Leer numero de doble precision | No se manejan errores
            } while ( cantidad <= 1.0 );

            if ( saldo < cantidad ) System.out.println("Saldo insuficiente");
            else
            {
                saldo -= cantidad;
                System.out.println("Retiro exitoso");
            }
            in.close();
        }
        else System.out.println("Actualmente no cuentas con saldo en tu cuenta");
    }

    public void datosCuenta () {
        System.out.println("Numero de cuenta: " + numeroCuenta);
        System.out.println("Titular: " + titular);
        System.out.println("Saldo: " + saldo);
    }

    public String toString () {
        return "CuentaBancaria[Numero de cuenta: " + numeroCuenta + "Titular: " + titular + "Saldo: " + saldo+"]";
    }
}
