import java.util.Scanner;
import java.util.Random;

class Cafetera {
    int capacidadMaxima;
    int cantidadActual;
    String sabor;

    //Constructores
    public Cafetera () {
        capacidadMaxima = 1000;
        cantidadActual = 0;
    }

    public Cafetera (int ml) {
        capacidadMaxima = ml;
        cantidadActual = ml;
    }

    public Cafetera (int capacidadMaxima, int cantidadActual) {
        cantidadActual = Math.abs(cantidadActual);
        this.capacidadMaxima = Math.abs(capacidadMaxima);

        if ( cantidadActual > capacidadMaxima) {
            this.cantidadActual = capacidadMaxima;
        } else this.cantidadActual = cantidadActual;
                
    }
    //Accedentes y mutadores

    public int getCapacidadMaxima () { return capacidadMaxima;}
    public int getCantidadActual () { return cantidadActual;}
    public String getSabor () { return sabor; }
    
    public void setCapacidadMaxima (int capacidadMaxima) { this.capacidadMaxima = capacidadMaxima; }
    public void setCantidadActual (int cantidadActual) {
        if ( cantidadActual > capacidadMaxima) {
            this.cantidadActual = capacidadMaxima;
        } else this.cantidadActual = cantidadActual;
     }
    public void setSabor (String sabor) { this.sabor = sabor; }

     //Metodos definidos por el usuario

     public void llenarCafetera () {
            cantidadActual = capacidadMaxima;
     }

     public void servirTaza (int ml) {
        ml = Math.abs(ml);
        System.out.println("\nSirviendo una taza de cafe "+ sabor);
        if ( ml > cantidadActual ) {
            System.out.println("\nNo hay suficiente cafe para llenar la taza, tu taza fue llenada: " + cantidadActual + " ml.");
            cantidadActual = 0;
        } else cantidadActual -= ml;
     }

     public void agregarCafe (int ml) {
        ml = Math.abs(ml);
        int sobrante = cantidadActual+ml-capacidadMaxima;
        if ( cantidadActual + ml <= capacidadMaxima ) {
            cantidadActual += ml;
        } else {
            cantidadActual = capacidadMaxima;
            System.out.println("\n"+sobrante+" ml se han regado");
        }
     }

     public void vaciarCafetera () {
            cantidadActual = 0;
     }

     public String toString () {
            return "Cafetera[Capacidad Maxima: " + capacidadMaxima + "Cantidad Actual: " + cantidadActual + "Sabor: " + sabor + "]";
     }
}

public class Cafe {
    private static String [] sabores = { "Java", "Americano", "Capuccino", "Moka", "Espresso", "Colombiano", "Frances", "Italiano" };

    public static void main(String[] args) {
        Random rand = new Random();
        Scanner sc = new Scanner(System.in);
        Cafetera c1 = new Cafetera(4000,3450);
        c1.setSabor(sabores[rand.nextInt(8)]);
        int opcion = 0;

        do {
            System.out.println("\nCafe " + c1.getSabor() + " restante: " + c1.getCantidadActual() + " ml");
            System.out.println("\n1. Llenar cafetera\n2. Servir taza\n3. Agregar cafe\n4. Vaciar cafetera\n5. Salir\n");
            System.out.print(": " );
            opcion = sc.nextInt();
            switch (opcion) {
                case 1:
                    c1.llenarCafetera();
                    break;
                case 2:
                    System.out.println("\n¿Cuantos ml de cafe quieres servir?");
                    c1.servirTaza(sc.nextInt());
                    break;
                
                case 3:
                    System.out.println("\n¿Cuantos ml de cafe quieres agregar?");
                    c1.agregarCafe(sc.nextInt());
                    break;

                case 4:
                    c1.vaciarCafetera();
                    break;
            
                default:
                    break;
            }
            
        } while (opcion != 5);
        sc.close();

    }
}
