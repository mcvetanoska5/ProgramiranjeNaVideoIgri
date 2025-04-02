import random, pygame, sys
from pygame.locals import *
# Game settings
FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = BLACK
# Directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0  # syntactic sugar: index of the worm's head
# Initialize global variables
tremorItem1 = None
tremorItem2 = None
yellowApple = None
blueApple = None
secondWorm = None
score = 0
gameSpeed = FPS
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')
    showStartScreen()  # Show start screen before the game starts
    while True:
        runGame(FPS)
        showGameOverScreen()
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 4)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        instructionsFont = pygame.font.Font('freesansbold.ttf', 24)
        instructionsSurf = instructionsFont.render('Press any key to start', True, WHITE)
        instructionsRect = instructionsSurf.get_rect()
        instructionsRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 1.5)
        DISPLAYSURF.blit(instructionsSurf, instructionsRect)
        pygame.display.update()
        degrees1 += 3
        degrees2 += 7
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                return  # Exit and start the game
def runGame(FPS):
    global tremorItem1, tremorItem2, yellowApple, blueApple, secondWorm, score, gameSpeed
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    apple = getRandomLocation()
    yellowApple = getRandomLocation()
    blueApple = getRandomLocation()
    tremorItem1 = getRandomLocation()
    tremorItem2 = getRandomLocation()
    secondWorm = None
    start_ticks = pygame.time.get_ticks()  # For time tracking
    while True:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Get elapsed time in seconds
        if elapsed_time > 20 and secondWorm is None:  # Add second worm after 20 seconds
            secondWorm = getRandomLocation()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        if wormCoords[HEAD]['x'] == -1:  # Wrap around the left side
            wormCoords[HEAD]['x'] = CELLWIDTH - 1
        elif wormCoords[HEAD]['x'] == CELLWIDTH:  # Wrap around the right side
            wormCoords[HEAD]['x'] = 0
        elif wormCoords[HEAD]['y'] == -1:  # Wrap around the top side
            wormCoords[HEAD]['y'] = CELLHEIGHT - 1
        elif wormCoords[HEAD]['y'] == CELLHEIGHT:  # Wrap around the bottom side
            wormCoords[HEAD]['y'] = 0
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # Game over
        # Check for collisions with special items (yellowApple, blueApple, etc.)
        if wormCoords[HEAD]['x'] == yellowApple['x'] and wormCoords[HEAD]['y'] == yellowApple['y']:
            yellowApple = getRandomLocation()
            wormCoords.pop()  # Remove one segment from the tail (shorten worm)
        if wormCoords[HEAD]['x'] == blueApple['x'] and wormCoords[HEAD]['y'] == blueApple['y']:
            blueApple = getRandomLocation()  # Reset blue apple location
            gameSpeed = max(5, gameSpeed - 5)  # Slow down the game
        if wormCoords[HEAD]['x'] == tremorItem1['x'] and wormCoords[HEAD]['y'] == tremorItem1['y']:
            score += 3  # Add points for tremorItem1
            tremorItem1 = getRandomLocation()  # Reset tremor item location
        elif wormCoords[HEAD]['x'] == tremorItem2['x'] and wormCoords[HEAD]['y'] == tremorItem2['y']:
            score += 3  # Add points for tremorItem2
            tremorItem2 = getRandomLocation()  # Reset tremor item location
        if secondWorm and wormCoords[HEAD]['x'] == secondWorm['x'] and wormCoords[HEAD]['y'] == secondWorm['y']:
            score += 1  # Add points if second worm is eaten
            wormCoords.append({'x': wormCoords[-1]['x'], 'y': wormCoords[-1]['y']})  # Grow the worm when second worm is eaten
            secondWorm = getRandomLocation()  # Reset second worm location
        # Add new head in the direction the worm is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)  # Add new head at the beginning
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawApple(yellowApple)
        drawApple(blueApple)
        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(gameSpeed)
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(gameSurf, gameRect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == QUIT:
                return  # Restart the game or quit
def drawScore(score):
    scoreSurf = BASICFONT.render(f'Score: {score}', True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormSegmentRect)
def drawApple(apple):
    x = apple['x'] * CELLSIZE
    y = apple['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
def terminate():
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
