class ItemCompra { // Clase padre | superclass
    private String nombre;
    private double precioUnidad;

    ItemCompra ( String n, double p ) {
        nombre = n;
        precioUnidad = p;
    }

    ItemCompra ( ) {
        this.nombre = "Sin item";
        this.precioUnidad = 0.0f;
    }

    public double getPrecio() { 
        return precioUnidad; //Precio unitario no ponderado
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    public void setPrecioUnidad(double precioUnidad) {
        this.precioUnidad = precioUnidad;
    }

    public String toString() {
        return nombre + "@" + precioUnidad;
    }
}

class ItemPonderado extends ItemCompra {
    private double kg; //El precioUnidad equivale a precio por kg

    ItemPonderado () {
        super(); //Instanciar clase padre | super class y loa atributos que hereda
        kg = 0.0f;
    }

    ItemPonderado ( String n, double p, double kg ) {
        super(n, p); //Instanciar por parametros y heredar
        this.kg = kg;
    }

    public double getKg() {
        return kg;
    }

    public void setKg(double kg) {
        this.kg = kg;
    }

    @Override //Especificar el reemplazo de la funcion getPrecio
    public double getPrecio () {
        return kg*super.getPrecio(); //Precio = kg*precioUnitario
    }

    @Override
    public String toString () {
        return super.toString() + " " + kg + " " + getPrecio() + " SR";
    }

}

class ItemContabilizado extends ItemCompra {
    private int unidades;

    ItemContabilizado () {
        super();
        this.unidades = 0;
    }

    ItemContabilizado ( String n, double p, int u) {
        super(n,p);
        u = Math.abs(u);
        if ( u >=1 )
            unidades = u;
        else
            unidades = 1;
    }

    public int getUnidades() {
        return unidades;
    }

    public void setUnidades(int unidades) {
        this.unidades = unidades;
    }

    @Override
    public double getPrecio() {
        return unidades*super.getPrecio();
    }

    @Override
    public String toString() {
        return super.toString() + " " + unidades + "  Unidades " + getPrecio() + " SR";
    }
}

public class Herencia {
    public static void main(String[] args) {
        ItemCompra iCom = new ItemCompra("Paleta", 10);
        ItemPonderado iPon = new ItemPonderado("Azúcar", 22.5, 2.5);
        ItemContabilizado iCon = new ItemContabilizado("Paleta", 10, 25);
        System.out.println(iCom +"\n" + iPon + "\n" + iCon);
    }
}