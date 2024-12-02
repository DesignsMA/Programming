package ahorcado;

import java.util.List;

public class Administrador extends Usuario {
    private static final long serialVersionUID = 1L;
    private String password;

    // Constructor
    public Administrador(String username, String password) {
        super(username);
        this.password = password;
    }

    // Getter
    public String getPassword() {
        return password;
    }

    // Métodos específicos del administrador
    public void eliminarJugador(List<Jugador> jugadores, String username) { // recibe una lista de jugadores
        jugadores.removeIf(jugador -> jugador.getUsername().equals(username));
    }

    public void cargarPalabrasDesdeArchivo(String archivo) {
        // Aquí se puede implementar la lectura de palabras desde un archivo
        System.out.println("Palabras cargadas desde el archivo: " + archivo);
    }

    public void mostrarTablaDePosiciones(List<Jugador> jugadores) {
        // Ordenar jugadores por palabras acertadas y mostrar
        jugadores.stream()
                .sorted((j1, j2) -> Integer.compare(j2.palabrasAcertadas, j1.palabrasAcertadas))
                .forEach(jugador -> System.out
                        .println(jugador.getUsername() + " - Acertadas: " + jugador.palabrasAcertadas));
    }

    @Override
    public void mostrarEstadisticas() {

    }

    @Override
    public String toString() {
        return "Administrador{username='" + username + "'}";
    }
}