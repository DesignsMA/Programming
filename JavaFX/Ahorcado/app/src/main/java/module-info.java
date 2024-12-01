module hellofx {
    requires javafx.controls;
    requires javafx.fxml;
    requires Transitive javafx.graphics;

    opens ahorcado to javafx.fxml;
    exports ahorcado;

}
