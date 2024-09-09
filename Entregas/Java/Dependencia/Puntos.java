package Entregas.Java.Dependencia;
import java.util.Scanner;
class Punto {
    private double x;
    private double y;

    public Punto () {
        x = 0;
        y = 0;
    }

    public Punto (double x, double y) {
        this.x = x;
        this.y = y;
    } 

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public double distancia (Punto p) { //Dependencia, hace uso de la clase punto temporalmente
        return Math.sqrt( Math.pow( (p.getX() - x), 2 ) + Math.pow( (p.getY() - y), 2 ) );
    }

    public Punto puntoMedio (Punto p) {
        return new Punto( (x + p.getX())/2, (y + p.getY())/2 );
    } 

    public String toString () {
        return "(" + x + ", " + y + ")";
    }

}

public class Puntos {
    public static void main ( String []args) {
        int opt;
        Scanner sc = new Scanner(System.in);
        Punto p1 = new Punto();
        Punto p2 = new Punto();
        do {
            System.out.println("\n1. Modificar los puntos\n2. Distancia\n3. Punto medio\n4. Imprimir puntos\n5. Salir");
            System.out.print(": ");
            opt = sc.nextInt();
            switch (opt) {

                case 1:
                    do {
                        System.out.println("\n1. Modificar punto 1\n2. Modificar punto 2\n3. Regresar");
                        System.out.print(": ");
                        opt = sc.nextInt();
                        switch (opt) {
                            case 1:
                                System.out.println("Introduce x: ");
                                p1.setX(sc.nextDouble());
                                System.out.println("Introduce y: ");
                                p1.setY(sc.nextDouble());
                                break;
                            
                            case 2:
                                System.out.println("Introduce x: ");
                                p2.setX(sc.nextDouble());
                                System.out.println("Introduce y: ");
                                p2.setY(sc.nextDouble());
                                break;

                            default:
                                break;
                        }
                        
                    } while (opt != 3);
                    break;
                
                case 2:
                    System.out.println("Distancia: " + p1.distancia(p2));
                    break;

                case 3: 
                    System.out.println("Punto medio: " + p1.puntoMedio(p2));
                    break;
                
                case 4:
                    System.out.println("Punto 1: " + p1);
                    System.out.println("Punto 2: " + p2);
                    break;
            
                default:
                    break;
            }
            
        } while (opt != 5);
        sc.close();
    }

}
