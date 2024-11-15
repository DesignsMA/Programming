public class Archivos {
    public static void main(String[] args) {
        Banco b = new Banco(10);
        try {
            BancoIO.leerArchivo("file.txt", b);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        System.out.println(b);
    }
}