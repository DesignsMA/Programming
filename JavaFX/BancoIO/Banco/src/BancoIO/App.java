package BancoIO;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.InputMismatchException;

import org.w3c.dom.css.CSSStyleDeclaration;

import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.css.*;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.scene.layout.Background;
import javafx.scene.layout.HBox;
import javafx.scene.control.Label;
import javafx.scene.control.Button;
import javafx.scene.control.Control;
import javafx.scene.control.TextField;
import javafx.event.EventHandler;
import javafx.event.ActionEvent;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.Node;

public class App extends Application {
    Button b1, b2, b3, b4, b5, b6;
    Label l1, l2;
    TextField tf1, tf2;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage escenario) {
        VBox c1 = new VBox();
        HBox c11 = new HBox();
        c1.setAlignment(Pos.CENTER);
        c1.setSpacing(20);
        c11.setAlignment(Pos.CENTER);
        c11.setSpacing(10);
        b1 = new Button("Agregar cuenta");
        b2 = new Button("Depositar");
        b3 = new Button("Retirar");
        b4 = new Button("Mostrar Cuentas");
        b5 = new Button("Salir");
        b6 = new Button("ACEPTAR");
        l1 = new Label();
        l2 = new Label();
        tf1 = new TextField();
        tf2 = new TextField();
        b6.setVisible(false);
        b6.setManaged(false);
        c11.getChildren().addAll(tf1, tf2);
        for (Node nd : c11.getChildren()) {
            ((TextField) nd).setAlignment(Pos.CENTER);
            ((TextField) nd).setVisible(false);
            ((TextField) nd).setManaged(false);
            ((TextField) nd).setMinSize(105, 50);
        }
        c1.getChildren().addAll(b1, b2, b3, b4, b5, l1, c11, l2, b6);
        for (Node nd : c1.getChildren()) {
            if (nd instanceof Label) {
                ((Label) nd).setAlignment(Pos.CENTER);
                ((Label) nd).setVisible(false);
                ((Label) nd).setManaged(false);
            } else if (nd instanceof Button) {
                ((Button) nd).setAlignment(Pos.CENTER);
                ((Button) nd).setMinSize(220, 60);
            }
        }

        // Agregar funcionalidad, en lugar de sustituir cada listener, hacemos uso de un
        // listener general
        /*
         * La funcion lambda recibe un ActionEvent e como parametro y c1 el contenedor
         * de los componentes de la ventana
         * el evento 'e' es generador por el boton cuando se hace click en el
         * este evento es enviado a listener como parametro
         */

        Banco b = new Banco(50);
        try {
            BancoIO.leerArchivo("file.txt", b);
        } catch (FileNotFoundException e) {
            Alert a = new Alert(AlertType.WARNING);
            a.setTitle("Error");
            a.setContentText("Archivo no encontrado\n" + e.getStackTrace());
            a.showAndWait();
        }
        b1.setOnAction(e -> listener(e, c1, b));
        b2.setOnAction(e -> listener(e, c1, b));
        b3.setOnAction(e -> listener(e, c1, b));
        b4.setOnAction(e -> listener(e, c1, b));
        b5.setOnAction(e -> listener(e, c1, b));

        Scene escena = new Scene(c1, 720, 500);
        // Agregar escena a escenario.
        escenario.setScene(escena);
        // Escenario
        escenario.setTitle("BANCO");
        escenario.show();

    }

    public void alerta(String msg) {
        Alert a = new Alert(AlertType.WARNING);
        a.setTitle("Error");
        a.setContentText(msg);
        a.showAndWait();
    }

    public void nuevaCuenta(int n, double b, Banco banco) {
        CuentaBancaria cuenta;
        n = Integer.parseInt(tf1.getText());
        b = Double.parseDouble(tf2.getText());
        cuenta = new CuentaBancaria(b, n);
        banco.agregarCuenta(cuenta);
    }

    public void listener(ActionEvent e, VBox contenedor, Banco banco) {
        // Hide all controls in the container initially
        for (Node nd : contenedor.getChildren()) {
            if (nd instanceof Control) {
                nd.setVisible(false);
                nd.setManaged(false); // Ensure it doesn't occupy space
            }
        }

        try {
            // Variables for potential use
            int noCuenta = 0;
            double balance = 0;
            CuentaBancaria cuenta;
            if (banco.getNoC() > 0) {
                cuenta = banco.getCuentas()[banco.getNoC() - 1];
            }

            // Check which button triggered the event
            if (e.getSource() == b1) { // Add account button
                l1.setText("Introduce los datos de la cuenta");
                l1.setVisible(true);
                l1.setManaged(true);

                tf1.setPromptText("Número de cuenta");
                tf2.setPromptText("Balance inicial");
                tf1.setVisible(true);
                tf2.setVisible(true);
                tf1.setManaged(true);
                tf2.setManaged(true);

                b6.setVisible(true);
                b6.setManaged(true);

                // Set action for Aceptar button
                b6.setOnAction(evento -> {
                    try {
                        nuevaCuenta(noCuenta, balance, banco);
                        // Notify user
                        l2.setText("Cuenta agregada exitosamente\n" + banco.getCuentas()[banco.getNoC() - 1]);
                        l2.setVisible(true);
                        l2.setManaged(true);

                        // Hide input fields and Aceptar button
                        tf1.setVisible(false);
                        tf2.setVisible(false);
                        tf1.setManaged(false);
                        tf2.setManaged(false);
                        b6.setVisible(false);
                        b6.setManaged(false);
                    } catch (NumberFormatException ex) {
                        alerta("Por favor, introduce valores numéricos válidos.");
                    } catch (IllegalArgumentException e2) {
                        alerta(e2.getMessage());
                    } catch (RuntimeException e3) {
                        alerta(e3.getMessage());
                    }
                });
            }

        } catch (IllegalArgumentException e2) {
            alerta(e2.getMessage());
        } catch (RuntimeException e3) {
            alerta(e3.getMessage());
        }
    }
}
