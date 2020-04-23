import pygame
import neat
import os
import random
import time
pygame.font.init()

c1 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/cactus1.png'))
c2 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/cactus2.png'))
fd1 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/fDinoUp.png'))
fd2 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/fDinoDown.png'))


bg = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/bg.png'))
base = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/base.png'))

cactusImages = [
    pygame.transform.scale(fd1, (fd1.get_width()-15, fd1.get_height()-15)),
    pygame.transform.scale(fd2, (fd2.get_width()-15, fd2.get_height()-15)),
    pygame.transform.scale(c1, (c1.get_width()-10, c1.get_height()-10)),
    pygame.transform.scale(c2, (c2.get_width()-10, c2.get_height()-10)),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/cactus3.png')),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/cactus4.png'))
]

dinoImages = [
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/mainDino/dino0.png')),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/mainDino/dino1.png')),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/mainDino/dino2.png')),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/mainDino/dino3.png')),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/mainDino/dino4.png')),
    pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/mainDino/dino5.png'))
]

WIDTH = bg.get_width()
HEIGHT = bg.get_height()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Google T-rex game using NEAT')
ANIMATION_TIME = 5

VELOCITY = 15
SCORE = 0
HIGHEST = 0
ALIVE = 100


class Background:
    global WINDOW, bg, WIDTH

    def __init__(self):
        self.x1 = 0
        self.x2 = bg.get_width()
        self.image = bg
        self.velocity = 1

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.image.get_width() <= 0:
            self.x1 = self.x2 +  WIDTH

        if self.x2 + self.image.get_width() <= 0:
            self.x2 = self.x1 +  WIDTH

    def draw(self):
        WINDOW.blit(self.image, (self.x1,0))
        WINDOW.blit(self.image, (self.x2,0))

class Base:

    global WINDOW, base, WIDTH, VELOCITY

    def __init__(self, y):
        self.x1 = 0
        self.x2 = base.get_width()
        self.y = y
        self.velocity = VELOCITY
        self.image = base

    def move(self):
        self.x1 -= VELOCITY
        self.x2 -= VELOCITY

        if self.x1 + self.image.get_width() <= 0:
            self.x1 = self.x2 + self.image.get_width()

        if self.x2 + self.image.get_width() <= 0:
            self.x2 = self.x1 + self.image.get_width()

    def draw(self):
        WINDOW.blit(self.image, (self.x1, self.y))
        WINDOW.blit(self.image, (self.x2, self.y))

class Dino:
    global dino, WINDOW, ANIMATION_TIME, duckDino1, duckDino2, dinoImages
    
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.tickCount = 10
        self.images = dinoImages
        self.image = dinoImages[0]
        self.imageCount = 0
        self.height = y
        self.acceleration = 1
        self.velocity = 5
        self.jumped = False
        self.duck = False


    def move(self):
        if self.jumped:
            self.duck = False
            self.imageCount = 99
            a = self.acceleration
            if self.tickCount >= -10:
                if self.tickCount < 0:
                    a  = -self.acceleration

                self.y -= (self.tickCount ** 2) * 0.5 * a
                self.tickCount -= 1
            else:
                self.jumped = False
                self.tickCount = 10
                self.imageCount = 0
    

    def draw(self):

        if self.duck:                                  #duck
            self.imageCount += 1

            if self.imageCount <= ANIMATION_TIME:
                self.image = self.images[4]

            elif self.imageCount <= ANIMATION_TIME*2:
                self.image = self.images[5]
            
            elif self.imageCount <= ANIMATION_TIME*3:
                self.image = self.images[4]
                self.imageCount = 0
            
        else:
            if self.imageCount == 99:               #jump
                self.image = self.images[0]
            
            else:                                   #move forward
                self.imageCount += 1            
                if self.imageCount <= ANIMATION_TIME:
                    self.image = self.images[1]

                elif self.imageCount <= ANIMATION_TIME*2:
                    self.image = self.images[2]
                
                elif self.imageCount <= ANIMATION_TIME*3:
                    self.image = self.images[1]
                    self.imageCount = 0

        WINDOW.blit(self.image, (self.x,self.y-self.image.get_height()))

