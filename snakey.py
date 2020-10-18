import pygame 
import random 

FPS = 10
WINWIDTH = 600
WINHEIGHT = 400
BOXSIZE = 25

BOXWIDTH = WINWIDTH / BOXSIZE
BOXHEIGHT = WINHEIGHT / BOXSIZE

BLACK = (0,   0,   0)
RED = (255,   0,   0)
GREEN = (0, 255,   0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("snake")
        self.window = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.directionX = 1
        self.directionY = 0
        self.startX = random.randint(6, BOXWIDTH -6 )
        self.startY = random.randint(6, BOXHEIGHT - 6)
        self.snakeBody = [{'x': self.startX, 'y': self.startY},
                            {'x': self.startX - 1, 'y': self.startY}]

        self.applePos = self.randomLocation()

    def runGame(self):
        self.window.fill(BLACK)
        self.drawGrid()
        self.move()
        self.events()
        self.drawSnake(self.snakeBody)
        self.drawApple(self.applePos)
        pygame.display.update()
        self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_RIGHT]:
                    self.directionX = 1
                    self.directionY = 0
                elif keys[pygame.K_LEFT]:
                    self.directionX = -1
                    self.directionY = 0
                elif keys[pygame.K_UP]:
                    self.directionX = 0
                    self.directionY = -1
                elif keys[pygame.K_DOWN]:
                    self.directionX = 0
                    self.directionY = 1
        
        # removing snake body if we havent eaten an apple 
        if not(self.snakeBody[0]['x'] == self.applePos['x'] and self.snakeBody[0]['y'] == self.applePos['y']):
            self.snakeBody.pop(-1)
        else:
            self.applePos = self.randomLocation()

        # checking for collisions 
        if self.snakeBody[0]['x'] == -1 or self.snakeBody[0]['y'] == -1 or self.snakeBody[0]['x'] == BOXWIDTH or self.snakeBody[0]['y'] == BOXHEIGHT:
            self.showGameOver()
            self.reset()
        
        # check if the snake hit itself 
        for collide in self.snakeBody[1:]:
            if (self.snakeBody[0]['x'] == collide['x'] and self.snakeBody[0]['y'] == collide['y']):
                self.showGameOver()
                self.reset()


    def move(self):
        self.snakeBody.insert(0, {'x': self.snakeBody[0]['x'] + self.directionX, 'y': self.snakeBody[0]['y'] + self.directionY})

    def drawGrid(self):
       for x in range(0, WINWIDTH, BOXSIZE):
           for y in range(0, WINHEIGHT, BOXSIZE):
               pygame.draw.line(self.window, (50, 50, 50), (x, 0), (x, WINHEIGHT))
               pygame.draw.line(self.window, (50, 50 , 50), (0, y), (WINWIDTH, y))

    def drawSnake(self, position):
        for pos in position:
            x = pos['x'] * BOXSIZE
            y = pos['y'] * BOXSIZE
            snakeRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
            pygame.draw.rect(self.window, GREEN, snakeRect)

    def drawApple(self, position):
        x = position['x'] * BOXSIZE
        y = position['y'] * BOXSIZE
        appleRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        pygame.draw.rect(self.window, RED, appleRect)

    def randomLocation(self):
        return {'x': random.randint(0, BOXWIDTH - 1), 'y': random.randint(0, BOXHEIGHT - 1)}

    def drawText(self, text, size, color, x, y):
        font = pygame.font.Font("freesansbold.ttf", size)
        fontSurf = font.render(text, True, color)
        fontRect = fontSurf.get_rect()
        fontRect.midtop = (x, y)
        self.window.blit(fontSurf, fontRect)

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

        return waiting
            
    def showStartScreen(self):
        self.window.fill(BLACK)
        self.drawText("Snake Game", 25, (255, 255, 255), WINWIDTH / 2, WINHEIGHT/ 2)
        pygame.display.update()
        self.waitForKey()

    def showGameOver(self):
        self.window.fill(BLACK)
        self.drawText("Game Over", 25, (255, 255, 255), WINWIDTH / 2, WINHEIGHT / 2)
        pygame.display.update()
        self.waitForKey()

    def reset(self):
        self.snakeBody = [{'x': self.startX, 'y': self.startY},
                            {'x': self.startX - 1, 'y': self.startY}]
        self.applePos = self.randomLocation()

game = Game()
game.showStartScreen()
while game.running:
    game.runGame()

pygame.quit()