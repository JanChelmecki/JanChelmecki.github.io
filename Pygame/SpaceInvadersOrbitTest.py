import pygame, random, math
from pygame.constants import K_SPACE

level = 7

#settings
turning = 100 #the lower the number, the faster invaders turn

bullet_speed = -8
sensitivity = 3 #how fast players move

bullets_per_player = 25
bullets_won_per_invader_hit = 3


radius = 50
#we store the parametrization of the circle so that we don't have to compute sin and cos every time we need them
circle = [(round(radius*math.cos(i/100)), round(radius*math.sin(i/100))) for i in range(628)]

#region Other global constants
size=(640,480)
pygame.font.init()
myfont = pygame.font.SysFont(None, 30)
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
RED=(255,50,50)
YELLOW=(255,255,0)
GREEN = (50, 255, 50)
PINK = (255, 255, 100)
#endregion

class Game():
    def __init__(self, level):
        
        super().__init__()

        self.level = level
        
        #region level settings
        self.progress = 0
        self.recreate_invaders = False
        if level<=3:
            self.progress_per_hit = 20
            invaders = 5*level
            hunting_invaders = 0
            invader_queens = 0
            if level == 3:
                hunting_invaders = 3
        elif 3<level<6:
            self.progress_per_hit = 10
            
            invaders = 15
            hunting_invaders = 2*(level-1)
            invader_queens = 0
            self.recreate_invaders = True
        elif level == 6:
            invaders = 0
            hunting_invaders = 0
            invader_queens = 1
        else:
            self.progress_per_hit = 5
            self.recreate_invaders = True
            invaders = 15
            hunting_invaders = 8
            invader_queens = 1
        #endregion
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("SpaceInvaders")

        #region Sprites initialization

        self.all_sprites_group = pygame.sprite.Group()
        
        #Player(s)
        self.player_group = pygame.sprite.Group()
        self.player = Player(RED, 10, 10) #create a player
        self.player_group.add(self.player)
        self.all_sprites_group.add(self.player)

        #Invaders
        self.invader_group = pygame.sprite.Group()
        for i in range(invaders):
            invader = Invader(BLUE, 10, 10)
            self.invader_group.add(invader)
            self.all_sprites_group.add(invader)

        #Hunting Invaders
        self.hunting_invader_group = pygame.sprite.Group()
        for i in range(hunting_invaders):
            hunting_invader = HuntingInvader(GREEN, 10, 10)
            self.hunting_invader_group.add(hunting_invader)
            self.invader_group.add(hunting_invader)
            self.all_sprites_group.add(hunting_invader)

        #Invader Queens
        self.queen_group = pygame.sprite.Group()
        for i in range(invader_queens):
            queen = InvaderQueen(YELLOW, 10, 10)
            self.queen_group.add(queen)
            self.all_sprites_group.add(queen)
            for minion in queen.get_minions():
                self.invader_group.add(minion)
                self.all_sprites_group.add(minion)

        #Bullets
        self.bullet_group = pygame.sprite.Group()
        #endregion

    def controls(self):
        for event in pygame.event.get(): #stops the game, if required
            if event.type==pygame.QUIT:
                global done
                done = True
            elif event.type==pygame.KEYDOWN:
                if event.key == K_SPACE:
                    if self.player.able_to_shoot():
                        self.new_bullet(self.player.get_x()+ self.player.get_width()//2, self.player.get_y())

        #player controls        
        keys = pygame.key.get_pressed()

        #horizontal movement
        if keys[pygame.K_a]:
            self.player.set_v_x(-sensitivity)
        elif keys[pygame.K_d]:
            self.player.set_v_x(sensitivity)
        else:
            self.player.set_v_x(0)

        #vertical movement
        if keys[pygame.K_w]:
            self.player.set_v_y(-sensitivity)
        elif keys[pygame.K_s]:
            self.player.set_v_y(sensitivity)
        else:
            self.player.set_v_y(0)

    def logic(self):

        self.controls()

        hit = pygame.sprite.groupcollide(self.invader_group, self.bullet_group, True, True, collided = None)
        for invader in hit:
            self.player.reward()
            if self.recreate_invaders:
                self.new_invader()
                if type(invader)==InvaderMinion:
                    self.kill_minion(invader)

        player_hit_group = pygame.sprite.spritecollide(self.player, self.invader_group, True)
        for invader in player_hit_group:
            self.player.lose_a_life()
            if type(invader)==InvaderMinion:
                self.kill_minion(invader)

        self.all_sprites_group.update()

        self.update_screen()

        self.clock.tick(60)
    
    def scoreboard(self):
        self.screen.blit(myfont.render("Lives: "+str(self.player.get_lives()), 1, WHITE), (10, 5))
        self.screen.blit(myfont.render("Bullets: "+str(self.player.get_bullets()), 1, WHITE), (10, 30))
        self.screen.blit(myfont.render("Level: "+str(self.level), 1, YELLOW), (550, 5))
        #self.screen.blit(myfont.render("Level progress: "+str(self.progress)+"%", 1, WHITE), (10, 30))

    def update_screen(self):
        self.screen.fill(BLACK)
        self.scoreboard()
        self.all_sprites_group.draw(self.screen)
        pygame.display.flip()

    def nextlevel(self): #when to end level
        if self.level<3:
            return len(self.invader_group) <= 5*(self.level)-3
        elif 3<=self.level<6:
            return len(self.hunting_invader_group) == 0
        else:
            return len(self.queen_group) == 0

    def new_bullet(self, x, y): #when somebody shoots at (x,y)
        bullet = Bullet(WHITE, 2, 10, x, y)
        self.all_sprites_group.add(bullet)
        self.bullet_group.add(bullet)

    def new_invader(self):
        invader = Invader(BLUE, 10, 10)
        self.all_sprites_group.add(invader)
        self.invader_group.add(invader)

    def target_player(self, from_x, from_y):
        x_diff = self.player.get_x()-from_x
        if self.player.get_y()-from_y<=150: #divident is dependent on y-difference
            div = 64
        else:
            div = 128
        if x_diff>=0:
            return x_diff//div+2
        else:
            return x_diff//div-1

    def kill_minion(self, minion):
        queen = minion.get_queen()
        if queen.remove_minion(minion):
            self.invader_group.add(queen)

class Invader(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        super().__init__()
         
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, 640-width) 
        self.rect.y = random.randrange(-size[1]-height, -height)

        self.width = width
        self.height = height
        self.v_x = (-1)**random.randint(0,1)
        self.v_y = random.randint(2,3)

    def update(self):
        #move horizontally
        newposition = self.rect.x + self.v_x
        if newposition >= 0 and newposition + self.width <= size[0]:
            self.rect.x = newposition
        else:
            self.v_x = -self.v_x
        
        rand = random.randint(0,turning) #change speed randomly
        if rand == 0:
            self.v_x = random.randint(-1,1)

        #move vertically
        self.rect.y += self.v_y
        if self.rect.y > size[0]+self.height:
            self.rect.y = -self.height

class HuntingInvader(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        super().__init__()
         
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.hunt = True
        self.stop = True
        self.default_hight = random.randint(0,80)

        self.turning = 50 #how often it turns when not hunting

        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, 640-width) 
        self.rect.y = random.randrange(-100-height, -height)

        self.width = width
        self.height = height
        self.v_x = 0
        self.v_y = random.randint(3,4)

    def update(self):
        if self.hunt: #attacking
            #move vertically
            self.rect.y += self.v_y
            if self.rect.y > size[0]+self.height:
                self.rect.y = -self.height
                self.stop = True
            elif self.stop and self.rect.y>=self.default_hight:
                self.stop = False
                self.hunt = False

            #move horizontally, targeting the player
            self.rect.x += g.target_player(self.rect.x, self.rect.y)
        else: #circling in the upper parts of the screen
            #move horizontally
            newposition = self.rect.x + self.v_x
            if newposition >= 0 and newposition + self.width <= size[0]:
                self.rect.x = newposition

                rand = random.randint(0,self.turning) #change speed randomly
                if rand == 0:
                    self.v_x = 3*(-1)**random.randint(0,1)
                    rand = random.randint(0, 11) #decide whether to hunt
                    if rand ==0:
                        self.hunt = True
            else:
                self.v_x = -self.v_x

class InvaderQueen(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        super().__init__()
         
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(radius+width, 640-width-radius) 
        self.rect.y = random.randrange(-size[1]-height, -height)

        self.width = width
        self.height = height
        self.v_x = 0
        self.v_y = random.randint(4,5)

        self.strike = False
        self.float = False
        self.turning = 50 #how often it turns when not hunting
        self.default_height = random.randint(radius+width, radius + 5*width)

        self.minions = []
        for i in range(6):
            self.minions.append(InvaderMinion(PINK, 10, 10, self, (628*i)//6) )

    def update(self):
        if self.strike: #attacking
            #move vertically
            self.rect.y += self.v_y
            #move horizontally, targeting the player
            self.rect.x += g.target_player(self.rect.x, self.rect.y)
            if self.rect.y>=size[1]+radius+self.width:
                self.strike = False
                self.float = True
                for minion in self.minions:
                    minion.set_angular_speed(2)
        elif self.float:
            self.rect.y -= 4
            if self.rect.y<self.default_height:
                self.float = False
        else: #circling in the upper parts of the screen
            #move horizontally
            newposition = self.rect.x + self.v_x
            if newposition >= radius and newposition + self.width + radius <= size[0]:
                self.rect.x = newposition

                rand = random.randint(0,self.turning) #change speed randomly
                if rand == 0:
                    self.v_x = 3*(-1)**random.randint(0,1)
                    rand = random.randint(0, 5) #decide whether to hunt
                    if rand ==0:
                        self.strike = True
                        self.float = False
                        for minion in self.minions:
                            minion.set_angular_speed(6)
            else:
                self.v_x = -self.v_x
    
    #region Set-Get
    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_v_x(self):
        return self.v_x

    def get_v_y(self):
        return self.v_y

    def get_minions(self):
        return self.minions

    def remove_minion(self, minion):
        self.minions.remove(minion)
        return self.minions == [] #returns True, if there are no minions left
    #endregion

class InvaderMinion(pygame.sprite.Sprite):

    def __init__(self, color, width, height, queen, phase):

        super().__init__()
         
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.phase = phase
        self.angular_speed = 2
        self.queen = queen

        self.rect.x = 0
        self.rect.y = 0

        self.width = width
        self.height = height

    def update(self):
        self.rect.x = self.queen.get_x() + circle[self.phase][0]
        self.rect.y = self.queen.get_y() + circle[self.phase][1]
        self.phase += self.angular_speed
        if self.phase >= 627:
            self.phase = 0
        """
        disp_x = self.rect.x - self.queen.get_x() #displacement from the queen
        disp_y = self.rect.y - self.queen.get_y()

        It is easy to check that a body who satisfies
            x' = y
            y' = -x
        where x' and y' denote the vertical and horizontal components of the velocity vector,
        circles around the origin. 
        
        However, the //20 and numerical errors make the motion unstable, causing the invader to move further and further away.

        self.v_x = disp_y//10 + self.queen.get_v_x() #the second term accounts for queen's motion
        self.v_y = -disp_x//10 + self.queen.get_v_y()

        self.rect.x += self.v_x
        self.rect.y += self.v_y
        """

        #region Set-Get
        def set_angular_speed(x):
            self.angular_speed = x
        #endregion

    def set_angular_speed(self, x):
        self.angular_speed = x

    def get_queen(self):
        return self.queen

class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        super().__init__()
         
        self.image = pygame.Surface([width,height]) 
        self.image.fill(color)

        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, 640-width) 
        self.rect.y = 480 - height

        self.width = width
        self.height = height
        self.v_x = 0
        self.v_y = 0

        self.score = 0
        self.lives = 5
        self.bullets = bullets_per_player

    def update(self):
        #move horizontally
        newposition = self.rect.x + self.v_x
        if newposition >= 0 and newposition + self.width <= size[0]:
            self.rect.x = newposition

        #move vertivally
        newposition = self.rect.y + self.v_y
        if newposition >= 0 and newposition + self.height <= size[1]:
            self.rect.y = newposition

    def able_to_shoot(self):
        if self.bullets>0:
            self.bullets -= 1
            return True
        else:
            return False
    
    def lose_a_life(self):
        self.lives -= 1 #take away a life point
        if self.lives <= 0:
            global done
            done = True
    
    def reward(self):
        self.score += 1
        self.bullets += bullets_won_per_invader_hit
    
    #region Set-Get
    def set_v_y(self, v_y):
        self.v_y = v_y

    def set_v_x(self, v_x):
        self.v_x = v_x

    def get_x(self):
        return self.rect.x
    
    def get_y(self):
        return self.rect.y

    def get_width(self):
        return self.width

    def get_lives(self):
        return self.lives

    def get_bullets(self):
        return self.bullets

    def get_score(self):
        return self.score
    #endregion

class Bullet(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x, y):

        super().__init__()
         
        self.image = pygame.Surface([width,height]) 
        self.image.fill(color)

        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y

        self.width = width
        self.height = height
        self.v_y = bullet_speed
    
    def update(self):
        self.rect.y += self.v_y

pygame.init()

g = Game(level) #create a game
done = False

while not done:
    g.logic()
    if g.nextlevel():
        level += 1
        g = Game(level)

pygame.quit()