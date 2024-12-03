package ahorcado;

public class Administrador extends Usuario {
    private static final long serialVersionUID = 1L;
    private String password;

    // Constructor
    public Administrador(String username, String password) {
        super(username);
        this.password = password;
    }

    // Getter
    public String getPassword() {
        return password;
    }


    @Override
    public String toString() {
        return "Administrador{username='" + username + "'}";
    }
}