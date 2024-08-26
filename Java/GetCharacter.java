import java.util.Scanner;

public class GetCharacter {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);

    System.out.print("Enter a character: ");
    char character = scanner.next().charAt(0);

    System.out.println("You entered: " + character);
    scanner.close();
  }
}