// Java Program to Illustrate BufferedReader Class 
// Via Its Methods 
  
// Importing required classes 
import java.io.BufferedReader; 
import java.io.FileReader; 
import java.io.IOException;
public class Bufferedread {

    public static void main(String[] args) 
        throws IOException 
    { 
  
        // Creating object of FileReader and BufferedReader 
        // class 
        FileReader fr = new FileReader("Java/file.txt"); 
        BufferedReader br = new BufferedReader(fr); 
  
        char c[] = new char[20]; 
  
        // Illustrating markSupported() method 
        if (br.markSupported()) { 
  
            // Print statement 
            System.out.println( 
                "mark() method is supported"); 
  
            // Illustrating mark method 
            br.mark(100); //Marks the initial position on the buffer
        } 
  
        // File Contents is as follows: 
        // This is first line 
        // this is second line 
        // Skipping 8 characters 
        br.skip(8); //Skipping "This is "
  
        // Illustrating ready() method 
        if (br.ready()) {  //If stream is ready to be read (file)
  
            // Illustrating readLine() method 
            System.out.println(br.readLine());  //print line after 8 characters
  
            // Illustrating read(char c[],int off,int len) 
            br.read(c); //Reads second line into array c (destination buffer)
  
            for (int i = 0; i < 20; i++) { 
                System.out.print(c[i]); //prints characters
            } 
  
            System.out.println(); 
  
            // Illustrating reset() method 
            br.reset(); //resets the reader  to its initial place
            for (int i = 0; i < 8; i++) { 
  
                // Illustrating read() method 
                System.out.print((char)br.read());//reads  8 characters from the start "This is " 
            } 
        }
        br.close(); 
    } 
    
}
