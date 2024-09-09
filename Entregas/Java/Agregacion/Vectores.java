import java.util.Scanner;

class Vector {
    private double x,y,z;
    public Vector(){
        x = 0;
        y = 0;
        z = 0;
    }

    public Vector(double x, double y, double z){
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double getZ() {
        return z;
    }

    public void setX(double x) {
        this.x = x;
    }

    public void setY(double y) {
        this.y = y;
    }

    public void setZ(double z) {
        this.z = z;
    }

    public double magnitud() {
        return Math.sqrt( Math.pow(x,2) + Math.pow(y,2) + Math.pow(z,2) );
    }

    public Vector vectorUnitario() {
        double magnitud = magnitud();
        return new Vector( x/magnitud, y/magnitud, z/magnitud );
    }

    public Vector productoEscalar(double escalar) {
        return new Vector( x*escalar, y*escalar, z*escalar );
    }

    public Vector sumaVectorial(Vector v) {
        return new Vector( x + v.getX(), y + v.getY(), z + v.getZ() );
    }

    public double productoPunto(Vector v) {
        return x*v.getX() + y*v.getY() + z*v.getZ();
    }

    public Vector productoCruz(Vector v) {
        return new Vector( y*v.getZ() - z*v.getY(), z*v.getX() - x*v.getZ(), x*v.getY() - y*v.getX() );
    }

    public String toString() {
        return "(" + x + ", " + y + ", " + z + ")";
    }
}

class paralelepipedo {
    private Vector v1,v2,v3;

    public paralelepipedo() {
        v1 = new Vector();
        v2 = new Vector();
        v3 = new Vector();
    }

    public paralelepipedo( Vector v1, Vector v2, Vector v3) {
        this.v1 = v1;
        this.v2 = v2;
        this.v3 = v3;
    }

    public Vector getV1() {
        return v1;
    }

    public Vector getV2() {
        return v2;
    }

    public Vector getV3() {
        return v3;
    }

    public void setV1(Vector v1) {
        this.v1 = v1;
    }

    public void setV2(Vector v2) {
        this.v2 = v2;
    }

    public void setV3(Vector v3) {
        this.v3 = v3;
    }

    public double volumen() {
        return Math.abs( v1.productoCruz(v2).productoPunto(v3) ); //Base x Altura (|(uxv)*w|)
    }

    public String toString() {
        return "V1: " + v1 + " V2: " + v2 + " V3: " + v3;
    }


}

public class Vectores {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Vector v1 = new Vector(7,-1,3); //Referencian a la direccion de memoria que contiene al objeto
        Vector v2 = new Vector(20,7,14);
        Vector v3 = new Vector(-5,12,15);
        double x = 0,y = 0,z = 0;
        int opt;
        paralelepipedo p = new paralelepipedo(v1,v2,v3); //Agregación | El objeto recibe una variable externa que referencia a una direccion de memoria

        do {
            System.out.println("1. Leer vectores\n2. Calcular volumen\n3. Imprimir vectores del paralelepipedo\n4. Salir");
            System.out.print(": ");
            opt = sc.nextInt();
            switch (opt) {
                case 1:
                    do {
                        System.out.print("\n1. Vector 1\n2. Vector 2\n3. Vector 3\n5. Salir\n: ");
                        opt = sc.nextInt();
                        if ( opt >= 1 && opt <= 3) {
                            System.out.print("\nX: ");
                            x = sc.nextDouble();
                            System.out.print("\nY: ");
                            y = sc.nextDouble();
                            System.out.print("\nZ: ");
                            z = sc.nextDouble();
                        }
                        switch (opt) {
                            case 1:
                                p.setV1( new Vector(x,y,z) ); //Composición | El objeto contiene una referencia a una direccion de memoria
                                break;
                            
                            case 2:
                                p.setV2( new Vector(x,y,z) );
                                break;
                            
                            case 3:
                                p.setV3( new Vector(x,y,z) );
                                break;
                        
                            default:
                                break;
                        }
                    } while (opt != 5);
                    break;
                
                case 2:
                    System.out.println("\nVolumen: " + p.volumen() + "\n");
                    break;
                
                case 3:
                    System.out.println("\n" + p + "\n");
                    break;
            
                default:
                    break;
            }
            
        } while (opt != 4);
        System.out.println(p.volumen());
        sc.close();
    }
    
    
}
