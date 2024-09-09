package Clases;
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

    public int getDia() {
        return dia;
    }

    public int getMes() {
        return mes;
    }

    public int getAnio() {
        return anio;
    }

    public void setDia(int dia) {
        this.dia = dia;
    }

    public void setMes(int mes) {
        this.mes = mes;
    }

    public void setAnio(int anio) {
        this.anio = anio;
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

    public int diasMes () { //No parametrizado
        if ( mes == 2 ) {
            if ( bisiesto(anio) ) {
                return 29;
            } else {
                return 28;
            }
        } else if ( mes == 4 || mes == 6 || mes == 9 || mes == 11 ) {
            return 30;
        } else {
            return 31;
        }
    }

    public int diasMes (int a, int mes) { //Parametrizado
        if ( mes == 2 ) {
            if ( bisiesto(a) ) {
                return 29;
            } else {
                return 28;
            }
        } else if ( mes == 4 || mes == 6 || mes == 9 || mes == 11 ) {
            return 30;
        } else {
            return 31;
        }
    }

    public int diasTranscurridos ( ) {
        int dt = -1; //Desfase de 1 dia
        for ( int a = 1900; a <= anio ; a++) {
            for ( int m = 1; m <= 12; m++) {
                if ( m == mes && a == anio ) {
                    dt += dia;
                    break; //Si se ha llegado a fecha actual, salir
                } else {
                    dt += diasMes(a,m); //dias del mes en el año
                }
            }
        } 
        return dt;
    }

    public int diaSemana() { //congruencia de zeller https://es.wikipedia.org/wiki/Congruencia_de_Zeller
        int q = dia;
        int m = mes;
        int y = anio;

        if (m == 1 || m == 2) {
            m += 12;
            y -= 1;
        }

        int k = y % 100;
        int j = y / 100;

        int h = (q + (13 * (m + 1)) / 5 + k + (k / 4) + (j / 4) + (5 * j)) % 7;

        // Ajustar el resultado para que 0 sea domingo y 6 sea sábado
        int diaSemana = (h + 5) % 7;

        return diaSemana;
    }
    
    public String corta () {
         return dia + "-" + mes + "-" + anio;
    }

    public String larga () {
        String[] dias = {"Lunes", "Martes", "Miercoles", "Jueves",  "Viernes", "Sábado", "Domingo"};
        String[] meses = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
        return dias[diaSemana()] + " " + dia + " de " + meses[mes-1] + " de " + anio;
    }

    public void fechaTras ( long  f ) { //Recibe fecha en formato númerico
        int d,m,a;
        f += 1; //Desfase de 1 en lenguaje natural 
        for ( a = 1900; a <= 2050 ; a++) {
            for ( m = 1; m <= 12; m++) {
                for ( d = 1; d <= diasMes(a,m); d++) {
                    f--;
                    if ( f == 0 ) {
                        dia = d;
                        mes = m;
                        anio = a;
                    }
                }
            }
        } 
    }

    public void siguiente () {
        if ( mes == 12 && anio == 2050 && dia == diasMes()) {
            dia = 1;
            mes = 1;
            anio = 1900;
        } else if ( dia+1 > diasMes()) 
        {
            dia = 1;
            if ( mes+1 > 12 ) {
                mes = 1;
                anio += 1;
            } else {
                mes += 1;
            }
        } else {
            dia +=1;
        }
    }

    public void anterior () {
        if ( mes == 1 && dia == 1 && anio == 1900) {
            dia = 31;
            mes = 12;
            anio = 2050;
        } else if ( dia-1 < 1 ) 
        {
            if ( mes-1 < 1 ) {
                mes = 12;
                anio -= 1;
            } else {
                mes -= 1;
            }
            dia = diasMes(); //El mes cambia
        } else {
            dia -=1;
        }
    }

    public String toString () {
        return dia + "-" + mes + "-" + anio;
    }
}

public class Fechas {
    
    public static void main (String []args) {
        Fecha f1;
        Scanner sc = new Scanner( System.in );
        int d,m,a, opt;
        System.out.println("\nIngrese la fecha en formato dd-mm-aaaa ( 1-1-1900 - 31-12-2050 )");
        System.out.print("Dia: ");
        d = sc.nextInt();
        System.out.print("Mes: ");
        m = sc.nextInt();
        System.out.print("Año: ");
        a = sc.nextInt();
        f1 = new Fecha(d, m, a);

        do {
            System.out.println("1. Mostrar fecha en formato corto");
            System.out.println("2. Mostrar fecha en formato largo");
            System.out.println("3. Mostrar días transcurridos desde el 1-1-1900");
            System.out.println("4. Mostrar día de la semana");
            System.out.println("5. Mostrar fecha tras n días");
            System.out.println("6. Mostrar fecha siguiente");
            System.out.println("7. Mostrar fecha anterior");
            System.out.println("8. Salir");
            System.out.println("Seleccione una opción: ");
            opt = sc.nextInt();

            switch ( opt ) {
                case 1:
                    System.out.println(f1.corta());                    
                    break;
                
                case 2:
                    System.out.println(f1.larga());
                    break;
                
                case 3:
                    System.out.println("Días transcurridos desde el 1-1-1900: " + f1.diasTranscurridos());
                    break;
                
                case 4:
                    System.out.println("Dia de la semana: " + (f1.diaSemana()+1));
                    break;
                
                case 5:
                    System.out.println("Ingresa el número de dias transcurridos desde el 1-1-1900: ");
                    long dias = sc.nextLong();
                    f1.fechaTras(dias);
                    System.out.println(f1.larga());
                    break;
                
                case 6:
                    f1.siguiente();
                    System.out.println("Fecha siguiente: " + f1);
                    break;
                
                case 7:
                    f1.anterior();
                    System.out.println("Fecha anterior: " + f1);
                    break;
            
                default:
                    break;
            }            
        } while (opt != 8);
        sc.close();
    }

    
}
