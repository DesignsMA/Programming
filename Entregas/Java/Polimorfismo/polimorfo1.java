/*// Parent p = new Child(); Upcasting, child to parent, implicit (can be explicit)
 all parent atributes accesible but overriden methods are used instead 

 Child c = (Child)p; Explicit cast (type) parent (only cast type)
Downcasting has to be done externally and due to downcasting a child object
can acquire the properties of the parent object. 
 
c.name = p.name; Name is a property of the parent
i.e., c.name = "GeeksforGeeks"*/
 class Foo { 
    public void method() { 
        System.out.println("Foo"); 
    } 
} 
 
 class Bar extends Foo { 
    public void method() { 
        System.out.println("Bar"); 
    } 
} 
 
 class Goo extends Bar { 
    public void method(String message) { 
        System.out.println("Goo:" + message); 
    } 
} 

public class polimorfo1 {
    public static void main(String[] args) {
        Foo f = new Bar(); 
        f.method(); 
        
    }
}