import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.scene.control.Label;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.event.EventHandler;
import javafx.event.ActionEvent;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;

public class Archivos extends Application {
    public static void main(String[] args) {
        Banco b = new Banco(50);
        try {
            BancoIO.leerArchivo("file.txt", b);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        System.out.println(b);
    }
}