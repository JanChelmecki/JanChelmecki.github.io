import pygame, random
from pygame.constants import KEYDOWN, KEYUP

class Invader(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed):

        super().__init__()
         
        self.image = pygame.Surface([width,height]) 
        self.image.fill(color)

        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, 640) 
        self.rect.y = random.randrange(0, 50)

        self.width = width
        self.height = height
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed

class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
       
        self.image = pygame.Surface([width,height]) 
        self.image.fill(color)
        
        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, size[0]-width) 
        self.rect.y = size[1]-height

        self.speed = 0
        self.width = width
        self.height = height
        self.lives = 5
        self.bullets = 50

    def update(self):
        newposition = self.rect.x + self.speed
        if newposition>=0 and newposition+self.width<=size[0]:
            self.rect.x = newposition

    def shoot(self):
        bullet = Bullet(WHITE, self.rect.x, self.rect.y)
        all_sprites_group.add(bullet)
        bullets_group.add(bullet)
        self.bullets -= 1

    def set_speed(self, speed):
        self.speed = speed

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, color, x, y):
        super().__init__()
       
        self.image = pygame.Surface([2,2]) 
        self.image.fill(color) 
        
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y

        self.speed = -3
        self.width = 2
        self.height = 2

    def update(self):
        self.rect.y += self.speed

#region initializationa
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
RED = (255, 50, 50)

pygame.init()
size=(640,480)
screen=pygame.display.set_mode(size)

pygame.display.set_caption("Space Invadors")

invader_group = pygame.sprite.Group() 
all_sprites_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

number_of_invaders = 10 #create invaders
for x in range(number_of_invaders):
    invader = Invader(BLUE, 20, 20, 1)
    invader_group.add(invader)
    all_sprites_group.add(invader)

player = Player(RED, 10, 10)
all_sprites_group.add(player)

clock=pygame.time.Clock()
#endregion

done = False

while not done:
    #user input and controls
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True
        elif event.type==KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.set_speed(-3)
            elif event.key == pygame.K_RIGHT:
                player.set_speed(3)
            if event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                player.set_speed(0)
    
    player_hit_group = pygame.sprite.spritecollide(player, invader_group, True)
    for enemy in player_hit_group:
        player.lives -= 1
        if player.lives == 0:
            done = True

    for bullet in bullets_group:
        bullet_hit_group = pygame.sprite.spritecollide(bullet, invader_group, True)

    screen.fill(BLACK)
    all_sprites_group.update()
    all_sprites_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()