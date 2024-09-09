package Entregas.Java.Cartesiano;

public class Punto {
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
