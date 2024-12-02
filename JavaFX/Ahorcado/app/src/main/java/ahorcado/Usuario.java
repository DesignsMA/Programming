package ahorcado;

import java.io.Serializable;

public abstract class Usuario implements Serializable {
    private static final long serialVersionUID = 1L;
    protected String username;

    // Constructor
    public Usuario(String username) {
        this.username = username;
    }

    // Getter
    public String getUsername() {
        return username;
    }

    @Override
    public String toString() {
        return "Usuario{username='" + username + "'}";
    }

    // Método abstracto que debe ser implementado por las clases hijas
    public abstract void mostrarEstadisticas();
}
