class Factorial {

    private int operations;

    private int calc( int n ) {
        int result = 0;
        if (n == 1 ) return 1;
        result = n * calc( n-1 );
        return result;
    }

    int fact(int n) {
        int max = n, result;
        operations++;
        result = calc(n);
        for (int i = 0; i < max; i++) {
            System.out.print(n);
            if ( n != 1 ) System.out.print(" *  ");
            n--;
        }
        System.out.println(" = " + result + "\nOperations Done: " + operations);
        return result;
    }
}

public class Wrapping {
    public static void main(String[] args) {

        System.out.println();
        Factorial f = new Factorial();
        f.fact(5);
        f.fact(10);
        f.fact(15);
    }
    
}
