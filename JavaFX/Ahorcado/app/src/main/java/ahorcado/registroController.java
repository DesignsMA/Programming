package ahorcado;

import java.io.IOException;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class registroController {

    @FXML
    private TextField usernameField;

    @FXML
    private PasswordField passwordField;

    // Método para manejar el login como jugador
    @FXML
    private void handleJugadorLogin() {
        String username = usernameField.getText(); // obtener nombre

        if (username.isEmpty()) {
            Alerta.mostrarAlerta(AlertType.WARNING, "ALERTA", "El usuario no puede estar vacio.", true);
            return;
        }

        // Verificar si es un jugador (por ejemplo, verificando que no sea un
        // administrador)

        if (isJugador(username)) {
            loadJugadorScene();
        }

    }

    // Método para manejar el login como administrador
    @FXML
    private void handleAdminLogin() {
        String username = usernameField.getText();
        String password = passwordField.getText();

        if (username.isEmpty() || password.isEmpty()) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error", "El usuario y contraseña no pueden estar vacios.", true);
            return;
        }

        // Verificar credenciales del administrador
        if (isAdmin(username, password)) {
            loadAdminScene();
        } else {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error", "Credenciales invalidas", true);
        }
    }

    // Verificar si el usuario es un jugador
    private boolean isJugador(String username) {
        try {
            MainApp.usuarios = AhorcadoIO.obtenerUsuarios("usuarios.bin");
            for (Usuario usuario : MainApp.usuarios) { // recorrer lista
                if (usuario instanceof Jugador)
                    if (usuario.getUsername().equals(username)) { // Si el jugador existe
                        MainApp.actual = usuario;
                        return true;
                    }
            }
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al abrir archivo", e.getMessage(), true);
        } catch (ClassNotFoundException e2) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Clase no encontrada", e2.getMessage(), true);
        }
        /* Si el usuario no existe */
        try {
            if (!manejarUsuarios.encontrarUsuario(MainApp.usuarios, username)) {
                manejarUsuarios.agregarJugador(username);
                Alerta.mostrarAlerta(AlertType.CONFIRMATION, "", "Usuario agregado exitosamente!", true);
                AhorcadoIO.escribirBin("usuarios.bin", MainApp.usuarios);
            }

        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al abrir archivo", e.getMessage(), true);
        }

        return false;
    }

    // Verificar si el usuario es un administrador
    private boolean isAdmin(String username, String password) {
        if (username.equals("foxypato") && password.equals("admin123"))
            return true;

        try {
            MainApp.usuarios = AhorcadoIO.obtenerUsuarios("usuarios.bin");
            for (Usuario usuario : MainApp.usuarios) { // recorrer lista
                if (usuario instanceof Administrador)
                    if (usuario.getUsername().equals(username)
                            && ((Administrador) usuario).getPassword().equals(password)) { // Si el jugador existe
                                                                                           // en
                        // la lista
                        MainApp.actual = usuario;
                        return true;
                    }
            }
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al abrir archivo", e.getMessage(), true);
        } catch (ClassNotFoundException e2) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Clase no encontrada", e2.getMessage(), true);
        }
        return false;
    }

    // Cargar la escena de jugador
    private void loadJugadorScene() {
        try {
            Parent loader = FXMLLoader.load(getClass().getResource("/jugador.fxml"));
            Scene scene = new Scene(loader); // cargar scena
            scene.getStylesheets().add(getClass().getResource("/styles.css").toExternalForm()); /* Recuperar estilos */
            Stage stage = (Stage) usernameField.getScene().getWindow(); // recuperar escenario
            stage.setScene(scene);
            stage.setTitle("Juego del Ahorcado - Jugador");
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al cargar la escena jugador", e.getMessage(), true);
        }
    }

    // Cargar la escena de administrador
    private void loadAdminScene() {
        try {
            Parent admin = FXMLLoader.load(getClass().getResource("/admin.fxml"));
            Scene scene = new Scene(admin); // cargar scena
            scene.getStylesheets().add(getClass().getResource("/styles.css").toExternalForm()); /* Recuperar estilos */
            Stage stage = (Stage) usernameField.getScene().getWindow(); // recuperar escenario
            stage.setScene(scene);
            stage.setTitle("Juego del Ahorcado - Administrador");
        } catch (IOException e) {
            Alerta.mostrarAlerta(AlertType.ERROR, "Error al cargar la escena admin", e.getMessage(), true);
        }
    }

}
