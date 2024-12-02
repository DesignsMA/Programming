package ahorcado;

import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.File;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import javafx.scene.control.Alert;

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

    @SuppressWarnings("unchecked")
    public static List<Usuario> obtenerUsuarios(String archivo)
            throws IOException, ClassNotFoundException {
        List<Usuario> usuarios;
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(archivo));
        usuarios = (List<Usuario>) ois.readObject();
        ois.close();
        return usuarios;
    }

}