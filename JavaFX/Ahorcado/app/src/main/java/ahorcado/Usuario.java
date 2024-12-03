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
    public abstract String toString();
}
