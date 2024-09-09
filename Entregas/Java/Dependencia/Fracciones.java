package Entregas.Java.Dependencia;
import java.util.Scanner;
class Fraccion {
    private int numerador;
    private int denominador;

    public Fraccion () {
        numerador = 1;
        denominador = 1;
    }

    public Fraccion ( int n, int d) {
        numerador = n;
        denominador = d;
    }

    public int getNumerador() {
        return numerador;
    }

    public int getDenominador() {
        return denominador;
    }

    public void setNumerador(int numerador) {
        this.numerador = numerador;
    }

    public void setDenominador(int denominador) {
        this.denominador = denominador;
    }

    public Fraccion sumar ( Fraccion f ) { //Dependencia, hace uso de la clase Fraccion temporalmente
        int n = numerador*f.getDenominador() + f.getNumerador()*denominador;
        int d = denominador*f.getDenominador();
        return new Fraccion(n, d);
    }

    public Fraccion restar ( Fraccion f ) {
        int n = numerador*f.getDenominador() - f.getNumerador()*denominador;
        int d = denominador*f.getDenominador();
        return new Fraccion(n, d);
    }

    public Fraccion multiplicar ( Fraccion f ) {
        int n = numerador*f.getNumerador();
        int d = denominador*f.getDenominador();
        return new Fraccion(n, d);
    }

    public Fraccion dividir ( Fraccion f ) {
        int n = numerador*f.getDenominador();
        int d = denominador*f.getNumerador();
        return new Fraccion(n, d);
    }

    public Fraccion simplificar () {
        int n = numerador;
        int d = denominador;
        int aux;
        while ( d != 0 ) {
            aux = d; //guardar divisor actual
            d = n%d; // 
            n = aux; //denominador 
        }
        return new Fraccion(numerador/n, denominador/n);

    }

    public String toString () {
        return numerador + "/" + denominador;
    }

}

public class Fracciones {

    public static void main(String[] args) {
        int n, d;
        Fraccion f1, f2;
        Scanner sc = new Scanner(System.in);
        System.out.println("Introduce el numerador de la primera fracción: ");
        n = sc.nextInt();
        System.out.println("Introduce el denominador de la primera fracción: ");
        d = sc.nextInt();
        f1 = new Fraccion(n, d);
        System.out.println("Introduce el numerador de la segunda fracción: ");
        n = sc.nextInt();
        System.out.println("Introduce el denominador de la segunda fracción: ");
        d = sc.nextInt();
        f2 = new Fraccion(n, d);
        System.out.println("La primera fracción es: " + f1);
        System.out.println("La segunda fracción es: " + f2);
        System.out.println("La suma de las fracciones es: " + f1.sumar(f2).simplificar());
        System.out.println("La resta de las fracciones es: " + f1.restar(f2).simplificar());
        System.out.println("La multiplicación de las fracciones es: " + f1.multiplicar(f2).simplificar());
        System.out.println("La división de las fracciones es: " + f1.dividir(f2).simplificar());


    }
    
}
