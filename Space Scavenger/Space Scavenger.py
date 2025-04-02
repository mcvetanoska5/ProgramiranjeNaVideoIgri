import pygame
import random

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
SPACESHIP_SPEED = 5
ASTEROID_SPEED = 3
CRYSTAL_SPAWN_INTERVAL = 2000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
spaceship_img = pygame.image.load("spaceship_game_resources\\spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
asteroid_img = pygame.image.load("spaceship_game_resources\\asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
energy_crystal_img = pygame.image.load("spaceship_game_resources\\energy_crystal.png")
energy_crystal_img = pygame.transform.scale(energy_crystal_img, (30, 30))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Scavenger")
g_music = pygame.mixer.Sound("spaceship_game_resources\\background_music.wav")
g_music.play(-1)
clash_sound = pygame.mixer.Sound("spaceship_game_resources\\clash_sound.wav")
spaceship_x = WINDOW_WIDTH // 2 - 25
spaceship_y = WINDOW_HEIGHT // 2 - 25
asteroids = []
crystals = []
score = 0
def get_random_position():
    x = random.randint(0, WINDOW_WIDTH - energy_crystal_img.get_width())
    y = random.randint(0, WINDOW_HEIGHT - energy_crystal_img.get_height())
    return x, y
def move_asteroids():
    global ASTEROID_SPEED
    for asteroid in asteroids:
        asteroid['y'] += ASTEROID_SPEED
        if asteroid['y'] > WINDOW_HEIGHT:
            asteroid['y'] = random.randint(-100, -30)
            asteroid['x'] = random.randint(0, WINDOW_WIDTH - asteroid_img.get_width())
    if ASTEROID_SPEED < 10:
        ASTEROID_SPEED += 0.01
def check_crystal_collection():
    global spaceship_x, spaceship_y, score
    for crystal in crystals:
        crystal_rect = pygame.Rect(crystal['x'], crystal['y'], energy_crystal_img.get_width(),
                                   energy_crystal_img.get_height())
        spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_img.get_width(), spaceship_img.get_height())
        if spaceship_rect.colliderect(crystal_rect):
            crystals.remove(crystal)
            score += 5
            if score % 5 == 0:
                global SPACESHIP_SPEED
                SPACESHIP_SPEED += 1
def check_asteroid_collision():
    global spaceship_x, spaceship_y, running
    spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_img.get_width(), spaceship_img.get_height())
    for asteroid in asteroids:
        asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], asteroid_img.get_width(), asteroid_img.get_height())
        if spaceship_rect.colliderect(asteroid_rect):
            clash_sound.play()
            pygame.display.update()
            pygame.time.delay(1000)
            return True
    return False
def main():
    global spaceship_x, spaceship_y, score, running
    last_crystal_spawn_time = pygame.time.get_ticks()
    for _ in range(5):
        asteroids.append({
            'x': random.randint(0, WINDOW_WIDTH - asteroid_img.get_width()),
            'y': random.randint(-150, -30)
        })
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= SPACESHIP_SPEED
        if keys[pygame.K_RIGHT] and spaceship_x < WINDOW_WIDTH - spaceship_img.get_width():
            spaceship_x += SPACESHIP_SPEED
        if keys[pygame.K_UP] and spaceship_y > 0:
            spaceship_y -= SPACESHIP_SPEED
        if keys[pygame.K_DOWN] and spaceship_y < WINDOW_HEIGHT - spaceship_img.get_height():
            spaceship_y += SPACESHIP_SPEED
        if pygame.time.get_ticks() - last_crystal_spawn_time > CRYSTAL_SPAWN_INTERVAL:
            x, y = get_random_position()
            crystals.append({'x': x, 'y': y})
            last_crystal_spawn_time = pygame.time.get_ticks()
        move_asteroids()
        check_crystal_collection()
        if check_asteroid_collision():
            font = pygame.font.SysFont('Arial', 48)
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False
        for asteroid in asteroids:
            screen.blit(asteroid_img, (asteroid['x'], asteroid['y']))
        for crystal in crystals:
            screen.blit(energy_crystal_img, (crystal['x'], crystal['y']))
        screen.blit(spaceship_img, (spaceship_x, spaceship_y))
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        if score >= 10:
            font = pygame.font.SysFont('Arial', 48)
            win_text = font.render("You Win!", True, RED)
            screen.blit(win_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False
        pygame.display.update()
        clock.tick(FPS)
if __name__ == "__main__":
    main()
