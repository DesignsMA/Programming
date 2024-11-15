
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import javax.print.DocFlavor.READER;

public class ArchivosPre {
        /*
         * Absolute path direccion que empieza desde la raiz del sistema hasta la
         * direccion donde se ubica la entidad
         * i.e direccion absoluta del programa ejecutado
         * "D:\Users\sepma\Downloads\Data\C728\Git\C-C++-C#\C\git\Entregas\Java"
         * Relative path direccion relativo a otra direccion, i.e La direccion relativa
         * al programa ejecutado es ""
         */
        public static void main(String[] args) {
                File f = new File("temp");
                String datos = "Lorem Ipsum Docet";
                byte[] bytes = datos.getBytes();
                FileOutputStream writer;
                FileInputStream reader;
                f.mkdir(); // Crear directorio en la ubicacion del ejecutable
                f = new File(f.getAbsolutePath() + File.separator + "name.txt");

                try {
                        f.createNewFile(); // Crear archivo en directorio
                        writer = new FileOutputStream(f);
                        reader = new FileInputStream(f);
                        writer.write(bytes);
                        String input = new String(reader.readAllBytes());
                        System.out.println(input);

                } catch (IOException e2) {
                        System.out.println("El archivo no fue creado");
                }

                // apply File class methods on File object
                System.out.println("File name :" + f.getName());
                System.out.println("Path: " + f.getPath());
                System.out.println("Absolute path:"
                                + f.getAbsolutePath());
                System.out.println("Parent:" + f.getParent());
                System.out.println("Exists :" + f.exists());

                if (f.exists()) {
                        System.out.println("Is writable:"
                                        + f.canWrite());
                        System.out.println("Is readable" + f.canRead());
                        System.out.println("Is a directory:"
                                        + f.isDirectory());
                        System.out.println("File Size in bytes "
                                        + f.length());
                }
        }
}
