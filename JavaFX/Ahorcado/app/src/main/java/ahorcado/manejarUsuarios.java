package ahorcado;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

import javafx.scene.control.Alert.AlertType;

public class manejarUsuarios {

    public static void encontrarUsuario(List<Usuario> usuarios) {

    }

    public static void agregarJugador(String username) {
        try {
            MainApp.usuarios.add(new Jugador(username));
            AhorcadoIO.escribirBin("usuarios.bin", MainApp.usuarios);
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al abrir archivo", e.getMessage(), true);
        }
    }

    public static String listaATexto(List<Usuario> lista) {
        String cadenaFinal = lista.stream()
                .map(Object::toString)
                .collect(Collectors.joining("\n"));
        return cadenaFinal;
    }

}
