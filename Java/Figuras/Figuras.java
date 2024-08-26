package Figuras;
import java.awt.Color;
import java.awt.Graphics;
import java.util.Random;
import java.util.Scanner;
public class Figuras {
    public boolean verficar (Circulo c, double a) 
    {
        if (c.area() == a) 
        {
            return true;
        }
        return false;
    }
    public static void main(String[] args) {
        Random rand = new Random();
        MyFrame myFrame = new MyFrame( new Color(rand.nextInt(255), rand.nextInt(255), rand.nextInt(255)));
        
        

    }
}
