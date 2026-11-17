import pygame
import random
import sys

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Temple Run")
clock = pygame.time.Clock()

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)

# --- Game Variables ---
player_rect = pygame.Rect(100, HEIGHT - 100, 40, 60)
velocity_y = 0
gravity = 1
jump_strength = -18
is_jumping = False

obstacles = []
spawn_timer = 0
spawn_delay = 60  # Frames between spawns
speed = 7

score = 0
game_over = False
font = pygame.font.SysFont("Arial", 30, bold=True)

# --- Main Game Loop ---
while True:
    # 1. Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                velocity_y = jump_strength
                is_jumping = True
            if event.key == pygame.K_r and game_over:
                # Reset Game
                player_rect.y = HEIGHT - 100
                obstacles.clear()
                score = 0
                speed = 7
                game_over = False

    if not game_over:
        # 2. Player Physics (Jumping & Gravity)
        velocity_y += gravity
        player_rect.y += velocity_y
        
        # Ground collision
        if player_rect.y >= HEIGHT - 100:
            player_rect.y = HEIGHT - 100
            velocity_y = 0
            is_jumping = False

        # 3. Spawn Obstacles
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            obs_height = random.randint(30, 70)
            obs_rect = pygame.Rect(WIDTH, HEIGHT - 40 - obs_height, 30, obs_height)
            obstacles.append(obs_rect)

        # 4. Move Obstacles & Check Collisions
        for obs in obstacles[:]:
            obs.x -= speed
            if obs.x + obs.width < 0:
                obstacles.remove(obs)
                score += 1
            
            # Collision Detection
            if player_rect.colliderect(obs):
                game_over = True

        # Increase difficulty over time
        speed = 7 + (score // 10)

    # 5. Drawing Everything
    screen.fill(BLACK)
    
    # Draw Ground
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - 40, WIDTH, 40))
    
    # Draw Player
    pygame.draw.rect(screen, GREEN, player_rect)
    
    # Draw Obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    # Draw UI
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        go_text = font.render("GAME OVER! Press 'R' to Restart", True, RED)
        screen.blit(go_text, (WIDTH//2 - 220, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60) # 60 FPS