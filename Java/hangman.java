import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Random;


public class hangman {

    String randomWord() {
        String[] words = {"apple", "banana", "orange", "grape", "kiwi", "geeks","vehicles"};
        Random rand = new Random();
        int index = rand.nextInt(words.length);
        return words[index];
    }

    void newGame() {
        int tries = 4;
        StringBuilder word = new StringBuilder(randomWord());
        StringBuilder hidden = new StringBuilder(word); //Explicitly declaring size
        BufferedReader rd = new BufferedReader( new InputStreamReader( System.in) );
        char[] discovered = new char[] {};
        for ( int i = 0; i < word.length() ; i++)
            hidden.setCharAt(i, '_');

        do
        {
            System.out.println("Guess the word! \n" + hidden.toString());
            System.out.println("Tries left: " + tries);
            System.out.print("Enter a letter: ");

            try 
            {
                char letter = rd.readLine().charAt(0);
                boolean found = false;

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
            } catch (Exception e) {
                System.out.println("Invalid input");
            }
            
        } while ( tries > 0 || hidden.equals(word) );
        
    }
    public static void main(String[] args) {
        hangman game = new hangman();
        game.newGame();
    }


    
}
