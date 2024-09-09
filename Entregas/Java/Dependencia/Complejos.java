package Entregas.Java.Dependencia;

class Complejo {
	private double a; // Parte real
	private double b; // Parte imaginaria

	public Complejo(double a, double b) {
		this.a = a;
		this.b = b;
	}

	public Complejo sumar(Complejo c2) {
		return new Complejo(this.a + c2.a, this.b + c2.b);
	}

	public Complejo restar(Complejo c2) {
		return new Complejo(this.a - c2.a, this.b - c2.b);
	}

	public Complejo multiplicar(Complejo c2) {
		double real = this.a * c2.a - this.b * c2.b;
		double imaginario = this.a * c2.b + this.b * c2.a;
		return new Complejo(real, imaginario);
	}

	public Complejo conjugado() {
		return new Complejo(this.a, -this.b);
	}

	public double modulo() {
		return Math.sqrt(this.a * this.a + this.b * this.b);
    } 

	public double angulo() {
		return Math.atan2(this.b, this.a)*180/Math.PI; //devuelve en grados
	}

	public String toString() {
		return this.a + " + ( " + this.b + "i )";
	}
}

public class Complejos {
	public static void main(String[] args) {
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        System.out.print("Ingrese la parte real del primer número complejo: ");
        double a1 = scanner.nextDouble();
        System.out.print("Ingrese la parte imaginaria del primer número complejo: ");
        double b1 = scanner.nextDouble();
        Complejo c1 = new Complejo(a1, b1);
            
        System.out.print("Ingrese la parte real del segundo número complejo: ");
        double a2 = scanner.nextDouble();
        System.out.print("Ingrese la parte imaginaria del segundo número complejo: ");
        double b2 = scanner.nextDouble();
        Complejo c2 = new Complejo(a2, b2);
            
        int opcion;
        do {
            System.out.println("\nSeleccione una operación:");
            System.out.println("1. Sumar complejos");
            System.out.println("2. Restar complejos");
            System.out.println("3. Multiplicar complejos");
            System.out.println("4. Conjugado del primer complejo");
            System.out.println("5. Módulo del primer complejo");
            System.out.println("6. Ángulo del primer complejo");
            System.out.println("7. Conjugado del segundo complejo");
            System.out.println("8. Módulo del segundo complejo");
            System.out.println("9. Ángulo del segundo complejo");
            System.out.println("10. Salir");
            opcion = scanner.nextInt();
            
            switch (opcion) {
                case 1:
                    System.out.println("Resultado: " + c1.sumar(c2));
                    break;
                case 2:
                    System.out.println("Resultado: " + c1.restar(c2));
                    break;
                case 3:
                    System.out.println("Resultado: " + c1.multiplicar(c2));
                    break;
                case 4:
                    System.out.println("Conjugado del primer complejo: " + c1.conjugado());
                    break;
                case 5:
                    System.out.println("Módulo del primer complejo: " + c1.modulo());
                    break;
                case 6:
                    System.out.println("Ángulo del primer complejo: " + c1.angulo() + "°");
                    break;
                case 7:
                    System.out.println("Conjugado del segundo complejo: " + c2.conjugado());
                    break;
                case 8:
                    System.out.println("Módulo del segundo complejo: " + c2.modulo());
                    break;
                case 9:
                    System.out.println("Ángulo del segundo complejo: " + c2.angulo() + "°");
                    break;
                case 10:
                    System.out.println("Saliendo...");
                    break;
                default:
                    System.out.println("Opción no válida.");
            }
        } while (opcion != 10);
        scanner.close();
    }

}
          
