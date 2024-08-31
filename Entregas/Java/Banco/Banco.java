import java.util.Random;
//Clases
class Cuenta { //La clase no tiene tipo de acceso puesto que solo se accede desde el propio archivo
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
        saldo = 0f;
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
        Random rand = new Random();
        return Integer.parseInt( Integer.toString(rand.nextInt(9999))+actual );
    }
    
    //Comportamiento

    public void depositar (double cantidad) {
        saldo += cantidad;
        System.out.println("\nDeposito exitoso");
    }

    public void retirar (double cantidad) {
        if ( saldo >= 1.0f) {
            if ( saldo < cantidad ) System.out.println("\nSaldo insuficiente | Saldo actual: " + saldo);
            else
            {
                saldo -= cantidad;
                System.out.println("\nRetiro exitoso");
            }
        }
        else System.out.println("\nActualmente no cuentas con saldo en tu cuenta");
    }

    public void datosCuenta () {
        System.out.println("\nNumero de cuenta: " + numeroCuenta);
        System.out.println("Titular: " + titular);
        System.out.println("Saldo: " + saldo);
    }

    public String toString () {
        return "CuentaBancaria[Numero de cuenta: " + numeroCuenta + "Titular: " + titular + "Saldo: " + saldo+"]";
    }
}

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