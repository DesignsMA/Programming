import java.util.Scanner;
class Fecha {
    private int dia;
    private int mes;
    private int anio;

    public Fecha (int d, int m, int a) {
        dia = d;
        mes = m;
        anio = a;
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

    public boolean bisiesto ( int a ) {
        return a % 4 == 0; //1 if true
    }

    public boolean validar(int d, int m, int a) {
        if ( m< 1 || m > 12 || d > 31 || d < 1 || a < 1950 ) return false;
        if ( m == 2 && bisiesto(a) && d > 29 ) return false;
        if ( m == 2 && !bisiesto(a) && d > 28 ) return false;
        if ( (m == 4 || m == 6 || m == 9 || m == 11) && d > 30 ) return false;
        return true;
    }

    public boolean igual( Fecha f ) { //Dependencia
        return (anio == f.getAnio() && mes == f.getMes() && dia == f.getDia());
    }

    public String toString () {
        return dia + "/" + mes + "/" + anio;
    }
}

class Viaje {
    private Fecha f;
    private double tarifa, kilometros;

    public Viaje ( Fecha f,  double t, double k) {
        this.f = f;
        tarifa = t;
        kilometros = k;
    }

    public double getTarifa ()  { return tarifa;}
    public double getKilometros ()  { return kilometros;}
    public Fecha getFecha () {return f;}

    public double coste () { return tarifa* kilometros;}

    public String toString () {
        return "Fecha: " + f + " Coste: " + coste() + " Tarifa: " + tarifa + " Kilometros: " + kilometros;
    }   
}

class Conductor {
    private static int c;
    private String nombre;
    private Viaje viajes[];
    private int n, id;

    public Conductor ( String n ) {
        id = c;
        c++;
        nombre = n;
        viajes = new Viaje [3];
    }

    public Viaje[] getViajes () { return viajes;}

    public void agregar ( Viaje v ) {
        if (n < 3) {
            viajes[n] = v;
            n++;
        } else System.out.println( " Viajes máximos alcanzados");
    }

    public double ganancias ( Fecha f ) {
        double gan = 0;
        for (Viaje v: viajes) {
            if ( f.igual(v.getFecha()) ) {
                gan += v.coste();
            }
        }
        return gan;
    }

    public String toString () {
        return "Conductor: " + nombre + " id: " + id;
    }
    

}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner( System.in);
        System.out.println("Nombre del conductor: ");
        Conductor c1 = new Conductor( sc.nextLine());
        Fecha f = new Fecha(10,9,2024);
        int d,m,a;
        double tarifa, kilometros;
        for (int i = 0; i <3 ; i++ ) {
            do {
                System.out.println("Ingrese la fecha: 1900-2050 formato: dd-mm-aaaa");
                System.out.println("Dia: ");
                 d = sc.nextInt();
                System.out.println("Mes: ");
                 m = sc.nextInt();
                System.out.println("Año: ");
                 a = sc.nextInt();
                                
                System.out.println("Ingrese la tarifa: ");
                    tarifa = sc.nextDouble();
                System.out.println("Ingrese los kilometros: ");
                    kilometros = sc.nextDouble();
                
                if (tarifa <= 0 || kilometros <= 0 || !f.validar(d, m, a)) {
                    System.out.println("Datos incorrectos");
                }
            } while ( tarifa <= 0 || kilometros <= 0 || !f.validar(d, m, a));
            c1.agregar( new Viaje(new Fecha(d,m,a), tarifa, kilometros));
        }

        System.out.println( c1 + "\nGanancias de : " + f + "\n" + c1.ganancias(f) + "\nViajes:\n");
        for ( Viaje viajes: c1.getViajes()) {
            System.out.println(viajes);
        }
        sc.close();




    }
}
