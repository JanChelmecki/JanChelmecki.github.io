import pygame

def next(i,j, dir):
    """
    Returns the grid coordinates of the next tile in the dir direction
    """
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
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def is_node(self):
        return self.neighbours.count(-1) != 2

class Map():
    def __init__(self, grid, h):
        self.grid = grid
        self.h = h

        #initialize corners
        self.corner = []

        #find all the corners
        corner_pos = [] #mark corners 'on the grid', list where n'th item is the corner's grid coordinates
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
                        new = Corner(j*self.h, i*self.h) #create a new corner, with no neighbours yet
                        self.corner.append(new)
                        corner_pos.append((i,j)) #mark its position 'on the grid'
        
        #connect the corners
        for current in range(len(self.corner)):
            for dir in range(4): #check in all four directions
                if self.corner[current].get_neighbour(dir) == -1: #no known neighbour in the dir direction
                    (i, j) = corner_pos[current]
                    (k, l) = next(i, j, dir)
                    if grid[k][l] == 0: #there is a neighbour in the dir direction
                        while not (k,l) in corner_pos: #explore in the dir direction until reaching a corner
                            (k,l) = next(k, l, dir)
                        found = corner_pos.index((k,l))
                        self.corner[current].set_neighbour(dir, found) #connect current to found
                        self.corner[found].set_neighbour((dir+2)%4, current) #connect found to current

    def get_next(self, corner_num, dir):
        return self.corner[corner_num].get_neighbour(dir)

    def get_corner(self, corner_num):
        return self.corner[corner_num]

    def draw(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(screen,BLUE,(j*self.h, i*self.h, self.h, self.h))

class Game():
    def __init__(self, level):
        self.level = level
        self.all_sprites_group = pygame.sprite.Group()
        self.player = Player(0)
        self.all_sprites_group.add(self.player)

    def controls(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                global done
                done = True

    def logic(self):
        self.controls()
        self.update_screen()

    def update_screen(self):
        screen.fill(BLACK)
        map.draw()
        self.all_sprites_group.draw(screen)
        pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self, corner):
        super().__init__()
        global h
        self.image = pygame.Surface([h,h]) 
        self.image.fill(YELLOW) 
        self.rect = self.image.get_rect()
        self.rect.x = map.get_corner(corner).get_x()
        self.rect.y = map.get_corner(corner).get_y()
        self.dir = 0
        self.turn = 0
        self.corner = corner
        self.dist = 0
        self.d = 0
        self.speed = 2

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

#colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
YELLOW=(255,255,0)

#Initialize PyGame
pygame.init()
size = (640,480)
screen = pygame.display.set_mode(size)

#load map
grid1 = [
[1, 1, 1, 1, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1]
]
grid2 = [
[1, 1, 1, 1, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 0, 1],
[1, 0, 1, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1],
]
grid3 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 1, 1, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1],
]

h = 40
map = Map(grid3, h)

#--Titleofnewwindow/screen
pygame.display.set_caption("PacMan")

done=False

#Manages how fast screen refreshes
clock = pygame.time.Clock()

g = Game(0)

while not done:
    g.logic()
    clock.tick(60)

pygame.quit()