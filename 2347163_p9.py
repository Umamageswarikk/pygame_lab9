
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Dropper")

# Load images
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
jet_img = pygame.image.load("jet4new.png")
jet_img = pygame.transform.scale(jet_img, (200, 100))
bomb_img = pygame.image.load("bn.png")
bomb_img = pygame.transform.scale(bomb_img, (40, 40))
explosion_img = pygame.image.load("expnew.png")
explosion_img = pygame.transform.scale(explosion_img, (100, 100))
house_img = pygame.image.load("house3new.png")
house_img = pygame.transform.scale(house_img, (150, 150))

# Fonts
font = pygame.font.Font(None, 36)

# Variables
score = 0
jet_x = WIDTH - 100
jet_y = 50
bombs = []
explosions = []

house_x = WIDTH // 2 - 75
house_y = HEIGHT - 250
hit_count = 0

clock = pygame.time.Clock()

# Function to create a new bomb
def create_bomb():
    return {'x': random.randint(jet_x, jet_x + 100), 'y': jet_y + 50}

# Main game loop
running = True
while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            house_x, _ = event.pos

    # Move jet continuously from right to left
    jet_x -= 1
    if jet_x < -100:
        jet_x = WIDTH

    # Draw jet
    screen.blit(jet_img, (jet_x, jet_y))

    # Drop bombs like rain from the jet
    if random.random() < 0.05:  # Adjust bomb drop frequency
        bombs.append(create_bomb())

    # Move and draw bombs
    for bomb in bombs:
        bomb['y'] += 5
        if bomb['y'] > HEIGHT:
            bombs.remove(bomb)
        else:
            screen.blit(bomb_img, (bomb['x'], bomb['y']))

    # Check for collision with house
    for bomb in bombs:
        if house_x < bomb['x'] < house_x + 150 and house_y < bomb['y'] < house_y + 150:
            explosions.append({'x': house_x + 25, 'y': house_y + 25})
            bombs.remove(bomb)
            score += 1
            hit_count += 1

    # Draw and move explosions
    for explosion in explosions:
        screen.blit(explosion_img, (explosion['x'], explosion['y']))
        explosion['x'] += 1  # Move the explosion to display other explosions
        if explosion['x'] > WIDTH:
            explosions.remove(explosion)

    # Draw house
    screen.blit(house_img, (house_x, house_y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game over if hit by more than 3 bombs
    if hit_count > 3:
        game_over_text = font.render("Game Over! You got hit by too many bombs!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 300, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
