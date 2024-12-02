package ahorcado;

import java.io.IOException;

import javafx.fxml.FXML;
import javafx.scene.control.*;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javafx.scene.control.Alert.AlertType;

public class adminController {

    @FXML
    private TextField tf1;

    @FXML
    private PasswordField tf2;

    @FXML
    private Button btAceptar;

    @FXML
    private TextArea textArea; // texto de seccion 2

    private int idbt = 0;

    @FXML // especifica que es una funcion llamada por eventos
    private void handlePalabras() {
        textArea.setText("");
        mostrar(new Control[] { tf1, tf2, btAceptar }, false); // ocultar
        mostrar(new Control[] { tf1, btAceptar }, true); // mostrar
        idbt = 1;
    }

    @FXML
    private void handleAgregarAdmin() {
        textArea.setText("");
        mostrar(new Control[] { tf1, tf2, btAceptar }, false); // ocultar
        mostrar(new Control[] { tf1, tf2, btAceptar }, true); // mostrar
        idbt = 2;
    }

    @FXML
    private void handleRemoverJugador() {
        textArea.setText("");
        mostrar(new Control[] { tf1, tf2, btAceptar }, false); // ocultar
        mostrar(new Control[] { tf1, btAceptar }, true); // mostrar
        idbt = 3;
    }

    @FXML
    private void handleScoreboard() {
        textArea.setText("");
        mostrar(new Control[] { tf1, tf2, btAceptar }, false); // ocultar
        List<Jugador> jugadores = new ArrayList<>();
        for (Usuario usuario : MainApp.usuarios) {
            if (usuario instanceof Jugador) {
                jugadores.add((Jugador) usuario); // Hacemos un cast a Jugador
            }
        }

        jugadores.stream()
                .sorted((j1, j2) -> Integer.compare(j2.palabrasAcertadas, j1.palabrasAcertadas))
                .forEach(jugador -> {
                    // Concatenar el texto al TextArea
                    textArea.appendText(jugador.getUsername() + " - Acertadas: " + jugador.palabrasAcertadas + "\n");
                });
    }

    @FXML
    private void handleAceptar() {
        try {
            switch (idbt) {
                case 1: {
                    AhorcadoIO.leerPalabras(tf1.getText());
                    for (String cad : MainApp.palabras) {
                        textArea.setText(textArea.getText() + cad + "\n");
                    }
                    break;
                }

                case 2: {
                    String nombre = tf1.getText();
                    String password = tf2.getText();
                    boolean estado = false;
                    if (nombre.isBlank() || password.isBlank()) {
                        Alerta.mostrarAlerta(AlertType.ERROR, "ERROR", "No puedes colocar campos vacios", true);
                        break;
                    }

                    for (Usuario usr : MainApp.usuarios) {
                        if (usr.getUsername().equals(nombre)) {
                            Alerta.mostrarAlerta(AlertType.ERROR, "ERROR", "Usuario ya existente", true);
                            estado = true;
                            break;
                        }
                    }
                    if (!estado) { // Si no hubo error
                        MainApp.usuarios.add(new Administrador(nombre, password));
                        AhorcadoIO.escribirBin("usuarios.bin", MainApp.usuarios);
                    }
                    break;
                }

                case 3: {
                    String nombre = tf1.getText();
                    Iterator<Usuario> iterator = MainApp.usuarios.iterator();
                    while (iterator.hasNext()) { // remueve de forma segura
                        Usuario usr = iterator.next();
                        if (usr.getUsername().equals(nombre) && usr instanceof Jugador) {
                            iterator.remove(); // Elimina de la lista de forma segura
                            break;
                        }
                    }
                    AhorcadoIO.escribirBin("usuarios.bin", MainApp.usuarios);
                    textArea.setText(manejarUsuarios.listaATexto(MainApp.usuarios));
                }

                default:
                    break;
            }

        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al abrir archivo", e.getMessage(), true);

        }
        mostrar(new Control[] { tf1, tf2, btAceptar }, false); // ocultar

    }

    private void mostrar(Control[] controles, boolean valor) {
        for (Control control : controles) {
            control.setVisible(valor);
            control.setManaged(valor);
        }
    }

}
