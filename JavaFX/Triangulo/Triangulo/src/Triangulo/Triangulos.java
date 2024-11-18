package Triangulo;

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

    public double Altura() {
        Recta base = Base();
        Punto puntoFueraBase = null; // Punto que no está en la base
        if (!base.getP1().equals(p1) && !base.getP2().equals(p1)) {
            puntoFueraBase = p1;
        } else if (!base.getP1().equals(p2) && !base.getP2().equals(p2)) {
            puntoFueraBase = p2;
        } else {
            puntoFueraBase = p3;
        }
        // Calcular la distancia del punto fuera de la base a la recta base
        return base.distanciaPunto(puntoFueraBase);
    }

    public double Area() {
        double baseLongitud = Base().Longitud();
        double altura = Altura();
        return (baseLongitud * altura) / 2;
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

}

public class Triangulos {
    public static void main(String[] args) {
        // ....
    }
}
