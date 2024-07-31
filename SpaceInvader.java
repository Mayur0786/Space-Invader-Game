import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;

public class SpaceInvader extends JPanel implements ActionListener, KeyListener {
    private Timer timer;
    private Image playerImg, enemyImg, bulletImg, backgroundImg;
    private int playerX = 370, playerY = 480;
    private int playerXChange = 0;
    private ArrayList<Point> enemies;
    private ArrayList<Point> enemyDirections;
    private int enemySpeed = 1;
    private int bulletX = 0, bulletY = 480;
    private boolean bulletFired = false;
    private int score = 0;
    private String userName = "Player";

    public SpaceInvader() {
        // Load images
        playerImg = new ImageIcon("player.png").getImage();
        enemyImg = new ImageIcon("Alien1.png").getImage();
        bulletImg = new ImageIcon("bullet.png").getImage();
        backgroundImg = new ImageIcon("Space1.jpg").getImage();

        enemies = new ArrayList<>();
        enemyDirections = new ArrayList<>();
        addEnemies(2);

        setPreferredSize(new Dimension(800, 600));
        setBackground(Color.BLACK);
        setFocusable(true);
        addKeyListener(this);

        timer = new Timer(16, this); // Approx 60 FPS
        timer.start();
    }

    private void addEnemies(int num) {
        Random rand = new Random();
        for (int i = 0; i < num; i++) {
            enemies.add(new Point(rand.nextInt(736), rand.nextInt(150)));
            enemyDirections.add(new Point(enemySpeed, 40));
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.drawImage(backgroundImg, 0, 0, getWidth(), getHeight(), this);
        g.drawImage(playerImg, playerX, playerY, this);

        for (int i = 0; i < enemies.size(); i++) {
            g.drawImage(enemyImg, enemies.get(i).x, enemies.get(i).y, this);
        }

        if (bulletFired) {
            g.drawImage(bulletImg, bulletX + 16, bulletY + 10, this);
        }

        g.setColor(Color.WHITE);
        g.setFont(new Font("Arial", Font.PLAIN, 32));
        g.drawString(userName + "'s Score: " + score, 10, 30);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        updateGame();
        repaint();
    }

    private void updateGame() {
        playerX += playerXChange;

        if (playerX < 0)
            playerX = 0;
        if (playerX > 736)
            playerX = 736;

        for (int i = 0; i < enemies.size(); i++) {
            Point enemy = enemies.get(i);
            Point direction = enemyDirections.get(i);

            enemy.x += direction.x;
            if (enemy.x <= 0 || enemy.x >= 736) {
                direction.x = -direction.x;
                enemy.y += direction.y;
            }

            if (enemy.y > 440) {
                gameOver();
                return;
            }

            if (bulletFired && new Rectangle(bulletX + 16, bulletY + 10, 32, 32)
                    .intersects(new Rectangle(enemy.x, enemy.y, 64, 64))) {
                score++;
                bulletFired = false;
                bulletY = 480;
                enemy.x = new Random().nextInt(736);
                enemy.y = new Random().nextInt(150);

                if (score % 10 == 0) {
                    enemySpeed++;
                    addEnemies(1);
                }
            }
        }

        if (bulletFired) {
            bulletY -= 10;
            if (bulletY <= 0) {
                bulletFired = false;
                bulletY = 480;
            }
        }
    }

    private void gameOver() {
        timer.stop();
        JOptionPane.showMessageDialog(this, "GAME OVER\n" + userName + "'s Score: " + score, "Game Over",
                JOptionPane.INFORMATION_MESSAGE);
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();
        if (key == KeyEvent.VK_LEFT) {
            playerXChange = -5;
        } else if (key == KeyEvent.VK_RIGHT) {
            playerXChange = 5;
        } else if (key == KeyEvent.VK_SPACE) {
            if (!bulletFired) {
                bulletX = playerX;
                bulletFired = true;
            }
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        int key = e.getKeyCode();
        if (key == KeyEvent.VK_LEFT || key == KeyEvent.VK_RIGHT) {
            playerXChange = 0;
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Space Invader");
        SpaceInvader game = new SpaceInvader();
        frame.add(game);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
