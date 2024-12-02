package ahorcado;

import javafx.scene.control.Alert;

public class Alerta {

    public static void mostrarAlerta(Alert.AlertType tipo, String titulo, String msg, boolean bloquear) {
        Alert alert = new Alert(tipo);
        alert.setTitle(titulo);
        alert.setContentText(msg);
        if (bloquear) {
            alert.showAndWait();
        } else
            alert.show();
    }
}