import java.util.Scanner;

class Cuenta {
  private double balance;
  private int noCuenta;

  public Cuenta(int a) {
    balance = 0.0;
    noCuenta = a;
  }

  public void depositar(double suma) {
    if (suma > 0)
      balance += suma;
    else
      System.err.println("No es posible depositar cantidad negativa.");
  }

  public void retirar(double suma) {
    if (suma >= 0)
      balance -= suma;
    else
      System.err.println("No es posible retirar cantidad negativa.");
  }

  public double getBalance() {
    return balance;
  }

  public int getNoCuenta() {
    return noCuenta;
  }

  public String toString() {
    return "No. Cuenta: " + noCuenta + " - " + "Balance = " + balance;
  }
}

class CuentaAhorro extends Cuenta {
  private double interes; // Interes en porcentaje, i.e 10% se suma 10% del balance

  public CuentaAhorro(int noCuenta, double interes) {
    super(noCuenta); // Inicializando clase padre
    this.interes = interes;
  }

  public double getInteres() {
    return interes;
  }

  public void setInteres(double interes) {
    this.interes = interes;
  }

  public void depositaInteres() {
    super.depositar(super.getBalance() * (interes / 100.0f));
  }

  @Override
  public String toString() {
    return super.toString() + " Interes = " + interes;
  }
}

class CuentaCorriente extends Cuenta {
  /*
   * El sobregiro bancario es una situación en la que un banco permite que
   * un cuentahabiente realice pagos o desembolsos que exceden el saldo
   * disponible en su cuenta. Es una facilidad que ofrecen los bancos a
   * sus clientes para permitirles realizar transacciones financieras
   * cuando no tienen suficientes fondos en su cuenta corriente
   */
  private double sobregiro; // Límite de sobregiro

  public CuentaCorriente(int noCuenta, double sobregiro) {
    super(noCuenta);
    this.sobregiro = sobregiro;
  }

  public double getSobregiro() {
    return sobregiro;
  }

  public void setSobregiro(double sobregiro) {
    this.sobregiro = sobregiro;
  }

  public void estado() {
    if (super.getBalance() < 0)
      System.out.println("\t\tCuenta " + super.getNoCuenta() + " con sobregiro\n");
  }

  @Override
  public String toString() {
    return super.toString() + " Sobregiro = " + sobregiro;
  }

}

public class Banco {

  public static void main(String[] args) {
    int opc, n = 1;
    Cuenta[] cuentas = new Cuenta[20];
    Scanner sc = new Scanner(System.in);

    do {
      System.out.print(
          "\n1. Crear cuenta\n2. Eliminar cuenta\n3. Depositar\n4. Retirar\n5. Mostrar cuentas\n6. Actualizar\n7. Salir\n: ");
      opc = sc.nextInt();
      switch (opc) {
        case 1: { // Conteniendo los valores en solo este caso
          double valor;
          int cont = 0;
          char c;
          System.out.print("\na. Cuenta Ahorros\nb. Cuenta Corriente (Por defecto)\n: ");
          c = sc.next().charAt(0); // Lectura sin espacios caracter 1
          while (cuentas[cont] != null)
            ++cont;

          if (cont == 20) {
            System.out.print("\nLimite de cuentas alcanzado");
            break;
          }

          if (c == 'a') {
            System.out.print("\nInteres %: ");
            valor = sc.nextDouble();
            cuentas[cont] = new CuentaAhorro(n++, valor);
          } else {
            System.out.print("\nSobregiro: ");
            valor = sc.nextDouble();
            cuentas[cont] = new CuentaCorriente(n++, valor);
          }
        }
          break;

        case 2: {
          int no;
          mostrar(cuentas);
          System.out.print("\nIntroduzca el número de cuenta: ");
          no = sc.nextInt();
          for (Cuenta c : cuentas) {
            if (c.getNoCuenta() == no) {
              c = null; // Se borra la referencia y es elegido como basura por jvm
              break;
            }
          }
        }
          break;

        case 3: {
          int no;
          double deposito;
          mostrar(cuentas);
          System.out.print("\nIntroduzca el número de cuenta: ");
          no = sc.nextInt();
          System.out.print("\nIntroduzca el monto: ");
          deposito = sc.nextDouble();
          for (Cuenta c : cuentas) {
            if (c.getNoCuenta() == no) {
              c.depositar(deposito);
              break;
            }
          }
        }
          break;

        case 4: {
          int no;
          double retiro;
          mostrar(cuentas);
          System.out.print("\nIntroduzca el número de cuenta: ");
          no = sc.nextInt();
          System.out.print("\nIntroduzca el monto: ");
          retiro = sc.nextDouble();
          for (Cuenta c : cuentas) {
            if (c.getNoCuenta() == no) {
              if (retiro > c.getBalance() && c instanceof CuentaAhorro) {
                System.out.println("Balance insuficiente");
              } else if (c instanceof CuentaAhorro)
                c.retirar(retiro);

              if (retiro > c.getBalance() + ((CuentaCorriente) c).getSobregiro() && c instanceof CuentaCorriente) {
                System.out.println("Balance insuficiente");
              } else
                c.retirar(retiro);
              break;
            }
          }
        }
          break;

        case 5:
          mostrar(cuentas);
          break;

        case 6: {
          for (Cuenta c : cuentas) {
            if (c instanceof CuentaAhorro && c != null)
              ((CuentaAhorro) c).depositaInteres();
            else if (c != null)
              ((CuentaCorriente) c).estado();
          }
        }
          break;

        default:
          break;
      }
    } while (opc != 7);
  }

  public static void mostrar(Cuenta cs[]) {
    for (Cuenta c : cs) {
      if (c != null)
        System.out.println(c);
    }
  }
}