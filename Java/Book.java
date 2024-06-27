public class Book {
    //Instance Variables
    String title;
    String author;
    int yearPublished;
    int pages;
    String genre;
    String publisher;

    // Constructor Declaration of Class (method used to construct or declare the class)
    public Book( String title, String author,  int yearPublished, int pages,
                 String genre, String publisher)
    {
        this.title = title;
        this.author = author;
        this.yearPublished = yearPublished;
        this.pages = pages;
        this.genre = genre;
        this.publisher = publisher;
    }

    // Methods | Called after constructing the class
    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public int getYear() {
        return yearPublished;
    }

    public int getPages() {
        return pages;
    }

    public String getGenre() {
        return genre;
    }

    public String getPublisher() {
        return publisher;
    }

    //Override of the inherited method toString()
    @Override
    public String toString() {
        return "Book[title=" + this.title + ", author=" + this.author + 
        ",year=" + this.yearPublished + ", pages=" + this.pages + 
        ", genre=" + this.genre + ", publisher=" + this.publisher + "]";
    }

    public static void main(String[] args) {
        // Instanciating class (creating object)
        Book book1 = new Book("1984", "George Orwell", 1949, 264, "Dystopian Novel", "Editores Mexicanos Unidos");
        System.out.println(book1.toString());

    }
}
