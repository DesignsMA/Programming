import java.util.Scanner;

public class Termómetros {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Termómetro termometro; // Podemos hacer upcast
        double grados;
        int opc = 0;
        System.out.print("Eliga el termómetro:\n1. Farenheit\t2. Celsius\n: ");
        opc = sc.nextInt();
        System.out.print("\nGrados: ");
        grados = sc.nextDouble();

        if (opc == 1) {
            termometro = new TermómetroFahrenheit(grados);
        } else
            termometro = new TermómetroCelsius(grados);

        do {
            System.out.println("Memoria: \n" + termometro.imprimirMemoria());
            System.out.print(
                    "\n1. Leer temperatura\n2. Convertir los grados a una unidad distinta\n3. Determinar temperatura\n4. Almacenar temperatura\n5. Mostrar la temperatura mínima guardada\n6. Mostrar la temperatura máxima leída\n7. Resetear memoria\n8. Salir\n: ");
            opc = sc.nextInt();
            switch (opc) {
                case 1:
                    grados = sc.nextDouble();
                    termometro.setGrados(grados);
                    break;

                case 2:
                    if (termometro instanceof TermómetroFahrenheit)
                        System.out.println(termometro.getGrados() + " °F = " + termometro.convertir() + " °C");
                    else
                        System.out.println(termometro.getGrados() + " °C = " + termometro.convertir() + " °F");
                    break;

                case 3:
                    System.out.println(termometro.determinarTemperatura());
                    break;

                case 4:
                    termometro.guardarEnMemoria();
                    break;

                case 5:
                    if (termometro instanceof TermómetroFahrenheit)
                        System.out.println("\n: " + termometro.minimo() + " °F");
                    else
                        System.out.println("\n: " + termometro.minimo() + " °C");
                    break;

                case 6:
                    if (termometro instanceof TermómetroFahrenheit)
                        System.out.println("\n: " + termometro.maximo() + " °F");
                    else
                        System.out.println("\n: " + termometro.maximo() + " °C");
                    break;

                case 7:
                    termometro.resetearMemoria();

                default:
                    break;
            }
        } while (opc != 8);
    }

}
