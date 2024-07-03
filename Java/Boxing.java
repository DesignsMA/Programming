public class Boxing {
    public static void main(String[] args) {
        int i = 10;
        float f = 6.9f;
        double d = 5.6d;
        char c = 'a';
        boolean b = true;

        //wrapperClass objectName =  new wrapperClass(dataType) is deprecated since Java 9
        Integer intObj = Integer.valueOf(i); //Wrapping int data type into an integer object
        Float floatObj = Float.valueOf(f); //Wrapping float data type into a float object
        Double doubleObj = Double.valueOf(d); //Wrapping double data type into a double object
        Character charObj = Character.valueOf(c); //Wrapping char data type into a character object
        Boolean boolObj = Boolean.valueOf(b); //Wrapping boolean data type into a boolean object

        System.out.println();
        System.out.println("Bit Count: " + Integer.bitCount(i) + " | Object:  " + intObj);
        System.out.println("FloatToIntBits: " + Float.floatToIntBits(f) + " | Object:  " + floatObj);
        System.out.println("DoubleToLongBits: " + Double.doubleToLongBits(d) + " | Object:  " + doubleObj);
        System.out.println("Character: " + Character.isLetter(c) + " | Object:  " + charObj);
        System.out.println("Boolean (Object AND False): " + Boolean.logicalAnd(b, false) + " | Object:  " + boolObj);

        //Unwrapping objects to primitive data types

        int i2 = intObj.intValue(); //Unwrapping Integer object to int data type
        float f2 = floatObj.floatValue(); //Unwrapping Float object to float data type
        double d2 = doubleObj.doubleValue(); //Unwrapping Double object to double data type
        char c2 = charObj.charValue(); //Unwrapping Character object to char data type
        boolean b2 = boolObj.booleanValue(); //Unwrapping Boolean object to boolean data type


        System.out.println("\n\t\tUnwrapping Objects\nInt: " + i2);
        System.out.println("Float: " + f2);
        System.out.println("Double: " + d2);
        System.out.println("Char: " + c2);
        System.out.println("Boolean: " + b2);

    }

}