class Cactus:

    global WINDOW, WIDTH, cactusImages, VELOCITY, fDinoImages

    def __init__(self, y):
        self.imageIndex = random.randrange(1,6)
        self.image = cactusImages[self.imageIndex]
        self.x = WIDTH
        x = 0
        if self.imageIndex == 1:
            x = 80
        self.y = y - self.image.get_height() - x
        self.imageCount = 0

    def move(self):
        self.x -= VELOCITY

    def draw(self):
        if self.imageIndex == 0 or self.imageIndex == 1:
            self.imageCount += 1
            
            if self.imageCount <= ANIMATION_TIME:
                self.image = cactusImages[0]

            elif self.imageCount <= ANIMATION_TIME*2:
                self.image = cactusImages[1]

            elif self.imageCount <= ANIMATION_TIME*3:
                self.image = cactusImages[0]
                self.imageCount = 0
        
            WINDOW.blit(self.image, (self.x,self.y))

        else:
            self.image = cactusImages[self.imageIndex]
            WINDOW.blit(self.image, (self.x, self.y))

class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def collision(cactus, dino):
    dBox = (dino.x, dino.y-dino.image.get_height(), dino.image.get_width(), dino.image.get_height())
    cBox = (cactus.x, cactus.y , cactus.image.get_width(), cactus.image.get_height())

    rect1 = pygame.draw.rect(WINDOW, (247, 247,247), dBox, 1)
    rect2 = pygame.draw.rect(WINDOW, (247, 247,247), cBox, 1)

    # pygame.draw.line(
    #     WINDOW, 
    #     (255, 0,0), 
    #     (dino.x + dino.image.get_width(), (dino.y-dino.image.get_height())), 
    #     (cactus.x, cactus.y), 
    #     5
    # )

    # pygame.draw.line(
    #     WINDOW, 
    #     (255, 0,0), 
    #     (dino.x + dino.image.get_width(), (dino.y)), 
    #     (cactus.x, cactus.y+cactus.image.get_height()),
    #     5
    # )

    # print(
    #     abs(cactus.x - (dino.x + dino.image.get_width())),      #horizontal distance
    #     cactus.y - (dino.y - dino.image.get_height()),                                        #vertical distance
    #     VELOCITY
    # )

    if rect1.colliderect(rect2) or rect2.colliderect(rect1):
        return True
    return False



