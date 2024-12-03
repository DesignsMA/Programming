package ahorcado;

import java.io.File;
import java.io.IOException;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javafx.scene.control.Alert.AlertType;
import javafx.stage.Stage;

public class adminController {

    @FXML
    private TextField tf1;

    @FXML
    private PasswordField tf2;

    @FXML
    private Button btAceptar;

    @FXML
    private Button btMenu;

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
        textArea.setText(tabla.tablaGen());
    }

    @FXML
    private void handleReturn() {
        try {
            Parent parent = FXMLLoader.load(getClass().getResource("/registro.fxml"));
            Scene scene = new Scene(parent); // cargar scena
            scene.getStylesheets().add(getClass().getResource("/styles.css").toExternalForm()); /* Recuperar estilos */
            Stage stage = (Stage) textArea.getScene().getWindow(); // recuperar escenario
            stage.setScene(scene);
            stage.setTitle("Juego del Ahorcado - Iniciar Sesion");
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al cargar la escena menu", e.getMessage(), true);
        }
    }

    @FXML
    private void handleAceptar() {
        try {
            switch (idbt) {
                case 1: {
                    /* Actualizamos el archivo que apunta a palabras */
                    File file = new File(tf1.getText());
                    if (file.exists()) {
                        AhorcadoIO.escribirTexto("archivoPalabras.txt", tf1.getText());
                        AhorcadoIO.leerPalabras(AhorcadoIO.leerTexto("archivoPalabras.txt"));
                        for (String cad : MainApp.palabras) {
                            textArea.setText(textArea.getText() + cad + "\n");
                        }
                    } else
                        Alerta.mostrarAlerta(AlertType.WARNING, "ADVERTENCIA",
                                "Archivo no existente\nLas palabras no se actualizaron", false);

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
                            Alerta.mostrarAlerta(AlertType.INFORMATION, "Jugador " + nombre + " eliminado.",
                                    "Visualize usuarios actuales.",
                                    false);
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
