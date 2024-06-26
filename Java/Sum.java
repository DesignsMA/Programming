import java.util.Scanner;

public class Sum {
    public static void main(String[] args) {
        int a, b, c;
        Scanner scan = new Scanner(System.in);
        System.out.println("Enter the first number: ");
        a = scan.nextInt();
        System.out.println("Enter the second number: ");
        b = scan.nextInt();
        System.out.println("Enter the third number: ");
        c = scan.nextInt();
        System.out.println("The sum of the three numbers is: " + sum(a, b, c));
        System.out.println("The product of the three numbers is: " + product(a, b, c));
        scan.close();
    }

    public static int sum(int a, int b, int c) {
        int sum = a + b + c;
        return sum;
    }

    public static int product(int a, int b, int c) {
        int product = a * b * c;
        return product;
    }
}