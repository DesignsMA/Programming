package BancoIO;

public class Banco {
    private CuentaBancaria[] cuentas;
    private int noC;

    public Banco(int max) {
        cuentas = new CuentaBancaria[max];
        noC = 0;
    }

    public CuentaBancaria[] getCuentas() {
        return cuentas;
    }

    public int getNoC() {
        return noC;
    }

    public void agregarCuenta(CuentaBancaria cuenta) {
        if (noC == cuentas.length) {
            throw new RuntimeException("El banco está lleno. No se agregó la cuenta.");
        }
        this.cuentas[noC++] = cuenta;
    }

    public CuentaBancaria buscarCuenta(int noCuenta) {
        for (int i = 0; i < noC; i++) {
            if (cuentas[i].getNoCuenta() == noCuenta) {
                return cuentas[i];
            }
        }
        return null;
    }

    @Override
    public String toString() {
        if (noC == 0)
            return "No existe ninguna cuenta";

        String cadena = "";
        for (int i = 0; i < noC; i++) {
            cadena += cuentas[i].getNoCuenta() + " ";
            cadena += cuentas[i].getBalance() + "\n";
        }

        return cadena;
    }
}
