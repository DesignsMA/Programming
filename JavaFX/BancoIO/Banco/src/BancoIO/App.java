package BancoIO;

import java.io.FileNotFoundException;
import java.util.InputMismatchException;

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

public class App extends Application {
    Button b1, b2, b3, b4, b5;
    Label l1, l2;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage escenario) {
        VBox c1 = new VBox();
        c1.setAlignment(Pos.CENTER);
        c1.setSpacing(20);

        b1 = new Button("Agregar cuenta");
        b1.setAlignment(Pos.CENTER);
        b2 = new Button("Depositar");
        b2.setAlignment(Pos.CENTER);
        b3 = new Button("Retirar");
        b3.setAlignment(Pos.CENTER);
        b4 = new Button("Mostrar Cuentas");
        b4.setAlignment(Pos.CENTER);
        b5 = new Button("Salir");
        b5.setAlignment(Pos.CENTER);
        c1.getChildren().addAll(b1, b2, b3, b4, b5);

        /*
         * // Agregar funcionalidad
         * ButtonListener escucha = new ButtonListener();
         * b1.setOnAction(escucha);
         * b2.setOnAction(escucha);
         * b3.setOnAction(escucha);
         * b4.setOnAction(escucha);
         */
        Scene escena = new Scene(c1, 720, 500);
        // Agregar escena a escenario.
        escenario.setScene(escena);
        // Escenario
        escenario.setTitle("BANCO");
        escenario.show();

        Banco b = new Banco(50);
        try {
            BancoIO.leerArchivo("file.txt", b);
        } catch (FileNotFoundException e) {
            Alert a = new Alert(AlertType.WARNING);
            a.setTitle("Error");
            a.setContentText("Archivo no encontrado\n" + e.getStackTrace());
            a.showAndWait();
        }

    }
}