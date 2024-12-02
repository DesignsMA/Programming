import java.util.Date;
import java.util.Random;
import java.util.Scanner;


public class hangman {

    String randomWord() {
        String[] words = {"apple", "banana", "orange", "grape", "kiwi", "geeks","vehicles"};
        Random rand = new Random((new Date()).getTime());
        int index = rand.nextInt(words.length);
        return words[index];
    }

    void newGame() {
        int tries = 4;
        StringBuilder word = new StringBuilder(randomWord());
        StringBuilder hidden = new StringBuilder(word); //Explicitly declaring size
        Scanner rd = new Scanner(System.in);
        char letter;     

        for ( int i = 0; i < word.length() ; i++)
            hidden.setCharAt(i, '_');
        do
        {
            System.out.println("\n    Guess the word!\n        " + hidden.toString());
            System.out.println("\nTries left: " + tries);
            System.out.print("Enter a letter (a-z): ");

          try 
            {
                do letter = Character.toLowerCase( rd.next().charAt(0) );
                while ( letter < 'a' || letter > 'z');
                
                boolean found = false, repeated = false;
                for ( int i = 0; i < hidden.length() ; i++) 
                {
                    if ( hidden.charAt(i) == letter ) {
                        System.out.println("Letter already discovered");
                        found = true;
                        repeated = true;
                        break;
                    }
                }

                if ( !repeated ) {
                    for ( int i = 0; i < word.length() ; i++) {
                        if ( word.charAt(i) == letter ) {
                            hidden.setCharAt(i, letter);
                            found = true;
                        }
                    }
                    if ( !found ) { //if not found
                        tries--;
                        System.out.println("Letter not found");
                    }
                    repeated = false;
                }
            
            } catch (Exception e) {
                System.out.println("Invalid input");
            }
            
            
        } while ( tries > 0 && ! hidden.toString().equals(word.toString())); //While there are tries left and the word is not equal to the guessed

        rd.close();
        if ( tries > 0) {
            System.out.println("Congratulations! You guessed the word: " + word);
        } else {
            System.out.println("You lost! The word was: " + word);
        }
        
    }
    public static void main(String[] args) {
        hangman game = new hangman();
        game.newGame();
    }


    
}
