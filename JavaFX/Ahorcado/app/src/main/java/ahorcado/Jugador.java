package ahorcado;

public class Jugador extends Usuario {
    public int palabrasAcertadas;
    public int palabrasErradas;
    public int intentosRealizados;

    // Constructor
    public Jugador(String username) {
        super(username);
        this.palabrasAcertadas = 0;
        this.palabrasErradas = 0;
        this.intentosRealizados = 0;
    }

    // Métodos específicos del jugador
    public void adivinarPalabra(boolean acierto) {
        intentosRealizados++;
        if (acierto) {
            palabrasAcertadas++;
        } else {
            palabrasErradas++;
        }
    }

    public int getIntentosRealizados() {
        return intentosRealizados;
    }

    public int getPalabrasAcertadas() {
        return palabrasAcertadas;
    }

    public int getPalabrasErradas() {
        return palabrasErradas;
    }

    public void setIntentosRealizados(int intentosRealizados) {
        this.intentosRealizados = intentosRealizados;
    }

    public void setPalabrasAcertadas(int palabrasAcertadas) {
        this.palabrasAcertadas = palabrasAcertadas;
    }

    public void setPalabrasErradas(int palabrasErradas) {
        this.palabrasErradas = palabrasErradas;
    }

    public void mostrarEstadisticas() {
        System.out.println("Estadísticas de " + username + ":");
        System.out.println("Palabras acertadas: " + palabrasAcertadas);
        System.out.println("Palabras erradas: " + palabrasErradas);
        System.out.println("Número de intentos: " + intentosRealizados);
    }

    @Override
    public String toString() {
        return "Jugador{username='" + username + "', palabras acertadas=" + palabrasAcertadas + "}";
    }
}
