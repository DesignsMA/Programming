import java.util.Scanner;
import java.util.Random;

/* Parcial 2 | Programacion II
    Erika Bonfil Barragan
    Ciprian Romero Marco Antonio | 202325419
     */

class Carnivoro {
    private String alimentos[];

    public Carnivoro () {
        alimentos = new String[3];
        alimentos[0] = "Pescado";
        alimentos[1] = "Pollo";
        alimentos[2] = "Puerco";
    }

    public String[] getAlimentos() {
        return alimentos;
    }
}

abstract class Felino extends Carnivoro { //Clase abstracta, cazar es abstracto
    private String nombre;
    private int vidas;

    public Felino ( String n, int v) {
        super(); //Instanciar carnivoro
        nombre = n;
        vidas = v;
    }

    public String getNombre() {
        return nombre;
    }

    public int getVidas() {
        return vidas;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setVidas(int vidas) {
        this.vidas = vidas;
    }

    public String Comer() {
        Random r = new Random();
        return "\n" +nombre + " comio " + (super.getAlimentos())[r.nextInt(3)];
    }

    public abstract String cazar(); //Método abstracto

    @Override
    public String toString() {
        return "Soy " + nombre;
    }
}

class Leon extends Felino {

    public Leon ( String n) {
        super(n,1);
    }

    @Override
    public String cazar() {
        return "El leon " + super.getNombre() + " ha cazado una cebra.";
    }

    public void rugir() {
        System.out.println( super.getNombre() + ": Roaaar!!!");
    }

    @Override
    public String toString() {
        return super.toString() + ", un leon";
    }
}

class Gato extends Felino {

    public Gato ( String n ) {
        super(n, 7);
    }

    @Override
    public String cazar() {
        return "El gato " + super.getNombre() + " ha cazado un raton.";
    }

    public void ronronear() {
        System.out.println( super.getNombre() + ": Brrrrrr");
    }

    @Override
    public String toString() {
        return super.toString() + ", un gato y tengo " + super.getVidas() + " vidas";
    }

    }

public class Felinos {

    public static void Expresar ( Felino felinos[]) {
        for ( Felino f: felinos) {
            if ( f instanceof Leon ) 
                ((Leon)f).rugir(); //Cast explicito
            else
                ((Gato)f).ronronear();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner( System.in);
        int opc = 0;
        Felino felinos[] = new Felino[5];
        felinos[0] = new Leon("Mufasa");
        felinos[1] = new Gato("Felix");
        felinos[2] = new Leon("Scar");
        felinos[3] = new Gato("Garfield");
        felinos[4] = new Gato("Cremita");


        do {
            System.out.print("1. Alimentar felinos\n2. Cazar\n3. Expresar\n4. Salir\n: ");
            opc = sc.nextInt();

            switch (opc) {
                case 1:
                for ( Felino f: felinos) {
                    System.out.println(f.Comer());
                }   
                    break;

                case 2:
                for ( Felino f: felinos) {
                    System.out.println( "\n" + f.cazar());
                }
                break;

                case 3:
                Expresar(felinos);
                break;
            
                default:
                    break;
            }
        } while ( opc != 4);

        sc.close();
    }
}