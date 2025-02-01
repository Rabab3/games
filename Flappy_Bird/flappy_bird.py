import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 650, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Couleurs Girly
WHITE = (255, 255, 255)
PINK = (255, 105, 180)  # Un rose clair
LIGHT_PINK = (255, 105, 180)  # Un rose plus vif
LAVENDER = (230, 220, 250)  # Une couleur lavande douce
PASTEL_PURPLE = (186, 85, 211)  # Un violet pastel
PASTEL_GREEN = (144, 238, 144)  # Un vert pastel doux
YELLOW = (255, 255, 102)  # Un jaune doux et lumineux

# Paramètres de l'oiseau
BIRD_WIDTH, BIRD_HEIGHT = 40, 30
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Paramètres des tuyaux
PIPE_WIDTH = 70
PIPE_GAP = 200
pipe_velocity = 3
pipes = []  # Liste des tuyaux

# Score
score = 0
font = pygame.font.SysFont("Arial", 30)

# Horloge
clock = pygame.time.Clock()

# Liste des nuages
clouds = []

def create_cloud():
    """Crée un nuage avec une taille aléatoire."""
    cloud_width = random.randint(80, 160)
    cloud_height = random.randint(30, 60)
    cloud_x = WIDTH
    cloud_y = random.randint(50, 150)
    return pygame.Rect(cloud_x, cloud_y, cloud_width, cloud_height)

def move_clouds():
    """Déplace les nuages vers la gauche."""
    for cloud in clouds:
        cloud.x -= 1  # Déplacement vers la gauche
        if cloud.x + cloud.width < 0:  # Si le nuage sort de l'écran
            clouds.remove(cloud)
            clouds.append(create_cloud())  # Crée un nouveau nuage à droite

def draw_clouds():
    """Dessine les nuages à l'écran."""
    for cloud in clouds:
        pygame.draw.ellipse(WIN, WHITE, cloud)  # Dessine les nuages en blanc

def draw_bird(x, y):
    """Dessine l'oiseau avec un rectangle coloré.""" 
    pygame.draw.rect(WIN, PINK, (x, y, BIRD_WIDTH, BIRD_HEIGHT))  # Oiseau en rose clair

def draw_pipes(pipes):
    """Dessine les tuyaux."""
    for pipe in pipes:
        pygame.draw.rect(WIN, PASTEL_GREEN, pipe)  # Tuyaux en vert pastel

def move_pipes(pipes):
    """Déplace les tuyaux vers la gauche."""
    for pipe in pipes:
        pipe.x -= pipe_velocity
    return pipes

def generate_pipe():
    """Génère un nouveau tuyau."""
    gap_y = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, gap_y)
    bottom_pipe = pygame.Rect(WIDTH, gap_y + PIPE_GAP, PIPE_WIDTH, HEIGHT - gap_y - PIPE_GAP)
    return top_pipe, bottom_pipe  # Retourne un tuple de deux tuyaux

def check_collision(bird, pipes):
    """Vérifie si l'oiseau entre en collision avec un tuyau."""
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.y <= 0 or bird.y + BIRD_HEIGHT >= HEIGHT:
        return True
    return False

def update_score(bird, pipes):
    """Met à jour le score si l'oiseau passe un tuyau."""
    global score
    for pipe in pipes:
        if pipe.x + PIPE_WIDTH == bird_x:
            score += 1

def display_score(score):
    """Affiche le score à l'écran."""
    score_text = font.render(f"Score: {score}", True, PINK)  # Texte en rose
    WIN.blit(score_text, (10, 10))

def draw_start_screen():
    """Affiche l'écran de démarrage avec un message et un bouton pour commencer."""
    WIN.fill(LAVENDER)  # Fond en lavande douce
    start_text = font.render("Flappy Bird", True, PINK)
    instruction_text = font.render("Appuyez sur ESPACE pour voler", True, PINK)
    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
    
    WIN.blit(start_text, (WIDTH // 2 - 70, HEIGHT // 2 - 100))
    WIN.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    pygame.draw.rect(WIN, LIGHT_PINK, start_button)  # Bouton rose vif
    start_button_text = font.render("Start", True, WHITE)
    WIN.blit(start_button_text, (WIDTH // 2 - 30, HEIGHT // 2 + 65))
    
    pygame.display.update()
    
    return start_button

def game_over():
    """Affiche l'écran de fin de jeu avec les options Rejouer et Quitter."""
    global score, pipes, bird_y, bird_velocity

    WIN.fill(LAVENDER)
    game_over_text = font.render("Game Over!", True, PINK)
    score_text = font.render(f"Final Score: {score}", True, PINK)
    replay_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 50, 100, 50)
    quit_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 50, 100, 50)
    
    WIN.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 100))
    WIN.blit(score_text, (WIDTH // 2 - 90, HEIGHT // 2 - 50))
    
    # Dessiner les boutons
    pygame.draw.rect(WIN, PASTEL_PURPLE, replay_button)
    pygame.draw.rect(WIN, YELLOW, quit_button)
    
    # Texte des boutons
    replay_text = font.render("Rejouer", True, WHITE)
    quit_text = font.render("Quitter", True, WHITE)
    WIN.blit(replay_text, (WIDTH // 2 - 110, HEIGHT // 2 + 65))
    WIN.blit(quit_text, (WIDTH // 2 + 30, HEIGHT // 2 + 65))
    
    pygame.display.update()
    
    # Attendre que l'utilisateur clique sur un bouton
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button.collidepoint(mouse_pos):
                    # Réinitialiser le jeu
                    score = 0
                    pipes = []
                    bird_y = HEIGHT // 2
                    bird_velocity = 0
                    waiting = False
                    main()  # Redémarrer le jeu
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

def main():
    global bird_y, bird_velocity, score, pipes, clouds

    # Créer des nuages au départ
    for _ in range(5):
        clouds.append(create_cloud())
    
    # Afficher l'écran de démarrage
    start_button = draw_start_screen()
    
    # Attendre que l'utilisateur clique sur le bouton pour commencer
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    waiting = False  # Arrêter d'attendre et commencer le jeu

    # Boucle principale du jeu
    running = True
    while running:
        clock.tick(30)  # Limite à 30 FPS

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = FLAP_STRENGTH

        # Mise à jour de la position de l'oiseau
        bird_velocity += GRAVITY
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)

        # Génération des tuyaux si nécessaire
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            top_pipe, bottom_pipe = generate_pipe()
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)

        # Déplacement des tuyaux
        pipes = move_pipes(pipes)

        # Suppression des tuyaux hors de l'écran
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        # Vérification des collisions
        if check_collision(bird_rect, pipes):
            game_over()
            running = False

        # Mise à jour du score
        update_score(bird_rect, pipes)

        # Déplacer les nuages
        move_clouds()

        # Affichage
        WIN.fill(LAVENDER)  # Fond en lavande
        draw_clouds()  # Dessine les nuages
        draw_bird(bird_x, bird_y)  # Dessine l'oiseau en rose
        draw_pipes(pipes)
        display_score(score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
