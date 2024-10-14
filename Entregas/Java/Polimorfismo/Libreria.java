class Item {
    private int id;
    private String title;

    public Item(int id, String title) {
        this.id = id;
        this.title = title;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String toString() {
        return id + " " + title;
    }

}

class Impreso extends Item {
    private int pages;

    public Impreso(int id, String title, int pages) {
        super(id, title); // Inicializando atributos heredados de Item
        this.pages = pages;
    }

    public int getPages() {
        return pages;
    }

    public void setPages(int pages) {
        this.pages = pages;
    }

    @Override // Overriding
    public String toString() {
        return super.toString() + " (" + pages + " paginas)";
    }

}

class Multimedia extends Item {
    private double length; // En segundos

    public Multimedia(int id, String title, int length) {
        super(id, title);
        this.length = length;
    }

    public double getLength() {
        return length;
    }

    public void setLength(double length) {
        this.length = length;
    }

    @Override // Overriding
    public String toString() {
        return super.toString() + " (" + length + " segundos)";
    }
}

public class Libreria {

    public static void main(String[] args) {
        Item items[] = new Item[4]; // Impreso y Multimedia SON items
        // Hijo a padre, upcasting implicito
        items[0] = new Impreso(7985, "Alice in Wonderland ", 105);
        items[1] = new Multimedia(3565, "In a Sentimental Mood", 597);
        items[2] = new Impreso(2365, "Building Java Programs", 874);
        items[3] = new Item(5823, "Complete Wreck Diving");

        printItems(items);

    }

    public static void printItems(Item[] items) {
        for (Item item : items) { // Por cada item en items | Item es polimorfo
            System.out.println(item + "\n");
        }
    }
}
