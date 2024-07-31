import math
import random
import pygame
import imageio
from pygame import mixer
import tkinter as tk
from tkinter import simpledialog
import moviepy.editor

# Initialize pygame
pygame.init()

# Create a tkinter root window for user input
root = tk.Tk()
root.withdraw()

# Get user's name using a GUI dialog
user_name = simpledialog.askstring("Input", "Enter your name:")

# Check if the user canceled the input dialog
if user_name is None:
    exit()

# intro
#video = moviepy.editor.VideoFileClip("intro.mp4")
#video.preview()

# Create the screen with resizable options
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

# Initialize background images
background_images = ['Space1.jpg', 'Space4.jpg', 'Space5.jpg', 'Space3.jpg', 'Space2.jpg']
current_background_index = 0
background = pygame.image.load(background_images[current_background_index]).convert()

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_speed = 2  # Adjust the speed here
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Alien1.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)  # Set the initial speed for each enemy
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# User Score
user_scores = {user_name: 0}

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_sound = mixer.Sound("Moye Moye.wav")


def show_score(x, y):
    score = font.render(f"Score: {user_scores[user_name]}", True, (255, 255, 255))
    text_width, _ = font.size(f"Score: {user_scores[user_name]}")
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    text_width, _ = over_font.size("GAME OVER")
    screen.blit(over_text, (screen.get_width() // 2 - text_width // 2, screen.get_height() // 2 - 50))
    show_score(screen.get_width() // 2 - text_width // 2, screen.get_height() // 2 + 50)
    game_over_sound.play()  # Play game-over sound


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
# Inside the game loop
while running:
    screen.fill((0, 0, 0))  # RGB = Red, Green, Blue
    screen.blit(background, (0, 0))  # Background Image

    # Get the current screen dimensions
    screen_width, screen_height = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            screen_width, screen_height = event.w, event.h
            background = pygame.transform.scale(background, (screen_width, screen_height))

        if event.type == pygame.FULLSCREEN:
            if event.state == 1:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
            else:
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed  # Change direction to right if reaching left edge
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed  # Change direction to left if reaching right edge
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            user_scores[user_name] += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

            # Check if the score is a multiple of 10 and increase the speed
            if user_scores[user_name] % 10 == 0 and user_scores[user_name] != 0:
                enemy_speed += 1

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    # Check if user score is a multiple of 10
    if user_scores[user_name] % 10 == 0 and user_scores[user_name] != 0:
        # Increment background index and wrap around if needed
        current_background_index = (current_background_index + 1) % len(background_images)
        # Load the new background image
        background = pygame.image.load(background_images[current_background_index]).convert()
        # Resize the background image to match the screen size
        background = pygame.transform.scale(background, (screen_width, screen_height))

    pygame.display.update()

pygame.quit()
