
public class Archivos {
    public static void main(String[] args) {
        Banco b = new Banco(50);
        try {
            BancoIO.leerArchivo("file.txt", b);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        b.agregarCuenta(new CuentaBancaria(0, 77742));
        BancoIO.escribirArchivo("file.txt", b);

    }
}