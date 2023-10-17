import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 900
GRID_WIDTH, GRID_HEIGHT = 7, 6
CIRCLE_RADIUS = 50
MENU_WIDTH, MENU_HEIGHT = 300, 200  # Dimensions du menu

# Couleurs
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puissance 4")

# Variables pour le menu
menu_font = pygame.font.Font(None, 36)
menu_active = True  # Le menu est actif au début
selected_option = None  # Option sélectionnée dans le menu
title_text = menu_font.render("Puissance 4", True, BLACK)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

start_text = menu_font.render("Commencer", True, BLACK)
start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
quit_text = menu_font.render("Quitter", True, BLACK)
quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 350))

# Création d'une grille vide
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Fonction pour dessiner la grille de cercles
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = 100 + col * 100
            y = 100 + row * 100 + 50 
            pygame.draw.circle(screen, BLACK, (x, y), CIRCLE_RADIUS)
            if grid[row][col] == 1:
                pygame.draw.circle(screen, RED, (x, y), CIRCLE_RADIUS - 5)
            elif grid[row][col] == 2:
                pygame.draw.circle(screen, BLUE, (x, y), CIRCLE_RADIUS - 5)


# Fonction pour placer un pion dans la grille
def place_piece(col, player):
    for row in range(GRID_HEIGHT - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = player
            return True
    return False

current_player = 1

# Fonction pour vérifier les conditions de victoire
def check_win(player):
    # Vérification des victoires horizontales
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH - 3):
            if grid[row][col] == player and grid[row][col + 1] == player and grid[row][col + 2] == player and grid[row][col + 3] == player:
                return True

    # Vérification des victoires verticales
    for row in range(GRID_HEIGHT - 3):
        for col in range(GRID_WIDTH):
            if grid[row][col] == player and grid[row + 1][col] == player and grid[row + 2][col] == player and grid[row + 3][col] == player:
                return True

    # Vérification des victoires en diagonale descendante
    for row in range(GRID_HEIGHT - 3):
        for col in range(GRID_WIDTH - 3):
            if grid[row][col] == player and grid[row + 1][col + 1] == player and grid[row + 2][col + 2] == player and grid[row + 3][col + 3] == player:
                return True

    # Vérification des victoires en diagonale ascendante
    for row in range(3, GRID_HEIGHT):
        for col in range(GRID_WIDTH - 3):
            if grid[row][col] == player and grid[row - 1][col + 1] == player and grid[row - 2][col + 2] == player and grid[row - 3][col + 3] == player:
                return True

    return False


# Fonction pour afficher le joueur actuel
def display_current_player(player):
    font = pygame.font.Font(None, 36)
    if player == 1:
        text = font.render("Joueur 1 (Rouge)", True, BLACK)
    else:
        text = font.render("Joueur 2 (Bleu)", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(text, text_rect)

# Fonction pour afficher le menu
def display_menu():
    screen.fill(WHITE)  # Fond de l'écran en bleu
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.update()

# Fonction pour gérer le menu
def menu():
    global menu_active, selected_option
    while menu_active:
        display_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_rect.collidepoint(x, y):
                    menu_active = False
                    selected_option = "start"
                elif quit_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

# Boucle de jeu principale
running = True
winner = None
while running:
    if menu_active:
        menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
            x, y = event.pos
            col = (x - 100) // 100  # Calcul de la colonne en fonction de la position du clic
            if 0 <= col < GRID_WIDTH:
                if place_piece(col, current_player):
                    if check_win(current_player):
                        winner = current_player
                    else:
                        current_player = 3 - current_player  # Alterner entre les joueurs 1 et 2

                

    screen.fill(WHITE)  # Fond de l'écran en rouge
    draw_grid()
    
    # Écran de fin de partie
    if winner is not None:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Joueur {winner} gagne !", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)
        pygame.display.update()
    else :
        display_current_player(current_player)

    pygame.display.update()


