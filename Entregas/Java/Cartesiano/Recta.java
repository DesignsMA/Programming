package Entregas.Java.Cartesiano;

public class Recta {
    private Punto p1;
    private Punto p2;

    public Recta() {
        p1 = new Punto();
        p2 = new Punto();
    }

    public Recta ( Punto p1, Punto p2) {
        this.p1 = p1;
        this.p2 = p2;
    }

    public Recta ( double x1, double y1, double x2, double y2) {
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

    public double pendiente () {
        return (p2.getY() - p1.getY()) / (p2.getX() - p1.getX());
    }

    public double distanciaPunto ( Punto p ) {
        double m = pendiente();
        return Math.abs( m*p.getX() - p.getY() -m*p1.getX() + p1.getY())/Math.sqrt( Math.pow(m, 2) +1  );
    }

    public String toString () {
        return "P1: " + p1 + " P2: " + p2 + "\ny = " + pendiente() + "x + (" + ( p1.getY() -p1.getX()*pendiente()) + ")";
    }



}

