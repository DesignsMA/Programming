// Program to check for command line arguments

import java.io.DataInputStream;

class Inputs {
    public static void main(String[] args)
    {
        char[] name;
        int age;
        DataInputStream reader = new DataInputStream( System.in);
        // check if length of args array is
        // greater than 0
        // Prints the additional args when called : java <program.java> arg1 arg2 arg3 ...
        if (args.length > 0) {
            System.out.println(
                "The command line arguments are:");

            // iterating the args array and printing
            // the command line arguments
            for (String val : args)
                System.out.println(val);
        }
        else
            System.out.println("No command line "
                               + "arguments found.");
        
        //Gets an input directly from the console (string), doesn't echoes through another
        //method, adecuate for passwords

        name = System.console().readPassword("Enter password: ");
        System.out.println("Hello " + name.toString() + "!");

        
    }
}