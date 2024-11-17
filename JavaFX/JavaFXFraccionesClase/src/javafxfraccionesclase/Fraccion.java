package javafxfraccionesclase;


public class Fraccion {
        private int n;
    private int d;

    public Fraccion() {
        n = 0;
        d = 1;
    }

    public Fraccion(int n, int d) {
        this.n = n;
        this.d = d;
    }

    public int getN() {
        return n;
    }

    public void setN(int n) {
        this.n = n;
    }

    public int getD() {
        return d;
    }

    public void setD(int d) {
        this.d = d;
    }
    
    public Fraccion sumar(Fraccion f){
        int nr, dr;
        nr = n*f.getD()+d*f.getN();
        dr = d*f.getD();
        return new Fraccion(nr,dr);
    }
    
    public Fraccion restar(Fraccion f){
        int nr, dr;
        nr = n*f.getD()-d*f.getN();
        dr = d*f.getD();
        return new Fraccion(nr,dr);
    }
    
    public Fraccion multiplicar(Fraccion f){
        int nr, dr;
        nr = n*f.getN();
        dr = d*f.getD();
        return new Fraccion(nr,dr);
    }
    
    public Fraccion dividir(Fraccion f){
        int nr, dr;
        nr = n*f.getD();
        dr = d*f.getN();
        return new Fraccion(nr,dr);
    }
    
    @Override
    public String toString(){
        return n+"/"+d;
    }

}
