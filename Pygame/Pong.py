import pygame
import random

"""
This is a version of Pong. A ball bounces back and forth while the player tries to block
it with her paddle, gaining score points whenever successful. If the player fails to keep the ball
from hitting the left edge, they lose a try point. The game terminates when there are no tries left.

We try to make the game more difficult by incresing the ball speed randomly whenever it hits the paddle.
The speed has more chances of increasing when the score is. 
The random effect is added to make the game less schematic - if the speed was constant, 
one could predict the trajectory of the ball more easily. 
"""

score = 0
tries_left = 3

ball_width = 20
x = random.randint(150, 490) #ball coordinates
y = random.randint(200, 280)

k = 1 #indicates how fast the game gets harder (see delta_v() function). The bigger k is, the slower the difficulty increses.
sensitivity = 7 #indicates how fast the paddle moves

v_x = random.randint(2,4)
v_y = random.randint(2,4)*random.choice([-1, 1])

padd_length = 60
padd_width = 15
y_padd = 0 #paddle y-coordinate

def delta_v(score):
    """
    The function returns the change in velocity when hitting the paddle, which is
    - 1 with probability score/(score+k)
    - 0 with probability k/(score+k)
    """
    delta = random.randint(0,k+score-1)
    if delta<k: #k options
        delta = 0
    else: #the number of options equals score
        delta = 1

    return delta

def tries_left_color(tries_left):
    """
    The colour of the "Tries left: " text depends on the tries_left value.
    """
    if tries_left == 1:
        return RED
    elif tries_left == 2:
        return YELLOW
    else:
        return WHITE

#Colours
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,50,50)
BLUE=(50,50,255)
YELLOW=(255,255,0)

#Initialize PyGame
pygame.init()
x = 40
size=(640,480)
screen=pygame.display.set_mode(size)

#--Titleofnewwindow/screen
pygame.display.set_caption("Pong")

done=False

#Manages how fast screen refreshes
clock=pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True

    #user controls - moving the paddle up or down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and y_padd>0:
        y_padd += -sensitivity
    if keys[pygame.K_DOWN] and y_padd<size[1]-padd_length:
        y_padd += sensitivity

    """
    If the ball touches an edge, it bounces back. This is done by changing 
    the sign of appropriate velocity coordinate (v_x, if vertical edge, v_y, if horizontal edge).
    """
    if y <= 0 or y >= size[1]-ball_width: #lower or upper bound
        v_y *= -1
    if x >= size[0]-ball_width: #right bound
        v_x *= -1
    if x <= -abs(v_x): #left bound
        v_x *= -1
        tries_left -= 1
        if tries_left==0:
            done = True
    """
    Collision with paddle
    """
    if x <= padd_width and y_padd-padd_width<=y<=y_padd+padd_length:
        x = padd_width + 1  #this is done to prevent the ball changing its velocity more than once per hit
        v_x *= -1 #v_x is now positive

        v_x += delta_v(score) #we increase v_x (possilbly)

        if score%3 == 0: #we increse v_y every now and then, too
            if v_y>0:
                v_y += delta_v(score)
            else:
                v_y -= delta_v(score)
        
        score += 1

    #move the ball accordingly to its current velocity
    x += v_x
    y += v_y

    screen.fill(BLACK)
    pygame.draw.rect(screen,BLUE,(x, y, ball_width, ball_width))
    #pygame.draw.circle(screen,BLUE,(x, y), ball_width/2, 0)
    pygame.draw.rect(screen,WHITE,(0, y_padd, padd_width, padd_length))

    myfont = pygame.font.SysFont(None, 30) #"Comic Sans MS"
    screen.blit(myfont.render("Tries left: "+str(tries_left), 1, tries_left_color(tries_left)), (50, 0))
    screen.blit(myfont.render("Score: "+str(score), 1, WHITE), (200, 0))

    pygame.display.flip()
    clock.tick(60)

    

pygame.quit()