import pygame, random

grid = [
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

def next(i,j, dir):
    if dir == 0: #right
        return (i, j+1)
    elif dir == 1: #up
        return (i-1, j)
    elif dir == 2: #left
        return (i, j-1)
    else: #dir == 3 down
        return (i+1, j)
    

class Corner():
    def __init__(self, x, y, r = -1, u = -1, l = -1, d = -1):
        self.x = x
        self.y = y
        self.neighbours = [r, u, l, d]

    def get_neighbour(self, dir):
        return self.neighbours[dir]

    def set_neighbour(self, dir, a_corner):
        self.neighbours[dir] = a_corner

    def is_node(self):
        return self.neighbours.count(-1) != 2

class Map():
    def __init__(self, grid):
        self.grid = grid

        #initialize corners
        self.corner = []

        #find all the corners
        corner_pos = {} #mark corners 'on the grid' temporarily with dictionary {[i,j]:corner number}
        for i in range(1, len(grid)-1):
            for j in range(1, len(grid[i])-1):
                if grid[i][j] == 0: #not a wall
                    vert = 0 #count vertical neighbours
                    if grid[i+1][j]==0:
                        vert += 1
                    if grid[i-1][j]==0:
                        vert += 1
                    hor = 0 #count horizontal neighbours
                    if grid[i][j+1]==0:
                        hor += 1
                    if grid[i][j-1]==0:
                        hor += 1

                    if hor*vert != 0 or hor+vert == 1: #junction/branch/turn or dead end
                        new = Corner(20*j, 20*i) #create a new corner, with no neighbours yet
                        corner_pos[i,j] = len(self.corner) #mark its position 'on the grid'
                        self.corner.append(new)
        
        #connect the corners
        for current in range(len(self.corner)):
            for dir in range(4): #check in all four directions
                if self.corner[current].get_neighbour(dir) == -1: #no known neighbour in the dir direction
                    (k, l) = next(i, j, dir)
                    if grid[k,l] == 0: #there is a neighbour in the dir direction
                        while not (k,l) in corner_pos: #explore in the dir direction until reaching a corner
                            (k,l) = next(k, l, dir)
                        self.corner[current].set_neighbour(dir, corner_pos[k,l]) #connect current to found
                        self.corner[corner_pos[k,l]].set_neighbour((dir+2)%4, current) #connect found to current

        #initialize nodes
        self.node = {}
        self.f = {}

        node_nums = [i for i in range(0, len(self.corner)) if self.corner[i].is_node()] #mark all the nodes temporarily
        for i in node_nums:
            adjacent = [] #neighbouring nodes
            for dir in range(4): #explore in dir direction until meeting a node
                d = dir
                current = self.get_next(self.corner[i], dir)
                if current == -1: #no neighbour
                    adjacent.append(-1)
                else:
                    while current not in node_nums: #not a node, just a corner
                        count = 0 #look for the other neighbour
                        while count<3 and self.get_next(current, d) == -1:
                            d = (d+1)%4 #turn 90deg anticlockwise
                            count += 1
                        current = self.get_next(current, d) #move to the next corner
                    adjacent.append(self.get_next(current, d))
            self.node[i] = adjacent

            """
            x0 = (self.corner[i]).get_x()
                y0 = (self.corner[i]).get_y()
                x1 = (self.get_corner(current)).get_x()
                y1 = (self.get_corner(current)).get_y()
            """

    def get_next(self, corner_num, dir):
        return self.corner[corner_num].get_neighbour(dir)

    def get_corner(self, corner_num):
        return self.corner[corner_num]

    def route(start, end):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dir = 0
        self.turn = 0
        self.corner = 0
        self.dist = 0
        self.d = 0
        self.speed = 0

    def update(self):
        self.d += self.speed #move
        #update x and y
        if dir == 0:
            self.x += self.speed
        elif dir == 1:
            self.y -= self.speed
        elif dir == 2:
            self.x -= self.speed
        elif dir == 3:
            self.y += self.speed

        if abs(self.turn - self.dir) == 2: #turn is opposite to dir, the player turns around
            self.d = self.dist - self.d #change d to the distance from the next node
            self.corner = map.get_next(self.corner, dir) #change corner to next corner
            self.dir = self.turn

        if self.d >= self.dist: #reached the next corner
            self.d = 0 #reset d
            self.corner = map.get_next(self.corner, dir) #change corner to next corner
            self.x = map.get_corner(self.corner).get_x() #assume the right position
            self.y = map.get_corner(self.corner).get_x()

            if map.get_next(self.corner, self.turn) == -1: #there is NO neighbour in the dir direction
                self.turn = abs(2-self.dir) #change direction to opposite
                self.speed = 0 #stop
            
            self.dir = self.turn #change dir to the next direction
            
            #update dist
            if self.dir%2 == 0: #moving horizontally
                self.dist = abs( map.get_corner(self.corner).get_x() - map.get_corner(map.get_next(self.corner, dir)).get_x())
            else:
                self.dist = abs( map.get_corner(self.corner).get_y() - map.get_corner(map.get_next(self.corner, dir)).get_y())

        self.turn = self.dir #reset turn

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dir = 0
        self.nav = []
        self.corner = 0
        self.dist = 0
        self.d = 0
        self.speed = 0
        self.flee = False

    def update():
        pass

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Energizer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game():
    def __init__(self, level):
        
        super().__init__()

        self.level = level
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()

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
while False and not done:
    g.logic()

pygame.quit()