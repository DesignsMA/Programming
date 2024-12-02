module hellofx {
    requires transitive javafx.controls;
    requires javafx.fxml;
    requires transitive javafx.graphics;

    opens ahorcado to javafx.fxml;

    exports ahorcado;

}
