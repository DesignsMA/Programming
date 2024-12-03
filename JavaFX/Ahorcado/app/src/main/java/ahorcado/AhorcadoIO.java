package ahorcado;

import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.FileInputStream;
import java.io.File;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.Iterator;
import java.lang.Object;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Control;
import javafx.stage.Stage;

public class AhorcadoIO {
    // Función para escribir una lista de jugadores en un archivo binario
    public static void escribirBin(String archivo, List<Usuario> usuarios) throws IOException {
        // Escribir la lista de jugadores en el archivo binario
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(archivo));
        oos.writeObject(usuarios); // escribir lista
        oos.close();
    }

    public static void leerPalabras(String archivo) throws IOException {
        MainApp.palabras.clear();

        Scanner sc = new Scanner(new File(archivo));
        while (sc.hasNext()) { // Mientras el escaner pueda leer
            MainApp.palabras.add(sc.nextLine());
        }
        sc.close();

    }

    public static void escribirTexto(String archivo, String texto) throws IOException {
        try (FileWriter writer = new FileWriter(archivo)) {
            writer.write(texto);
        }
    }

    // Lee el contenido de un archivo y lo devuelve como un String
    public static String leerTexto(String archivo) throws IOException {
        String out;
        Scanner sc = new Scanner(new File(archivo));
        out = sc.nextLine();
        sc.close();
        return out;
    }

    @SuppressWarnings("unchecked")
    public static List<Usuario> obtenerUsuarios(String archivo)
            throws IOException, ClassNotFoundException {
        List<Usuario> usuarios;
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(archivo));
        usuarios = (List<Usuario>) ois.readObject();
        ois.close();
        return usuarios;
    }

    // Función para eliminar una palabra de la lista en memoria
    public static void eliminarPalabra(String palabra) {
        MainApp.palabras.remove(palabra);
    }

    // Función para actualizar un usuario en el archivo binario
    public static void actualizarUsuario(String archivo, Usuario usuarioActualizado)
            throws IOException, ClassNotFoundException {
        List<Usuario> usuarios = obtenerUsuarios(archivo);
        for (int i = 0; i < usuarios.size(); i++) {
            if (usuarios.get(i).getUsername().equals(usuarioActualizado.getUsername())) {
                usuarios.set(i, usuarioActualizado);
                break;
            }
        }
        escribirBin(archivo, usuarios);
    }
}