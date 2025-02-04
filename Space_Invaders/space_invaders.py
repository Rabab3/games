import pygame
import random
import os

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre du jeu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BEIGE = (245, 245, 220)

# Charger les images
BASE_DIR = os.path.dirname(__file__)
player_img = pygame.image.load(os.path.join(BASE_DIR, "player.png"))
enemy_img = pygame.image.load(os.path.join(BASE_DIR, "enemy.png"))
bullet_img = pygame.image.load(os.path.join(BASE_DIR, "bullet.png"))
powerup_img = pygame.image.load(os.path.join(BASE_DIR, "powerup.png"))
bomb_img = pygame.image.load(os.path.join(BASE_DIR, "bomb.png"))

# Redimensionner les images
player_img = pygame.transform.scale(player_img, (64, 64))
enemy_img = pygame.transform.scale(enemy_img, (64, 64))
bullet_img = pygame.transform.scale(bullet_img, (20, 40))
powerup_img = pygame.transform.scale(powerup_img, (60, 60))
bomb_img = pygame.transform.scale(bomb_img, (30, 30))

# Charger le score enregistré
highscore_file = os.path.join(BASE_DIR, "highscore.txt")
def load_highscore():
    try:
        with open(highscore_file, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_highscore(score):
    with open(highscore_file, "w") as file:
        file.write(str(score))

highscore = load_highscore()

# Classe Player
class Player:
    def __init__(self):
        self.x = WIDTH // 2 - 32
        self.y = HEIGHT - 80
        self.speed = 5
        self.img = player_img
    
    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - 64:
            self.x = WIDTH - 64
    
    def draw(self):
        screen.blit(self.img, (self.x, self.y))

# Classe Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.state = "ready"
    
    def fire(self, x, y):
        self.state = "fire"
        self.x = x + 22
        self.y = y - 20
    
    def update(self):
        if self.state == "fire":
            self.y -= self.speed
            if self.y <= 0:
                self.state = "ready"
                self.y = player.y

    def draw(self):
        if self.state == "fire":
            screen.blit(bullet_img, (self.x, self.y))

# Classe Enemy
class Enemy:
    def __init__(self, x, y, speed_x=0.02, speed_y=0.02):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.img = enemy_img
        self.bombs = []  # Liste des bombes associées à cet ennemi
    
    def update(self):
        self.x += self.speed_x
        if self.x <= 0 or self.x >= WIDTH - 64:
            self.speed_x *= -1
            self.y += self.speed_y
    
    def generate_bomb(self):
        if random.random() < 0.005:  # Chance pour qu'un ennemi génère une bombe
            bomb = Bomb(self.x + 32, self.y + 32)
            self.bombs.append(bomb)
    
    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        for bomb in self.bombs:
            bomb.update()
            bomb.draw()

# Classe PowerUp
class PowerUp:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50
        self.speed = 0.5
        self.active = False
        self.type = "speed"
    
    def activate(self, player):
        if self.active and is_collision(player.x, player.y, self.x, self.y, 40):
            self.active = False
            if self.type == "speed":
                player.speed += 2

    def update(self):
        if self.active:
            self.y += self.speed
            screen.blit(powerup_img, (self.x, self.y))

# Classe Bomb
class Bomb:
    def __init__(self, x, y, speed=4):
        self.x = x
        self.y = y
        self.speed = speed
    
    def update(self):
        self.y += self.speed
    
    def draw(self):
        screen.blit(bomb_img, (self.x, self.y))

# Fonction de collision
def is_collision(obj_x, obj_y, target_x, target_y, threshold):
    distance = ((obj_x - target_x) ** 2 + (obj_y - target_y) ** 2) ** 0.5
    return distance < threshold

# Initialisation des objets
player = Player()
bullet = Bullet(player.x, player.y)
enemies = [Enemy(random.randint(50, WIDTH - 50), random.randint(50, 150)) for _ in range(6)]
powerup = PowerUp()
bombs = []

# Score
score = 0
enemies_destroyed = 0
font = pygame.font.Font(None, 36)

def game_over_screen():
    global highscore
    screen.fill(BEIGE)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    enemies_text = font.render(f"Ennemis détruits: {enemies_destroyed}", True, WHITE)
    highscore_text = font.render(f"High Score: {highscore}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    screen.blit(enemies_text, (WIDTH // 2 - 80, HEIGHT // 2 + 40))
    screen.blit(highscore_text, (WIDTH // 2 - 80, HEIGHT // 2 + 80))
    pygame.display.update()
    pygame.time.delay(3000)

running = True
while running:
    screen.fill(BEIGE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-player.speed)
    if keys[pygame.K_RIGHT]:
        player.move(player.speed)
    if keys[pygame.K_SPACE] and bullet.state == "ready":
        bullet.fire(player.x, player.y)
    
    for enemy in enemies:
        enemy.update()
        enemy.generate_bomb()  # Générer des bombes pour chaque ennemi
        if is_collision(enemy.x, enemy.y, bullet.x, bullet.y, 30):
            bullet.state = "ready"
            bullet.y = player.y
            score += 1
            enemies_destroyed += 1
            enemy.x = random.randint(50, WIDTH - 50)
            enemy.y = random.randint(50, 150)
            if random.random() < 0.2:
                powerup.x = enemy.x
                powerup.y = enemy.y
                powerup.active = True
                powerup.type = random.choice(["speed", "bullet"])
        enemy.draw()
    
    if bullet.state == "fire":
        bullet.update()
        bullet.draw()
    
    powerup.update()
    powerup.activate(player)

    # Vérifier les bombes
    for bomb in bombs:
        bomb.update()
        bomb.draw()
        if is_collision(player.x, player.y, bomb.x, bomb.y, 30):
            running = False  # Game over si une bombe touche le joueur
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"High Score: {highscore}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(highscore_text, (10, 40))
    
    player.draw()
    pygame.display.update()
    
    if score > highscore:
        highscore = score
        save_highscore(highscore)

game_over_screen()
pygame.quit()
