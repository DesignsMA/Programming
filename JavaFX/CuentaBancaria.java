public class CuentaBancaria {
    private double balance;
    private int noCuenta;

    public CuentaBancaria(double balanceInicial, int noCuenta) {
        if (balanceInicial < 0)
            throw new IllegalArgumentException(
                    "El balance inicial debe ser positivo");
        if (noCuenta < 10000 || noCuenta > 99999)
            throw new IllegalArgumentException("No cuenta debe tener 5 digitos");
        else {
            this.balance = balanceInicial;
            this.noCuenta = noCuenta;
        }
    }

    public double getBalance() {
        return balance;
    }

    public int getNoCuenta() {
        return noCuenta;
    }

    public void depositar(double cantidad) {
        if (cantidad < 0)
            throw new IllegalArgumentException(
                    "¡Cantidad negativa, no es posible depositar! Proporcione un valor positivo");
        else
            this.balance = balance + cantidad;
    }

    public void retirar(double cantidad) { // Se debe usar la clausula throws para excepciones
                                           // personalizadas
        if (cantidad < 0)
            throw new IllegalArgumentException(
                    "¡Cantidad negativa, no es posible depositar! Proporcione un valor positivo");

        if (balance - cantidad < 0)
            throw new RuntimeException("¡No hay fondos suficientes!");
        else
            this.balance = balance - cantidad;
    }

    @Override
    public String toString() {
        return "" + noCuenta + " $" + balance;
    }
}
