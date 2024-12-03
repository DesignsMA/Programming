package ahorcado;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class MainApp extends Application {
    protected static List<Usuario> usuarios = new ArrayList<>();
    protected static Usuario actual;
    protected static List<String> palabras = new ArrayList<>();

    @Override
    public void start(Stage stage) throws Exception {
        File file = new File("usuarios.bin");
        if (!file.exists()) { /* Validando existencia de archivos */
            AhorcadoIO.escribirBin("usuarios.bin", new ArrayList<Usuario>());
        }
        file = new File("archivoPalabras.txt");
        if (!file.exists()) {
            AhorcadoIO.escribirTexto("archivoPalabras.txt", "palabras.txt");
        }
        file = new File("palabras.txt");
        if (!file.exists()) {
            AhorcadoIO.escribirTexto("palabras.txt", "hola\nadios\nperro\ngato\npajaro\nleon\njirafa\nelefante\n");
        }

        usuarios = AhorcadoIO.obtenerUsuarios("usuarios.bin");

        Parent root = FXMLLoader.load(getClass().getResource("/registro.fxml"));
        Scene scene = new Scene(root);
        scene.getStylesheets().add(getClass().getResource("/styles.css").toExternalForm());
        stage.setTitle("Juego del Ahorcado - Iniciar Sesion");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }

}