public abstract class Termómetro implements Estadistica, Temperatura {
    private double grados;
    private double memoria[]; // Estatico de 5 temperaturas
    private int n;

    public Termómetro(double grados) {
        this.grados = grados;
        memoria = new double[5];
    }

    public double getGrados() {
        return grados;
    }

    public void setGrados(double grados) {
        this.grados = grados;
    }

    // Método abstracto
    public abstract double convertir();

    public void guardarEnMemoria() {
        if (n > 4)
            n = 0;
        memoria[n++] = grados;
    };

    public void resetearMemoria() {
        for (int i = 0; i < 5; i++) {
            memoria[i] = 0.0f;
        }
        n = 0;
    };

    public String imprimirMemoria() {
        String cad = "\n";
        for (int i = 0; i < 5; i++) {
            cad += Double.toString(memoria[i]) + '\n';
        }
        return cad;
    }

    // Implementamos las interfaces estadistica
    // Se deja al metodo abstracto de la interfaz
    // Temperatura como abstracto
    public double minimo() {
        double min = memoria[0];
        for (int i = 0; i < 5; i++)
            if (memoria[i] < min)
                min = memoria[i];
        return min;
    }

    public double maximo() {
        double max = memoria[0];
        for (int i = 0; i < 5; i++)
            if (memoria[i] > max)
                max = memoria[i];
        return max;
    }

    @Override
    public String toString() {
        return "Temperatura actual: " + grados;
    }

}