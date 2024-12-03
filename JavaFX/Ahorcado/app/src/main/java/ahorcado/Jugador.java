package ahorcado;

public class Jugador extends Usuario {
    public int palabrasAcertadas;
    public int palabrasErradas;
    public int intentosRealizados;
    public boolean activo;

    // Constructor
    public Jugador(String username) {
        super(username);
        this.palabrasAcertadas = 0;
        this.palabrasErradas = 0;
        this.intentosRealizados = 0;
        activo = false;
    }

    // Métodos específicos del jugador
    public void adivinarPalabra(boolean acierto) {
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

    public void actualizarIntentos(int intentos) {
        this.intentosRealizados += intentos;

    }

    public String mostrarEstadisticas() {
        return ("Estadísticas de " + username + ":\n\n" + "Palabras acertadas: " + palabrasAcertadas + "\n\nPalabras erradas: " + palabrasErradas + "\n" + //
                        "\n" + //
                        "Número de intentos: " + intentosRealizados);
    }

    public void switchActivo() {
        activo = !activo;
    }

    @Override
    public String toString() {
        return "Jugador{username='" + username + "', palabras acertadas=" + palabrasAcertadas + "}";
    }
}
