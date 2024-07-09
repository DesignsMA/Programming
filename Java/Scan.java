import java.util.Scanner;

public class Scan {
    
        public static void main(String[] args) {
            int sum = 0, count =0;
            Scanner scan = new Scanner( System.in );
            System.out.println("Enter numbers to sum, type 'exit' to finish");
            while (scan.hasNextInt()) {
                sum += scan.nextInt();
                count++;
            }

            if (count>0) {
                System.out.println("Sum: " + sum);
                System.out.println("Average: " + (sum/count));
            } else System.out.println("No numbers to sum");
            scan.close();
    }
}
