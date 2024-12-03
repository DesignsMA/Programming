package ahorcado;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

public class tabla {

    public static String tablaGen() {

        List<Jugador> jugadores = new ArrayList<>();
        for (Usuario usuario : MainApp.usuarios) {
            if (usuario instanceof Jugador) {
                jugadores.add((Jugador) usuario); // Hacemos un cast a Jugador
            }
        }

        AtomicInteger position = new AtomicInteger(1);

        String resultado = jugadores.stream()
                // Ordenar por la diferencia de acertadas menos erradas (descendente)
                .sorted((j1, j2) -> Integer.compare(
                        (j2.palabrasAcertadas - j2.palabrasErradas),
                        (j1.palabrasAcertadas - j1.palabrasErradas)))
                .map(jugador -> position.getAndIncrement() + ". "
                        + jugador.getUsername()
                        + " | Acertadas: " + jugador.getPalabrasAcertadas()
                        + " | Erradas: " + jugador.getPalabrasErradas() + "\n\n")
                .collect(Collectors.joining("\n")); // Unir con saltos de línea

        return resultado;
    }

}
