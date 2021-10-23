import pygame

#GlobalConstants

#Colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
RED=(255,50,50)
DARKGREEN=(0,100,0) #006400
LIGHTBLUE = (183, 218, 249) #B7DAF9
BROWN = (139,69,19) #8b4513
YELLOW=(255,255,0)

#Initialize PyGame
pygame.init()
sun_x = -40
sun_y = 175
night = 0 #indicates for how long has it been dark
size=(640,480)
screen=pygame.display.set_mode(size)

#Titleofnewwindow/screen
pygame.display.set_caption("House")

done=False

#Manages how fast screen refreshes
clock=pygame.time.Clock()

while not done:
    #user input and controls
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True
    
    #game logic

    if sun_x<size[0]+40: #daytime
        screen.fill(LIGHTBLUE)
        sun_x+=4
        sun_y+=(sun_x-4-size[0]/2)/128
    else: #nightime
        screen.fill(BLACK)
        night+=1
        if night>120: #night ends
            sun_x = -40
            sun_y = 175
            night = 0

    pygame.draw.circle(screen,YELLOW,(sun_x,sun_y),40,0)

    pygame.draw.rect(screen, DARKGREEN, (0, 315, 640, 165)) #ground
    pygame.draw.rect(screen,RED,(220,165,200,150)) #house wall
    pygame.draw.polygon(screen,BROWN,[(200, 165), (440, 165), (360, 105,), (280, 105)]) #roof
    pygame.draw.rect(screen,BLUE,(245,185,40,40)); pygame.draw.rect(screen,BLUE,(355,185,40,40)) #windows upstairs
    pygame.draw.rect(screen,BLUE,(245,185+60,40,40)); pygame.draw.rect(screen,BLUE,(355,185+60,40,40)) #windows downstairs
    pygame.draw.rect(screen,BROWN,(300,245,40,70)) #door
    pygame.draw.rect(screen,BLUE,(300,185,40,40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()