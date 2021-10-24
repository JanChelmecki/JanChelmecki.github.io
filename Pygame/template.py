import pygame

#globalConstants

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
pygame.display.set_caption("MyWindow")

done=False

#Manages how fast screen refreshes
clock=pygame.time.Clock()

while not done:
    #user input and controls
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True
    
    #game logic
    if x<size[0]-40:
        x+=1

    screen.fill(BLACK)
    pygame.draw.rect(screen,BLUE,(220,165,200,150))
    pygame.draw.circle(screen,YELLOW,(x,100),40,0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()