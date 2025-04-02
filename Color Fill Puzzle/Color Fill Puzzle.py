import pygame
import sys

SCREEN_SIZE = 500
GRID_SIZE = 5
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Црвена, Зелена, Сина, Жолта
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Color Fill Puzzle")
font = pygame.font.Font(None, 36)
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = grid[row][col] if grid[row][col] else (200, 200, 200)  # Сива ако е празна
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
def is_valid_color(row, col, color):
    neighbors = [
        (row - 1, col), (row + 1, col),
        (row, col - 1), (row, col + 1)
    ]
    for r, c in neighbors:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and grid[r][c] == color:
            return False
    return True
def is_game_complete():
    for row in grid:
        if None in row:
            return False
    return True
def main():
    running = True
    selected_color = COLORS[0]  # Првично избрана боја
    while running:
        screen.fill((255, 255, 255))
        draw_grid()
        if is_game_complete():
            text = font.render("You Win!", True, (0, 0, 0))
            screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() // 2))
        else:
            text = font.render("Select a square and color it!", True, (0, 0, 0))
            screen.blit(text, (10, SCREEN_SIZE - 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_game_complete():
                x, y = pygame.mouse.get_pos()
                col, row = x // CELL_SIZE, y // CELL_SIZE
                if row < GRID_SIZE and col < GRID_SIZE:
                    if is_valid_color(row, col, selected_color):
                        grid[row][col] = selected_color
                    else:
                        print("Invalid move! Neighboring squares cannot have the same color.")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_color = COLORS[0]
                elif event.key == pygame.K_2:
                    selected_color = COLORS[1]
                elif event.key == pygame.K_3:
                    selected_color = COLORS[2]
                elif event.key == pygame.K_4:
                    selected_color = COLORS[3]
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()