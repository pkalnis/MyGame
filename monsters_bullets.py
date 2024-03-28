# sounds from: https://soundbible.com

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, color, pos, velocity):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((5, 5))
        self.color = color
        self.image.fill(pygame.Color(self.color))
        self.rect = self.image.get_rect()
        self.pos = self.image.get_rect()
        self.pos.x, self.pos.y = pos.x, pos.y
        self.velocity = pygame.Vector2(velocity)

        pygame.mixer.Sound.play(self.game.laserSound)


    def update(self):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.rect.x = self.pos.x + self.game.rect.x
        self.rect.y = self.pos.y + self.game.rect.y

        if self.rect.x < 0 or self.rect.x > self.game.width:
            self.kill()

        if self.rect.y < 0 or self.rect.y > self.game.height:
            self.kill()






#--------------------------------------------------------------- Player class START
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.costumes = self.load_costumes(PATH + 'alien2.png')
        self.costume = 'right'
        self.image = self.costumes[self.costume]
        self.rect = self.image.get_rect()
        self.pos = self.image.get_rect()
        self.pos.center = (self.game.world.width // 2, self.game.world.height // 2)

    def load_costumes(self, fname):
        costumes = {}
        costumes['base'] = pygame.transform.scale_by(pygame.image.load(fname).convert_alpha(), 0.3)
        costumes['right'] = costumes['base']
        costumes['left'] = pygame.transform.flip(costumes['base'], True, False)
        costumes['up'] = pygame.transform.rotate(costumes['base'], 90)
        costumes['down'] = pygame.transform.rotate(costumes['base'], -90)
        return costumes

    def change_costume(self, costume):
        self.costume = costume
        self.image = self.costumes[costume]

    def draw(self, screen):
        self.rect.x = self.pos.x + self.game.rect.x
        self.rect.y = self.pos.y + self.game.rect.y
        screen.blit(self.image, self.rect)

    def update(self, movement):
        dx = (movement['right'] - movement['left']) * 5
        dy = (movement['down'] - movement['up']) * 5

        if dx>0: self.change_costume('right')
        elif dx<0: self.change_costume('left')
        elif dy>0: self.change_costume('down')
        elif dy<0: self.change_costume('up')

        if (self.pos.x + dx) >= 0 and (self.pos.right + dx) < self.game.world.width:
            self.pos.x += dx

        if (self.pos.y + dy) >= 0 and (self.pos.bottom + dy) < self.game.world.height:
            self.pos.y += dy

        return self.pos

    def fire(self, bullets):
        step = 10
        bPos = pygame.Vector2(self.pos.center)
        bVelocity = pygame.Vector2(0,0)
        color = "black"
        match self.costume:
            case 'right':
                bPos.y += 19
                bVelocity.x = step
                color = "blue"
            case 'left':
                bPos.y += 19
                bVelocity.x = -step
                color = "green"
            case 'up':
                bPos.x += 19
                bVelocity.y = -step
                color = "pink"
            case 'down':
                bPos.x += -25
                bVelocity.y = step
                color = "red"
            case _:
                print("Unknown costume")

        bullets.add(Bullet(self.game, color, bPos, bVelocity))

#--------------------------------------------------------------- Player class END




#--------------------------------------------------------------- Game class START
class Game():
    def __init__(self, width, height, fps, caption):
        pygame.init()   # initialize the GAME object in memory
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF) # Set up the game window
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.image = pygame.transform.scale_by(pygame.image.load(PATH + 'background.png').convert(), 2.0)
        self.rect = self.image.get_rect()
        self.world = self.image.get_rect()     # size of the virtual world

        self.laserSound = pygame.mixer.Sound(PATH + 'laser.wav')

        self.movement={'up':False, 'down':False, 'left':False, 'right':False}

        self.player = Player(self)
        self.bullets = pygame.sprite.Group()


    # returns True if the game should continue running
    # returns False if the game must terminate
    def event_handler(self):
        for event in pygame.event.get(): #all events must be handled in the for loop
            if event.type == pygame.QUIT:  # window close
                return False
            if event.type == pygame.KEYDOWN:  # some key is pressed
                if event.key == pygame.K_RIGHT:  # right arrow is pressed
                    self.movement['right'] = True
                elif event.key == pygame.K_LEFT:  # left arrow is pressed
                    self.movement['left'] = True
                elif event.key == pygame.K_UP:  # up arrow is pressed
                    self.movement['up'] = True
                elif event.key == pygame.K_DOWN:  # down arrow is pressed
                    self.movement['down'] = True
                elif event.key == pygame.K_SPACE:
                    self.player.fire(self.bullets)
            if event.type == pygame.KEYUP:  # some key is released
                if event.key == pygame.K_RIGHT:  # right arrow is released
                    self.movement['right'] = False
                elif event.key == pygame.K_LEFT:  # left arrow is released
                    self.movement['left'] = False
                elif event.key == pygame.K_UP:  # up arrow is released
                    self.movement['up'] = False
                elif event.key == pygame.K_DOWN:  # down arrow is released
                    self.movement['down'] = False
        return True

    def view_camera(self, playerPos):
        camera = pygame.Rect(-self.rect.x, -self.rect.y, self.width, self.height)

        if playerPos.x < camera.x:
            self.rect.x += camera.x - playerPos.x
        if playerPos.right > camera.right:
            self.rect.x += camera.right - playerPos.right
        if playerPos.y < camera.y:
            self.rect.y += camera.y - playerPos.y
        if playerPos.bottom > camera.bottom:
            self.rect.y += camera.bottom - playerPos.bottom


    def run(self):                          # main game loop
        running = True
        while running:
            running = self.event_handler()

            playerPos = self.player.update(self.movement)
            self.view_camera(playerPos)

            self.bullets.update()

            ######## Draw everything
            self.screen.blit(self.image, self.rect)  # draw background
            self.bullets.draw(self.screen)
            self.player.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(FPS)

        pygame.quit()  # remove the GAME object from memory

#--------------------------------------------------------------- Game class END




#######################################################################################################
#                                   MAIN program starts here                                          #
#######################################################################################################

# Define constants
WIDTH, HEIGHT, FPS = 1200, 800, 30
PATH = "/Users/kalnisp/Dropbox (KAUST)/_TEACHING/MIT 60001 - Intro to Python/Projects/MyGame/assets/"

monsterGame = Game(WIDTH, HEIGHT, FPS, "shooting the enemies")
monsterGame.run()



