#declare a class  TEST with a private attribute c=2

# class TEST:
#     def __init__(self):
#         self.__c=2
#     def get_c(self):
#         return self.__c
#     def set_c(self,c):
#         self.__c=c

# let's create an object of the class TEST
# t=TEST()
# # let's print the value of c
# print(t.get_c())
# t.set_c(3)
# t.__c=4
# print(t.__c)
# print(t.get_c())
# print(t._TEST__c) #this is the way to access the private attribute, it's not recommended, it's funny to know that it's possible though 

# write a game: I will describe the game:
# We control a block, using the arrow. We have 3 lifes and we have to avoid the obstacles.
# The obstacles are moving from the right to the left. The speed of the obstacles is increasing with time.
# The game ends when we lose all the lifes.
# The score is the time we survive.
# The game is over when we lose all the lifes.
# The game is won when we reach 1000 points.

import pygame
import random

# initialize the game
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon

pygame.display.set_caption("My first game")
icon = pygame.image.load('ufo.png')
# scale the image based on the hitbox of the enemy
icon = pygame.transform.scale(icon, (32, 32))
# scale the image based on the hitbox of the enemy
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ufo.png')
# scale the image based on the hitbox of the player
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('ufo.png')
# scale the image based on the hitbox of the enemy
enemyImg = pygame.transform.scale(enemyImg, (64, 64))
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.3
enemyY_change = 40

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('ufo.png')
# scale the image based on the hitbox of the bullet
bulletImg = pygame.transform.scale(bulletImg, (32, 32))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))
    
def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX)**2 + (enemyY - bulletY)**2)**0.5
    if distance < 27:
        return True
    else:
        return False
    
# Game Loop
running = True
enemy_speed = 0.3  # Initialize enemy speed
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    # screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    # Enemy Movement
    enemyX += enemyX_change
    if enemyX <= 0 or enemyX >= 736:
        enemyX_change = -enemyX_change  # Reverse enemy direction
        enemyY += enemyY_change
        enemyX_change += 0.1  # Increase enemy speed after bounce
    
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        print(score_value)
        enemyX = random.randint(0, 800)
        enemyY = random.randint(50, 150)
    
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)
    
    if enemyY > 440:
        for j in range(2000):
            game_over_text()
        break
    
    pygame.display.update()
    
# Game Over

pygame.quit()
exit()


