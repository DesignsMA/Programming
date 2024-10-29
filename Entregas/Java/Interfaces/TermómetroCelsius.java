public class TermómetroCelsius extends Termómetro {

    public TermómetroCelsius(double grados) {
        // Grados en celsius sistema métrico
        super(grados);// Inicializando atributos heredados
    }

    @Override
    public String determinarTemperatura() {
        if (super.getGrados() < 38f)
            return "Temperatura normal: " + super.getGrados() + "°C";
        else
            return "Fiebre: " + super.getGrados() + "°C";
    }

    @Override
    public double convertir() {
        return (super.getGrados()) * (9f / 5f) + 32;
    }

    @Override
    public String toString() {
        return super.toString() + "°C";
    }
}
