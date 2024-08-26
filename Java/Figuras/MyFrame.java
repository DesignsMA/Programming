package Figuras;

import java.awt.*; 
import java.awt.event.WindowAdapter; 
import java.awt.event.WindowEvent; 
  
public class MyFrame extends Frame {
    private Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    private int height = screenSize.height;
    private int width = screenSize.width;
    private Color color;
    public MyFrame(Color color) 
    { 
        setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();

        this.color = color;
        Panel circlePanel = new Panel() {
            @Override
            public void paint(Graphics g) {
                g.setColor(color);
                g.fillOval(0, 0, 250, 250);         
            }
        };
        circlePanel.setPreferredSize( new Dimension(250,250));

        gbc.anchor = GridBagConstraints.CENTER;
        add(circlePanel,gbc);
        setVisible(true); 
        setSize(width/2, height); 
        addWindowListener(new WindowAdapter() { 
            @Override
            public void windowClosing(WindowEvent e) 
            { 
                System.exit(0); 
            } 
        });        
    }

    public Color getColor () { return color; };
    public void setColor (Color color) { this.color = color; };
    
}
