import pygame, random

class Snow(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed): 
        # Call the sprite constructor  
        super().__init__() 
        # Create a sprite and fill it with colour 
        self.image = pygame.Surface([width,height]) 
        self.image.fill(color) 
        # Set the position of the sprite 
        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, 600) 
        self.rect.y = random.randrange(0, 400)
        self.speed = speed
    
    def update(self):
        if self.rect.y <= size[1]:
            self.rect.y += self.speed
        else:
            self.rect.y = 0


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
pygame.display.set_caption("Snow")

done=False

snow_group = pygame.sprite.Group() 
all_sprites_group = pygame.sprite.Group()

number_of_flakes = 50 # we are creating 50 snowflakes
for x in range (number_of_flakes): 
    my_snow = Snow(WHITE, 5, 5, random.randint(1,2)) # snowflakes are white with size 5 by 5 px
    snow_group.add (my_snow) # adds the new snowflake to the group of snowflakes
    all_sprites_group.add (my_snow) # adds it to the group of all Sprites

#Manages how fast screen refreshes
clock=pygame.time.Clock()

while not done:
    #user input and controls
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True

    screen.fill(BLACK)
    all_sprites_group.update()
    all_sprites_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()