package ahorcado;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.Alert.AlertType;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Date;
import java.util.Random;

public class jugadorController {

    private int intentos;
    private StringBuilder palabra;
    private StringBuilder palabraOculta;

    @FXML
    private Label textArea;

    @FXML
    private Label ahorcadoText, intentosLabel;

    @FXML
    private TextField palabraField;

    @FXML
    private Button btEnviar, btTabla, btEstadisticas, btJugar, btAceptar;

    private String randomPalabra() {

        try {
            /* Almacena el arreglo (lista) de cadenas en MainApp.palabras */
            AhorcadoIO.leerPalabras(AhorcadoIO.leerTexto("archivoPalabras.txt"));
            Random rand = new Random((new Date()).getTime());
            int index = rand.nextInt(MainApp.palabras.size()); // elegir palabra aleatoria
            return MainApp.palabras.get(index);
        }

        catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al abrir archivo", e.getMessage(), true);
            return "";
        }

    }

    @FXML
    private void handleJugar() {

        intentos = 5;
        palabra = new StringBuilder(randomPalabra()); // inicializar palabra
        palabraOculta = new StringBuilder(palabra); // palabra oculta de ese tamaño

        for (int i = 0; i < palabra.length(); i++) {
            palabraOculta.setCharAt(i, '_');
        }

        intentosLabel.setText("Intentos: " + intentos);
        ahorcadoText.setText(palabraOculta.toString());
        mostrar(new Control[] { btJugar }, false);
        mostrar(new Control[] { ahorcadoText, palabraField, btEnviar, intentosLabel }, true);

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
    private void handleEnviarPalabra() {
        String letra = palabraField.getText().toLowerCase();
        if (letra.isEmpty() || letra.length() > 1 || letra.charAt(0) < 'a' || letra.charAt(0) > 'z') {
            Alerta.mostrarAlerta(Alert.AlertType.WARNING, "ALERTA", "Por favor ingresa una sola letra (a-z).", true);
            return;
        }

        intentosLabel.setText("Intentos: " + intentos);
        boolean acierto = esPalabraCorrecta(letra);
        intentosLabel.setText("Intentos: " + intentos);
        palabraField.clear();
    }

    private boolean esPalabraCorrecta(String letra) {
        char car = palabraField.getText().toLowerCase().charAt(0);
        boolean acierto = false;

        boolean found = false, repeated = false;
        for (int i = 0; i < palabraOculta.length(); i++) {
            if (palabraOculta.charAt(i) == car) {
                Alerta.mostrarAlerta(AlertType.WARNING, "", "Letra ya encontrada", true);
                found = true;
                repeated = true;
                break;
            }
        }

        if (!repeated) { // si no repetida
            for (int i = 0; i < palabra.length(); i++) {
                if (palabra.charAt(i) == car) {
                    palabraOculta.setCharAt(i, car);
                    found = true;
                }
            }
            if (!found) { // if not found
                intentos--;
                if (intentos != 0)
                    Alerta.mostrarAlerta(AlertType.WARNING, "", "Letra incorrecta!", false);
            }
            repeated = false;
        }

        if (intentos > 0 && palabraOculta.toString().equals(palabra.toString())) {
            ((Jugador) MainApp.actual).adivinarPalabra(found);
            Alerta.mostrarAlerta(Alert.AlertType.INFORMATION, "GANASTE!",
                    "", true);
            mostrar(new Control[] { btJugar }, true);
            mostrar(new Control[] { ahorcadoText, palabraField, btEnviar, intentosLabel }, false);

        } else if (intentos <= 0) {
            ((Jugador) MainApp.actual).adivinarPalabra(found);
            Alerta.mostrarAlerta(Alert.AlertType.INFORMATION, "PERDISTE! :C",
                    "La palabra era: " + palabra, true);
            mostrar(new Control[] { btJugar }, true);
            mostrar(new Control[] { ahorcadoText, palabraField, btEnviar, intentosLabel }, false);
        }

        ahorcadoText.setText(palabraOculta.toString());

        try {
            AhorcadoIO.escribirBin("usuarios.bin", MainApp.usuarios); // actualizar listado
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "ERROR", "Archivo no abierto.", true);
        }

        return found;
    }

    @FXML
    private void handleEstadisticasPersonales() {
        Jugador jugador = (Jugador) MainApp.actual;
        textArea.setText("");
        mostrar(new Control[] { btEstadisticas, btTabla }, false);
        mostrar(new Control[] { textArea, btAceptar }, true);
        textArea.setText(
                "Jugador: " + jugador.getUsername() + "\n\nPalabras acertadas: " + jugador.palabrasAcertadas
                        + "\n\nPalabras erradas: " + jugador.palabrasErradas);
    }

    @FXML
    private void handleTablaPosiciones() {
        textArea.setText("");
        mostrar(new Control[] { btEstadisticas, btTabla }, false);
        mostrar(new Control[] { textArea, btAceptar }, true);
        textArea.setText(tabla.tablaGen());
    }

    @FXML
    private void handleAceptar() {
        mostrar(new Control[] { btEstadisticas, btTabla }, true);
        mostrar(new Control[] { textArea, btAceptar }, false);

    }

    private void mostrar(Control[] controles, boolean valor) {
        for (Control control : controles) {
            control.setVisible(valor);
            control.setManaged(valor);
        }
    }
}