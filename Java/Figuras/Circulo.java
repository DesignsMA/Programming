package Figuras;

public class Circulo {
    private double radio;
    private String color;

    public Circulo ( double radio, String color) {
        this.radio = radio;
        this.color = color;
    }

    public double getRadio ( ) { return radio; }

    public String getColor ( ) { return color; }

    public void setRadio ( double radio) { this.radio = radio; }

    public void setColor ( String color) { this.color = color; }

    public double area ( ) {
        return Math.PI * Math.pow(radio, 2); //PI*r^2
    }

    public double perimetro ( ) {
        return 2 * Math.PI * radio; //2*PI*r
    }

    public String toString ( ) {
        return "Circulo [radio=" + radio + ", color=" + color + "]";
    }

}
