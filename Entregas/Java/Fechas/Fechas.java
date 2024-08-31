package Entregas.Java.Fechas;
import java.util.Scanner;
class Fecha {
    private int dia;
    private int mes;
    private int anio;

    Fecha () {
        dia = 1;
        mes = 1;
        anio = 1900;
    }

    Fecha (int d, int m, int a) {
         if ( valida(d, m, a) ) {
            dia = d;
            mes = m;
            anio = a;
         } else {
            dia = 1;
            mes = 1;
            anio = 1900;
         }
    }

    public boolean bisiesto (int a) {
        //Solo se aceptan fechas de 1900-2050, no checamos por anios seculares
        return a%4 == 0;//1 si bisiesto
    }

    private boolean valida ( int d, int m, int a ) {
        //a (entre el 1-1-1900 y el 31-12-2050); si
        //no cumple con estas condiciones, se asignará la fecha 1-1-1900.

        if ( a < 1900 || a > 2050 || d > 31 || d < 1 || m > 12 || m < 1) {
            System.out.println("Fecha no valida");
            return false;
        }


        if ( bisiesto(a) && m == 2 && d > 29) { //Si es bisiesto y febrero
            System.out.println("Febrero no puede tener un dia mayor a 29 en anio bisiesto");
            return false;
        } else if (bisiesto(a) == false && m == 2 && d > 28) { // Si solo es febrero
            System.out.println("Febrero no puede tener un dia mayor a 28 en anio no bisiesto");
            return false;
        } else if ( ( m == 4 || m == 6 || m == 9 || m == 11 ) && d > 30 ) { //Si es mes de 30 dias
            System.out.println("El mes " + m + " no puede tener mas de 30 dias");
            return false;
        }
        return true;
    }

    public String toString () {
        return dia + "-" + mes + "-" + anio;
    }
}

public class Fechas {
    
    public static void main (String []args) {
        Fecha f1 = new Fecha(32,13,2051);
        Fecha f2 = new Fecha();
        Fecha f3 = new Fecha(29,2,2000);
        Fecha f4 = new Fecha(29,2,2001);
        Fecha f5 = new Fecha(30,4,2000);
        Fecha f6 = new Fecha(31,6,2000);
        Fecha f7 = new Fecha(31,9,2000);

        System.out.println();
        System.out.println(f1);
        System.out.println(f2);
        System.out.println(f3);
        System.out.println(f4);
        System.out.println(f5);
        System.out.println(f6);
        System.out.println(f7);

    }

    
}
