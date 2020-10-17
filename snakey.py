import random
import pygame

FPS = 10
WINWIDTH = 600
WINHEIGHT = 400
BOXSIZE = 20

BOXWIDTH = WINWIDTH / BOXSIZE
BOXHEIGHT = WINHEIGHT / BOXSIZE

BLACK = (0,   0,   0)
RED = (255,   0,   0)
GREEN = (0, 255,   0)


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('snake')
        self.window = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.directionX = 1
        self.directionY = 0
        self.startX = random.randint(5, BOXWIDTH - 6)
        self.startY = random.randint(5, BOXHEIGHT - 6)
        self.wormBody = [{'x': self.startX, 'y': self.startY},
                         {'x': self.startX - 1, 'y': self.startY}]

        self.applePos = self.randomLocation()


    def runGame(self):
        self.window.fill(BLACK)
        self.drawGrid()
        self.move()
        self.events()
        self.drawWorm(self.wormBody)
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
    
        if not (self.wormBody[0]['x'] == self.applePos['x'] and self.wormBody[0]['y'] == self.applePos['y']):
            self.wormBody.pop(-1)
        else:
            self.applePos = self.randomLocation()

        if self.wormBody[0]['x'] == -1 or self.wormBody[0]['y'] == -1 or self.wormBody[0]['x'] == BOXWIDTH or self.wormBody[0]['y'] == BOXHEIGHT:
            self.showGameOver()
            self.reset()

        for collide in self.wormBody[1:]:
            if (self.wormBody[0]['x'] == collide['x'] and self.wormBody[0]['y'] == collide['y']) :
                self.showGameOver()
                self.reset()


    def move(self):
        self.wormBody.insert(0, {'x': self.wormBody[0]['x'] + self.directionX, 'y': self.wormBody[0]['y'] + self.directionY})
        pygame.display.update()


    def drawGrid(self):
        for x in range(0, WINWIDTH, BOXSIZE):
            for y in range(0, WINHEIGHT, BOXSIZE):
                pygame.draw.line(self.window, (50, 50, 50), (x, 0), (x, WINHEIGHT))
                pygame.draw.line(self.window, (50, 50, 50), (0, y), (WINWIDTH, y))

    def drawWorm(self, position):
        for pos in position:
            x = pos['x'] * BOXSIZE
            y = pos['y'] * BOXSIZE
            wormRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
            pygame.draw.rect(self.window, GREEN, wormBody)
            

    def drawApple(self, pos):
        x = pos['x'] * BOXSIZE
        y = pos['y'] * BOXSIZE
        appleRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
        pygame.draw.ellipse(self.window, RED, appleRect)

    def drawText(self, text,size, color, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
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
        if not waiting:
            return False
                    
    def showStartScreen(self):
        self.window.fill(BLACK)
        self.drawText('Snake', 25, (255, 255, 255), WINWIDTH / 2, WINHEIGHT / 2)
        pygame.display.update()
        self.waitForKey()

    def showGameOver(self):
        self.window.fill(BLACK)
        self.drawText("GaMe OvEr", 25, (255, 255, 255), WINWIDTH / 2, WINHEIGHT / 2)
        pygame.display.update()
        self.waitForKey()

    def randomLocation(self):
        return {'x': random.randint(0, BOXWIDTH - 1), 'y': random.randint(0, BOXHEIGHT - 1)}

    def reset(self):
        self.wormBody = [{'x':self.startX, 'y':self.startY}, {'x':self.startX - 1, 'y':self.startY}]
        self.applePos = self.randomLocation()

game = Game()
game.showStartScreen()
while game.running:
    game.runGame()

pygame.quit()
