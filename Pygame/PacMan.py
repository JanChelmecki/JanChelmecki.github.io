import pygame, random

map = [
[1,1,1,1,1,1,1,1,1,1], 
[1,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1], 
[1,1,0,1,1,1,1,1,0,1], 
[1,0,0,0,0,0,1,0,0,1],
[1,0,1,1,1,0,1,0,0,1],
[1,0,1,1,1,0,1,0,0,1], 
[1,0,1,1,1,0,1,0,0,1], 
[1,0,0,0,0,0,0,0,0,1], 
[1,1,1,1,1,1,1,1,1,1]]

class Game():
    def __init__(self, level):
        
        super().__init__()

        self.level = level
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

        #region sprites initialization
        self.all_sprites_group = pygame.sprite.Group()

        self.player = PacMan()
        self.all_sprites_group.add(self.player)

        self.wall_group = pygame.sprite.Group()

        global map
        for y in range(10):
            for x in range(10):
                if map[x][y] == 1:
                    tile = Tile(BLUE, 20, 20, 20*x, 20*y)
                    self.wall_group.add(tile)
        #endregion

    def controls(self):
        pass

    def logic(self):
        self.all_sprites_group.update()

        self.update_screen()

        self.clock.tick(60)

    def update_screen(self):
        self.screen.fill(BLACK)
        self.all_sprites_group.draw(self.screen)
        self.wall_group.draw(self.screen)
        pygame.display.flip()

    def nextlevel(self):
        pass

class Map():
    pass

class PacMan(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.color = YELLOW
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)

        self.rect = self.image.get_rect() 
        self.rect.x = 0
        self.rect.y = 0
        self.v_x = 0
        self.v_y = 0

    def update(self):
        pass

class Ghost(pygame.sprite.Sprite):
    pass

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y

class Dot(pygame.sprite.Sprite):
    pass

class Energizer(pygame.sprite.Sprite):
    pass


#colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
YELLOW=(255,255,0)

#Initialize PyGame
pygame.init()
x = 40
size=(640,480)
screen=pygame.display.set_mode(size)

#--Titleofnewwindow/screen
pygame.display.set_caption("PacMan")

done=False

#Manages how fast screen refreshes
clock=pygame.time.Clock()

g = Game(0)
i = 0
while not done and i<200:
    i+=1
    g.logic()

pygame.quit()