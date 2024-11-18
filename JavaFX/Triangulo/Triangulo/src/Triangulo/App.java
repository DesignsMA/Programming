package Triangulo;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Polygon;
import javafx.stage.Stage;

public class App extends Application {
    private Punto p1, p2, p3;
    private Triangulo triangulo;
    private TextArea outputArea;

    @Override
    public void start(Stage primaryStage) {
        p1 = new Punto();
        p2 = new Punto();
        p3 = new Punto();
        triangulo = new Triangulo(p1, p2, p3); /* Agregacion */
        Polygon trianguloF = new Polygon();
        trianguloF.setFill(Color.valueOf("#ff5353"));

        GridPane grid = new GridPane();
        // Establecer un padding (margen interno) de 10 píxeles alrededor del GridPane
        grid.setPadding(new Insets(10));
        // Establecer el espacio vertical (gap) entre las filas a 10 píxeles
        grid.setVgap(10);
        // Establecer el espacio horizontal (gap) entre las columnas a 10 píxeles
        grid.setHgap(10);

        // Labels y TextFields para puntos
        for (int i = 1; i <= 3; i++) {
            grid.add(new Label("P" + i + " X:"), 0, i); /* columna, fila */
            TextField xField = new TextField();
            grid.add(xField, 1, i);
            grid.add(new Label("P" + i + " Y:"), 2, i);
            TextField yField = new TextField();
            grid.add(yField, 3, i);

            int index = i;
            // Agregar listeners de cambios de texto para los campos X e Y de cada punto
            // Notifica al listener cada vez que el 'ObservableValue' textProperty cambia
            /*
             * Generalmente un textProperty hace uso de un ChangeListener, reducimos codigo
             * por medio de una funcion lambda que recibe los parametros de un
             * ChangeListener
             * https://docs.oracle.com/javafx/2/api/javafx/beans/value/ChangeListener.html
             * obs - ObservableValue textProperty
             * old - Valor viejo
             * newVal - Valor nuevo (El que notifica al listener)
             */

            xField.textProperty().addListener((obs, old, newVal) -> {
                // Convertir el nuevo valor ingresado a un número decimal
                double x = parseDouble(newVal);
                // Actualizar la coordenada X del punto correspondiente
                getPunto(index).setX(x);
            });
            yField.textProperty().addListener((obs, old, newVal) -> {
                // Parsear el nuevo valor ingresado a un número decimal
                double y = parseDouble(newVal);
                // Actualizar la coordenada Y del punto correspondiente
                getPunto(index).setY(y);
            });
        }

        // Crear botones para calcular Área y Perímetro
        Button areaBtn = new Button("Calcular Área");
        Button perimetroBtn = new Button("Calcular Perímetro");
        areaBtn.setMinWidth(100);
        perimetroBtn.setMinWidth(100);
        // Área de texto para mostrar los resultados
        outputArea = new TextArea();
        outputArea.setEditable(false); // Hacer que el área de texto no sea editable
        outputArea.setMaxHeight(30);

        // Definir la acción al hacer clic en el botón de Área
        areaBtn.setOnAction(e -> {
            outputArea.setText("Área: " + triangulo.Area());
            trianguloF.getPoints().clear();
            trianguloF.getPoints().addAll(new Double[] {
                    p1.getX(), p1.getY(),
                    p2.getX(), p2.getY(),
                    p3.getX(), p3.getY()
            });
        });

        // Definir la acción al hacer clic en el botón de Perímetro
        perimetroBtn.setOnAction(e -> {
            outputArea.setText("Perímetro: " + triangulo.Perimetro());
            trianguloF.getPoints().clear();
            trianguloF.getPoints().addAll(new Double[] {
                    p1.getX(), p1.getY(),
                    p2.getX(), p2.getY(),
                    p3.getX(), p3.getY()
            });
        });

        // Crear un contenedor horizontal para los botones con un espacio de 10 píxeles
        // entre ellos
        grid.add(areaBtn, 0, 4, 2, 1);
        grid.add(perimetroBtn, 3, 4, 2, 1);
        // Agregar los botones al GridPane, ocupando 4 columnas y 1 fila

        // Agregar el área de texto al GridPane, ocupando 4 columnas y 1 fila
        grid.add(outputArea, 0, 5, 4, 1);
        Group trianguloFig = new Group(trianguloF);
        grid.add(trianguloFig, 0, 6, 4, 1);

        // Crear una escena con el GridPane y establecer su tamaño
        Scene scene = new Scene(grid, 400, 300);

        // Configurar el título de la ventana principal
        primaryStage.setTitle("Triángulos en JavaFX");

        // Establecer la escena en el escenario principal
        primaryStage.setScene(scene);

        // Mostrar la ventana principal
        primaryStage.show();
    }

    // Método privado para obtener el punto correspondiente basado en el índice
    private Punto getPunto(int index) {
        switch (index) {
            case 1:
                return p1;
            case 2:
                return p2;
            case 3:
                return p3;
            default:
                return p1;
        }
    }

    // Método privado para convertir una cadena a un número decimal
    private double parseDouble(String value) {
        try {
            return Double.parseDouble(value); //
        } catch (NumberFormatException e) {
            return 0.0; // Retornar 0.0 si ocurre una excepción
        }
    }

    public static void main(String[] args) {
        launch(args); // Lanzar la aplicación JavaFX
    }
}
