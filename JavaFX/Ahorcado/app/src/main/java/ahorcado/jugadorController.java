package ahorcado;

import javafx.fxml.FXML;
import javafx.scene.control.TextField;
import javafx.scene.text.Text;

public class jugadorController {
    @FXML
    private TextField palabraField;

    @FXML
    private Text palabrasAcertadas;

    @FXML
    public Text palabrasErradas;

    private void handleScoreboard() {
        // Logica para el scoreboard
    }

    private boolean esPalabraCorrecta(String letra) {
        
        boolean acierto = false;
        letra = letra.toLowerCase();

        for(int i; i < MainApp.palabra.length(); i++) {
            if(MainApp.palabra.charAt(i) == letra.charAt(0)) {
                palabraAdivinada.setCharAt(i, )
                acierto = true;
            }
        }

        //Logica para verificar si la palabra es correcta

        
        ((Jugador)MainApp.actual).adivinarPalabra(boolean);
    }

    private void actualizarEstadisticas() {
        palabrasAcertadas
    }

}