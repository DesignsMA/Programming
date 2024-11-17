package javafxfraccionesclase;

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

public class Principal extends Application{
    TextField tf1, tf2, tf3, tf4, tf5, tf6;
    Button b1, b2, b3, b4;
    Label l1;
    
//    public void listener(ActionEvent e){
//        int n1, d1, n2, d2;
//            try{
//                n1 = Integer.parseInt(tf1.getText());
//                d1 = Integer.parseInt(tf2.getText());
//                n2 = Integer.parseInt(tf3.getText());
//                d2 = Integer.parseInt(tf4.getText());
//                Fraccion f1 = new Fraccion(n1,d1);
//                Fraccion f2 = new Fraccion(n2,d2);
//                Fraccion f3;
//
//                if(e.getSource() == b1){
//                    f3 = f1.sumar(f2);
//                    l1.setText("+");
//                }
//                else{
//                    if(e.getSource() == b2){
//                        f3 = f1.restar(f2);
//                        l1.setText("-");
//                    }
//                    else{
//                        if(e.getSource() == b3){
//                            f3 = f1.multiplicar(f2);
//                            l1.setText("X");
//                        }
//                        else{
//                            f3 = f1.dividir(f2);
//                            l1.setText("/");
//                        }
//                    }
//                }
//
//                tf5.setText(f3.getN()+"");
//                tf6.setText(f3.getD()+"");
//            }
//            catch(NumberFormatException e1){
//                Alert a = new Alert(AlertType.WARNING);
//                a.setTitle("Error");
//                a.setContentText("Ingresa la fracción");
//                a.showAndWait();
//            }
//    }
//    
    public static void main(String[] args) {
        launch(args);
        
    }
    @Override
    public void start(Stage escenario){
        //Diseño
        VBox root1 = new VBox();
        HBox root11 = new HBox();
        HBox root12 = new HBox();
        VBox root111 = new VBox();
        VBox root112 = new VBox();
        VBox root113 = new VBox();
        root11.setSpacing(20);
        root11.setAlignment(Pos.CENTER);
        root12.setSpacing(20);
        root12.setAlignment(Pos.CENTER);
        root1.setSpacing(20);
        
        //Controles
        tf1 = new TextField("");
        tf2 = new TextField("");
        tf3 = new TextField("");
        tf4 = new TextField("");
        tf5 = new TextField("");
        tf6 = new TextField("");
        
        tf1.setMaxWidth(50);
        tf2.setMaxWidth(50);
        tf3.setMaxWidth(50);
        tf4.setMaxWidth(50);
        tf5.setMaxWidth(50);
        tf6.setMaxWidth(50);
        tf5.setEditable(false);
        tf6.setEditable(false);
        
        b1 = new Button("Sumar");
        b2 = new Button("Restar");
        b3 = new Button("Multiplicar");
        b4 = new Button("Dividir");
        l1 = new Label("+");
        
        
        //Agregar controles al diseño
        root111.getChildren().addAll(tf1, tf2);
        root112.getChildren().addAll(tf3, tf4);
        root113.getChildren().addAll(tf5, tf6);
        
        root11.getChildren().addAll(root111,l1,root112,new Label("="),root113);
        root12.getChildren().addAll(b1, b2, b3, b4);
        
        root1.getChildren().addAll(root11, root12);
        
        //Agregar funcionalidad
        ButtonListener escucha = new ButtonListener();
        b1.setOnAction(escucha);
        b2.setOnAction(escucha);
        b3.setOnAction(escucha);
        b4.setOnAction(escucha);
        
        //b1.setOnAction(e->listener(e));
        //b2.setOnAction(e->listener(e));
        //b3.setOnAction(e->listener(e));
        //b4.setOnAction(e->listener(e));
        
        //Crear escena con diseño
        Scene escena = new Scene(root1,300,100);
        
        //Agregar escena a escenario.
        escenario.setScene(escena);
        //Escenario
        escenario.setTitle("Calculadora de fracciones");
        escenario.show();
    }
    
    public class ButtonListener implements EventHandler<ActionEvent>{

        @Override
        public void handle(ActionEvent e) {
            int n1, d1, n2, d2;
            try{
                n1 = Integer.parseInt(tf1.getText());
                d1 = Integer.parseInt(tf2.getText());
                n2 = Integer.parseInt(tf3.getText());
                d2 = Integer.parseInt(tf4.getText());
                Fraccion f1 = new Fraccion(n1,d1);
                Fraccion f2 = new Fraccion(n2,d2);
                Fraccion f3;

                if(e.getSource() == b1){
                    f3 = f1.sumar(f2);
                    l1.setText("+");
                }
                else{
                    if(e.getSource() == b2){
                        f3 = f1.restar(f2);
                        l1.setText("-");
                    }
                    else{
                        if(e.getSource() == b3){
                            f3 = f1.multiplicar(f2);
                            l1.setText("X");
                        }
                        else{
                            f3 = f1.dividir(f2);
                            l1.setText("/");
                        }
                    }
                }

                tf5.setText(f3.getN()+"");
                tf6.setText(f3.getD()+"");
            }
            catch(NumberFormatException e1){
                Alert a = new Alert(AlertType.WARNING);
                a.setTitle("Error");
                a.setContentText("Ingresa la fracción");
                a.showAndWait();
            }
        }
    }
}
