public class TermómetroFahrenheit extends Termómetro {

    public TermómetroFahrenheit(double grados) {
        // Grados en farenheit sistema imperial
        super(grados);// Inicializando atributos heredados
    }

    @Override
    public String determinarTemperatura() {
        if (super.getGrados() < 100.4f)
            return "Temperatura normal: " + super.getGrados() + "°F";
        else
            return "Fiebre: " + super.getGrados() + "°F";
    }

    @Override
    public double convertir() {
        return (super.getGrados() - 32) * (5f / 9f);
    }

    @Override
    public String toString() {
        return super.toString() + "°F";
    }

}