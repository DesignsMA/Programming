import java.io.*; 
import java.util.*;
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;

class userInput {
    public Date getDate () {
        Boolean incorrect = false;
        Date date = new Date();
        SimpleDateFormat dateF = new SimpleDateFormat("dd/MM/yyyy kk:mm");

        do {
            try {
                System.out.println("\nEnter a date in the format dd/MM/yyyy hh:mm");
                System.out.print("Enter date: ");
                String input = System.console().readLine();
                date = dateF.parse(input);
                incorrect = false;
            } catch (Exception e) {
                System.out.println("Incorrect format, try again");
                incorrect = true;
            }
            
        } while ( incorrect );
        return date;
    }

    public void formatDecimal(float value) {
        DecimalFormat ft = new DecimalFormat("###,###.00000000");
        System.out.println("Formatted value: " + ft.format(value));
    }
}

public class formatters {
    public static void main(String[] args) {
        userInput user = new userInput();
        Date date = user.getDate();
        System.out.println("Date: " + date.toString());
        user.formatDecimal(14523432.78930f);

    }

    
}
