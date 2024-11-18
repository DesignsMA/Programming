package Triangulo;

import java.util.Scanner;

class Recta {
    private Punto p1;
    private Punto p2;

    public Recta() {
        p1 = new Punto();
        p2 = new Punto();
    }

    public Recta(Punto p1, Punto p2) {
        this.p1 = p1;
        this.p2 = p2;
    }

    public Recta(double x1, double y1, double x2, double y2) {
        p1 = new Punto(x1, y1);
        p2 = new Punto(x2, y2);
    }

    public Punto getP1() {
        return p1;
    }

    public Punto getP2() {
        return p2;
    }

    public void setP1(Punto p1) {
        this.p1 = p1;
    }

    public void setP2(Punto p2) {
        this.p2 = p2;
    }

    public double pendiente() {
        return (p2.getY() - p1.getY()) / (p2.getX() - p1.getX());
    }

    public double distanciaPunto(Punto p) {
        double m = pendiente();
        double b = p1.getY() - m * p1.getX();
        return Math.abs(m * p.getX() - p.getY() + b) / Math.sqrt(Math.pow(m, 2) + 1);

    }

    public double Longitud() {
        return p1.distancia(p2);
    }

    public String toString() {
        return "P1: " + p1 + " P2: " + p2 + "\ny = " + pendiente() + "x + (" + (p1.getY() - p1.getX() * pendiente())
                + ")";
    }
}

class Punto {
    private double x;
    private double y;

    public Punto() {
        x = 0;
        y = 0;
    }

    public Punto(double x, double y) {
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

    public double distancia(Punto p) { // Dependencia, hace uso de la clase punto temporalmente
        return Math.sqrt(Math.pow((p.getX() - x), 2) + Math.pow((p.getY() - y), 2));
    }

    public Punto puntoMedio(Punto p) {
        return new Punto((x + p.getX()) / 2, (y + p.getY()) / 2);
    }

    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}

class Triangulo {
    private Punto p1, p2, p3;

    public Triangulo() {
        p1 = new Punto();
        p2 = new Punto();
        p3 = new Punto();
    }

    public Triangulo(Punto p1, Punto p2, Punto p3) {
        this.p1 = p1;
        this.p2 = p2;
        this.p3 = p3;
    }

    public Punto getP1() {
        return p1;
    }

    public Punto getP2() {
        return p2;
    }

    public Punto getP3() {
        return p3;
    }

    public void setP1(Punto p1) {
        this.p1 = p1;
    }

    public void setP2(Punto p2) {
        this.p2 = p2;
    }

    public void setP3(Punto p3) {
        this.p3 = p3;
    }

    public double Altura() { // No es obligatorio que p2-p3 sea la base
        Recta base = Base();
        Punto[] puntos = { p1, p2, p3 };
        for (Punto punto : puntos) {
            if (punto != base.getP1() && punto != base.getP2()) {
                return base.distanciaPunto(punto);
            }
        }
        return 0.0;
    }

    public Recta Base() { // Encuentra el lado mayor ( base ) y retorna la recta correspondiente
        double[] distancias = { p1.distancia(p2), p1.distancia(p3), p2.distancia(p3) };
        if (distancias[0] == Math.max(Math.max(distancias[0], distancias[1]), distancias[2])) { // Si la recta de p1-p2
                                                                                                // es la mayor de las
                                                                                                // otras
            return new Recta(p1, p2);
        } else if (distancias[1] == Math.max(Math.max(distancias[0], distancias[1]), distancias[2])) { // Si no si la
                                                                                                       // recta de
                                                                                                       // p1-p3...
            return new Recta(p1, p3);
        } else { // Si no la recta de p2-p3 es la mayor
            return new Recta(p2, p3);
        }
    }

    public double Perimetro() {
        return p1.distancia(p2) + p1.distancia(p3) + p2.distancia(p3);
    }

    public double Area() {
        return (Base().Longitud() * Altura()) / 2;
    }

}

public class Triangulos {
    public static void main(String[] args) {
        int opt;
        Scanner sc = new Scanner(System.in);
        Punto p1 = new Punto(2, 0);
        Punto p2 = new Punto(3, 4);
        Punto p3 = new Punto(-2, 5);
        Triangulo t = new Triangulo(p1, p2, p3);
        do {
            System.out.println(
                    "\n1. Modificar los puntos\n2. Altura\n3. Base\n4. Perimetro\n5. Area\n6. Imprimir puntos\n7. Salir");
            System.out.print(": ");
            opt = sc.nextInt();
            switch (opt) {

                case 1:
                    do {
                        System.out.println(
                                "\n1. Modificar punto 1\n2. Modificar punto 2\n3. Modificar punto 3\n4. Regresar");
                        System.out.print(": ");
                        opt = sc.nextInt();
                        switch (opt) {
                            case 1:
                                System.out.print("x: ");
                                p1.setX(sc.nextDouble());
                                System.out.print("y: ");
                                p1.setY(sc.nextDouble());
                                break;
                            case 2:
                                System.out.print("x: ");
                                p2.setX(sc.nextDouble());
                                System.out.print("y: ");
                                p2.setY(sc.nextDouble());
                                break;
                            case 3:
                                System.out.print("x: ");
                                p3.setX(sc.nextDouble());
                                System.out.print("y: ");
                                p3.setY(sc.nextDouble());
                                break;
                        }
                    } while (opt != 4);
                    break;
                case 2:
                    System.out.println("Altura: " + t.Altura());
                    break;
                case 3:
                    System.out.println("Base: " + t.Base() + " Longitud: " + t.Base().Longitud());
                    break;
                case 4:
                    System.out.println("Perimetro: " + t.Perimetro());
                    break;
                case 5:
                    System.out.println("Area: " + t.Area());
                    break;
                case 6:
                    System.out.println("P1: " + p1 + " P2: " + p2 + " P3: " + p3);
                    break;
            }
        } while (opt != 7);
    }
}
