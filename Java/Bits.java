import java.util.Scanner;

class Cinema {
    String[] movies;
    int[] prices;
    int[] times;
    short[][] seats;

    Cinema() {
        int n;
        System.out.println("Number of movies to place");
        Scanner scan = new Scanner(System.in);
        

    }

}

public class Bits {
    public static void main(String[] args) {
        char x = 'A';
        short y =  13476; //Short isn't unsigned, we consider the left-most bit
        int bit = 32768; // 0100 0000 0000 0000
        System.out.println((int) x + " " + (char) x + " ");
        System.out.println(Integer.toBinaryString(y) + " " + (short) y + " ");
        for (int i = 0; i < 16; i++) {
            if ( (bit >> i & y ) == bit >> i)
            
                System.out.print("I");
            else
                System.out.print("0");
        }
        System.out.println();
        for (int i = 0; i < 16; i++) {
            y ^= (bit >> i);
            if ( (bit >> i & y ) == bit >> i)
                System.out.print("I");
            else
                System.out.print("0");
        }
        System.out.println();
        
        System.out.println(Integer.toBinaryString(y) + " " + (short) y + " ");

    }
}
