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

# Position et vitesse du joueur
player_x = WIDTH // 2 - 32
player_y = HEIGHT - 80
player_speed = 5

# Liste des ennemis
num_enemies = 6
enemies = []
bombs = []
for i in range(num_enemies):
    enemies.append({
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, 150),
        "speed_x": 0.02,
        "speed_y": 0.02
    })

# Projectile
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"

# Power-up
powerup = {"x": random.randint(50, WIDTH - 50), "y": -50, "speed": 0.5, "active": False, "type": "speed"}  

# Score
score = 0
enemies_destroyed = 0
font = pygame.font.Font(None, 36)

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 22, y - 20))

def is_collision(obj_x, obj_y, target_x, target_y, threshold):
    distance = ((obj_x - target_x) ** 2 + (obj_y - target_y) ** 2) ** 0.5
    return distance < threshold

def game_over_screen():
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
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x
        fire_bullet(bullet_x, bullet_y)
    
    for enemy in enemies:
        enemy["x"] += enemy["speed_x"]
        
        if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 64:
            enemy["speed_x"] *= -1
            enemy["y"] += enemy["speed_y"]
        
        if is_collision(enemy["x"], enemy["y"], bullet_x, bullet_y, 30):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemies_destroyed += 1
            enemy["x"] = random.randint(50, WIDTH - 50)
            enemy["y"] = random.randint(50, 150)
            
            if random.random() < 0.2:
                powerup["x"] = enemy["x"]
                powerup["y"] = enemy["y"]
                powerup["active"] = True
                powerup["type"] = random.choice(["speed", "bullet"])

        if random.random() < 0.005:
            bombs.append({"x": enemy["x"], "y": enemy["y"], "speed": 4})

        draw_enemy(enemy["x"], enemy["y"])
    
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"

    if powerup["active"]:
        screen.blit(powerup_img, (powerup["x"], powerup["y"]))
        powerup["y"] += powerup["speed"]
        if is_collision(player_x, player_y, powerup["x"], powerup["y"], 40):
            powerup["active"] = False
            if powerup["type"] == "speed":
                player_speed += 2
            elif powerup["type"] == "bullet":
                bullet_speed += 3
    
    for bomb in bombs:
        screen.blit(bomb_img, (bomb["x"], bomb["y"]))
        bomb["y"] += bomb["speed"]
        if is_collision(player_x, player_y, bomb["x"], bomb["y"], 30):
            running = False
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"High Score: {highscore}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(highscore_text, (10, 40))
    
    draw_player(player_x, player_y)
    pygame.display.update()
    
    if score > highscore:
        highscore = score
        save_highscore(highscore)

def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

highscore = load_highscore()

def draw_text(text, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, 36)
    screen.blit(font.render(text, True, color), (x, y))

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, x + 15, y + 10)
    return pygame.Rect(x, y, w, h)

def game_over_screen(score):
    global highscore
    if score > highscore:
        highscore = score
        save_highscore(highscore)

    screen.fill((245, 245, 220))  # Beige
    draw_text("GAME OVER", 320, 200, (255, 0, 0))
    draw_text(f"Score: {score}", 320, 250)
    draw_text(f"High Score: {highscore}", 320, 300)

    replay_button = draw_button("Rejouer", 320, 350, 120, 40, (0, 255, 0))
    quit_button = draw_button("Quitter", 320, 410, 120, 40, (0, 0, 255))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return True  # Rejouer
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        pygame.time.delay(100)
        
if not game_over_screen(score):  # Si le joueur choisit de quitter
    running = False
    pygame.quit()
    exit()

pygame.quit()
print(f"Game Over! Score final: {score}, Ennemis détruits: {enemies_destroyed}, High Score: {highscore}")
            