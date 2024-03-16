# sounds from: https://soundbible.com

import pygame
from random import randint

# Define constants
WIDTH, HEIGHT = 800, 600
BSIZE = 50
FPS = 30
PATH = "./assets/"

#--------------------------------------------------------------- Ball class START
class Ball(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        #self.image = pygame.image.load('/Users/kalnisp/PycharmProjects/MyGame/alien2.png').convert_alpha()
        self.image = pygame.Surface((BSIZE, BSIZE))
        self.image.set_colorkey(pygame.Color("black"))   # set transparent color
        pygame.draw.circle(self.image, pygame.Color(color), (BSIZE // 2, BSIZE // 2), BSIZE // 2)
        self.rect = self.image.get_rect()
        self.velocity = pygame.math.Vector2((4, 4))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx=0, dy=0):
        if (self.rect.x + dx) >= 0 and (self.rect.right + dx) < WIDTH:
            self.rect.x += dx
        else:
            self.velocity.x *= -1
            pygame.mixer.Sound.play(clickSound)
            score.update(-1)

        if (self.rect.y + dy) >= 0 and (self.rect.bottom + dy) < HEIGHT:
            self.rect.y += dy
        else:
            self.velocity.y *= -1
            pygame.mixer.Sound.play(clickSound)
            score.update(-1)
#--------------------------------------------------------------- Ball class END


#--------------------------------------------------------------- Brick class START
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.brickWidth, self.brickHight = BSIZE*3, BSIZE//2
        self.image = pygame.Surface((self.brickWidth, self.brickHight))
        self.color = color
        self.image.fill(pygame.Color(self.color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#--------------------------------------------------------------- Brick class END


#--------------------------------------------------------------- Score class START
class ScoreClass:
    def __init__(self, startScore=0):
        self.score = startScore
        self.brickHit = {"green": 0, "red": 0}

    def update(self, dScore, item=None):
        self.score += dScore
        if item:
            self.brickHit[item.color] += 1

    def checkGameMustEnd(self):
        mustEnd = False
        if self.score < 0:
            print('Game over')
            mustEnd = True
        elif self.brickHit["green"] >= 5 and self.brickHit["red"] >= 5:
            print("***** YOU WON *****")
            mustEnd = True
        return mustEnd


    def draw(self, screen):
        # Set up the font object
        font = pygame.font.Font(None, 36)

        # Draw the score to the screen
        score_text = font.render(f"Score: {self.score}  Green: {self.brickHit["green"]}  Red: {self.brickHit["red"]}",
                                 True, pygame.Color("white"))
        screen.blit(score_text, (10, 10))
#--------------------------------------------------------------- Score class END





pygame.init()   # initialize the GAME object in memory
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)  # Set up the game window
pygame.display.set_caption('Zombie shooter')
clock = pygame.time.Clock()

score = ScoreClass()

clickSound = pygame.mixer.Sound(PATH + 'click.wav')
laserSound = pygame.mixer.Sound(PATH + 'laser.wav')

myBall = Ball("yellow")    # spawn a ball sprite

bricks = pygame.sprite.Group()
bricks.add(Brick("red", 100,100))  # spawn a red brick sprite and add it to the bricks group
bricks.add(Brick("green", 300,100))  # spawn a green brick sprite and add it to the bricks group



#---------------------------------------------- main game loop START
running = True
while running:
    ####### all events must be handled in the for loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # window close
            running = False
        if event.type == pygame.KEYDOWN:    # some key is pressed
            if event.key == pygame.K_RIGHT:  # right arrow is pressed
                myBall.move(dx=+10)
            elif event.key == pygame.K_LEFT:  # left arrow is pressed
                myBall.move(dx=-10)
            elif event.key == pygame.K_UP:    # up arrow is pressed
                myBall.move(dy=-10)
            elif event.key == pygame.K_DOWN:  # down arrow is pressed
                myBall.move(dy=+10)

    myBall.move(dx=myBall.velocity.x, dy=myBall.velocity.y)



    ######## Draw everything
    screen.fill(pygame.Color("blue"))  # draw background
    myBall.draw(screen)
    bricks.draw(screen)
    score.draw(screen)
    pygame.display.flip()

    # check collisions
    collide = pygame.sprite.spritecollide(myBall, bricks, True)
    for item in collide:                    # multiple bricks may collide
        score.update(+3, item)
        pygame.mixer.Sound.play(laserSound)
        item.rect.x = randint(0, WIDTH - item.rect.width)
        item.rect.y = randint(0, HEIGHT - item.rect.height)
        bricks.add(item)

    if score.checkGameMustEnd():
        running = False

    clock.tick(FPS)
#---------------------------------------------- main game loop END

pygame.quit()   # remove the GAME object from memory