def mainComputer(genomes, config):
    global WINDOW, VELOCITY, SCORE, HIGHEST, ALIVE

    with open('/home/aryan/Desktop/Dino Game/highestScoreMachine.txt', 'r') as f:
        HIGHEST = int(f.readline())
        f.close()

    g = []
    dinos = []
    nets = []


    for genomeID, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        g.append(genome)
        dinos.append(Dino(100, 330+94))


    tickCount = 0
    time = pygame.time.Clock()

    run = True

    bg = Background()
    base = Base(400)
    cactus = [Cactus(425)]

    while run :

        bg.draw()
        base.draw()

        tickCount += 1
        SCORE = tickCount
        time.tick(30)

        if tickCount % 100 == 0 and VELOCITY < 25.0:
            VELOCITY += 0.20
            print(f'Velocity increased : {VELOCITY}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(dinos) < 1:
            run = False
            break


        for x, dino in enumerate(dinos):
            g[x].fitness += 0.1
            dino.move()

            output = nets[x].activate((
                abs(cactus[-1].x - (dino.x + dino.image.get_width())),
                cactus[-1].y - (dino.y - dino.image.get_height()),
                VELOCITY
            ))

            if output[0] > 0.5:
                dino.jumped = True
                dino.duck = False
            else:
                dino.duck = True

        for c in cactus:
            passed = False
            c.draw()
            c.move()

            if dino.x  > c.x + c.image.get_width():
                passed = True

        for dino in dinos:
            if collision(cactus[-1], dino):
                g[dinos.index(dino)].fitness -= 1
                nets.pop(dinos.index(dino))
                g.pop(dinos.index(dino))
                dinos.pop(dinos.index(dino))

        if passed:
            cactus.append(Cactus(425))
            for genome in g:
                genome.fitness += 5
        else:
            ALIVE -= 1

        if cactus[0].x + cactus[0].image.get_width() < 0:
            cactus.pop(0)

        for dino in dinos:
            dino.draw()

        # dino.draw()

        if cactus[0].x + cactus[0].image.get_width() <= 0:
            cactus.append(Cactus(425))
            cactus.pop(0)

        bg.move()
        base.move()
        # dino.move()

        # collision(cactus[-1], dino)

        # if(collision(cactus[-1], dino)):
            # run = False
            # print(f'Score {SCORE}')

        # cactus[-1].move()
        # showScore()

        WINDOW.blit(pygame.font.Font('freesansbold.ttf', 32).render(f'HIGHEST : {HIGHEST}  Alive : {len(dinos)}  Score : {SCORE}', True, (0,0,0)), (50, 10))

        pygame.display.update()

    if SCORE > HIGHEST:
        with open('/home/aryan/Desktop/Dino Game/highestScoreMachine.txt', 'w') as f:
            f.write(str(SCORE))
        f.close()
    
    pygame.quit()

def mainManual():
    global WINDOW, VELOCITY, SCORE, HIGHEST, ALIVE

    with open('/home/aryan/Desktop/Dino Game/highestScoreHuman.txt', 'r') as f:
        HIGHEST = int(f.readline())
        f.close()

    tickCount = 0
    time = pygame.time.Clock()

    run = True
    alive = True

    bg = Background()
    base = Base(400)
    cactus = [Cactus(425)]
    dino = Dino(100, 330+94)

    while run :

        tickCount += 1
        time.tick(30)

        if alive : 
            SCORE = tickCount

            bg.draw()
            base.draw()

            if tickCount % 100 == 0 and VELOCITY < 25.0:
                VELOCITY += 0.20
                print(f'Velocity increased : {VELOCITY}')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dino.jumped = True
                        dino.duck = False
                    if event.key == pygame.K_DOWN:
                        dino.duck = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dino.duck = False

            for c in cactus:
                passed = False
                c.draw()
                c.move()

                if dino.x  > c.x + c.image.get_width():
                    passed = True

            if passed:
                cactus.append(Cactus(425))

            if collision(cactus[-1], dino):
                alive = False
        
            if cactus[0].x + cactus[0].image.get_width() < 0:
                cactus.pop(0)

            dino.draw()

            if cactus[0].x + cactus[0].image.get_width() <= 0:
                cactus.append(Cactus(425))
                cactus.pop(0)

            bg.move()
            base.move()
            dino.move()

            WINDOW.blit(pygame.font.Font('freesansbold.ttf', 32).render(f'HIGHEST : {HIGHEST}  Alive : {1}  Score : {SCORE}', True, (0,0,0)), (50, 10))

            pygame.display.update()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            WINDOW.blit(pygame.font.Font('freesansbold.ttf', 78).render(f'Your score : {SCORE}', True, (0,0,0)), (50, 200))
            pygame.display.update()

            if SCORE > HIGHEST:
                with open('/home/aryan/Desktop/Dino Game/highestScoreHuman.txt', 'w') as f:
                    f.write(str(SCORE))
                f.close()
    
    pygame.quit()



def run(configFile):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        configFile
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    
    stats =  neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(mainComputer, n=50)

def modeSelection():

    run = True
    while run:
        b1 = Button((245,195,194), 80, 100, 600, 100, text='Manual mode')
        b2 = Button((176,223,229), 80, 300, 600, 100, text='Automatic mode')

        b1.draw(WINDOW)
        b2.draw(WINDOW)

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.isOver(pos):
                    run = False
                    return True
                elif b2.isOver(pos):
                    run = False
                    return False
        

        pygame.display.update()



if __name__ == "__main__":
    if modeSelection():
        mainManual()
    else:
        run(os.path.join(os.path.dirname(__file__), 'config.txt'))
