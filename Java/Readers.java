import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;

class Scanners {

    void read() {
        Scanner scan = new Scanner( System.in );
        System.out.print("String (With Spaces): ");
        String str = scan.nextLine();
        System.out.println("You entered: " + str);
        System.out.print("String (Without Spaces): ");
        str = scan.next();
        System.out.println("You entered: " + str);
        System.out.print("Float: ");
        float flt = scan.nextFloat();
        System.out.println("You entered: " + flt);
    }

}

public class Readers {

    public static void main(String[] args)
    throws IOException //Buffered reader throws exceptions
    {
        BufferedReader bfr = new BufferedReader( new InputStreamReader(System.in) );

        System.out.print("String: ");
        String  str = bfr.readLine();
        System.out.println("You entered: " + str);
        System.out.print("Float: ");
        Float flt = Float.parseFloat( bfr.readLine() );
        System.out.println("You entered: " + flt);
        System.out.print("Int: ");
        int num = Integer.parseInt( bfr.readLine() );
        System.out.println("You entered: " + num);
        
        try { //We catch execeptions in order to continue the flow of the program
            System.out.println("Your name: ");
            str = bfr.readLine();
            System.out.println("You entered: " + str);
        } catch (Exception any) {
            System.out.println("There was an error while reading name...");
        }

        bfr.close(); //Stop reading input stream


    }
    
}
