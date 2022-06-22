import pygame, random

#colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
YELLOW=(255,255,0)
RED = (255, 50, 50)

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

    def count_neighbours(self):
        return 4-self.neighbours.count(-1)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Node(Corner):
    def __init__(self, x, y, r=-1, u=-1, l=-1, d=-1):
        super().__init__(x, y, r, u, l, d)
        self.adjacent = [-1, -1, -1, -1]
        self.dist = [-1, -1, -1, -1]

    def set_adjacent(self, dir, node, dist):
        self.adjacent[dir] = node
        self.dist[dir] = dist

    def get_adjacent(self, dir):
        return self.adjacent[dir]

    def get_dist(self, dir):
        return self.dist[dir]

class Map():
    def __init__(self, grid, h):
        self.grid = grid
        self.h = h

        #initialize corners
        self.corner = []

        #find all the corners
        corner_pos = [] #mark corners 'on the grid', list where n'th item is the corner's grid coordinates
        self.node_nums = []
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
                        if hor + vert == 2: #not a node, just a corner
                            new = Corner(j*h, i*h) #create a new corner, with no neighbours yet
                        else:
                            new = Node(j*h, i*h)
                            self.node_nums.append(len(self.corner)) #mark the corner as a node
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

        #connect the nodes
        for node in self.node_nums:
            for dir in range(4): #look in each direction
                if self.corner[node].get_neighbour(dir) != -1: #there is a neighbour
                    if self.corner[node].get_adjacent(dir) == -1: #adjacent unknown
                        #print("starting at", node, "exploring in dir = ", dir)
                        dist = 0 #distance from node
                        current = node
                        dir0 = dir #direction of search (might change on turns)
                        found = False
                        while not found: #jump to the next corner in the corridor until reaching a node
                            #find the other direction different from the corner
                            dir1 = dir0
                            while self.corner[current].get_neighbour(dir1) == -1 or (dir1-dir0)%4 == 2: #no way or facing opposite dir0
                                dir1 = (dir1+1)%4 #rotate 90 deg anticlockwisely
                            dir0 = dir1
                            next_corner = self.corner[current].get_neighbour(dir0)
                            dist += self.dist(current, next_corner, dir0) #update distance
                            current = next_corner
                            if current in self.node_nums: #stop if reached a node
                                found = True

                        #make the connection
                        self.corner[node].set_adjacent(dir, current, dist)
                        self.corner[current].set_adjacent((dir0+2)%4, node, dist)    

        self.player_spawn = 0
        self.ghost_spawn = [1]

    def get_next(self, corner_num, dir):
        return self.corner[corner_num].get_neighbour(dir)

    def get_corner(self, corner_num):
        return self.corner[corner_num]

    def dist(self, corner1, corner2, dir): #works only for connected corners, dir is the direction of the connection
        if dir%2 == 0:
            return abs(self.corner[corner1].get_x()-self.corner[corner2].get_x())
        else:
            return abs(self.corner[corner1].get_y()-self.corner[corner2].get_y())

    def draw(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(screen,BLUE,(j*self.h, i*self.h, self.h, self.h))
    
    def get_player_spawn(self):
        return self.player_spawn

    def get_ghost_spawn(self):
        return self.ghost_spawn

    def get_grid(self):
        return self.grid

class Game():
    def __init__(self, level):
        self.level = level
        self.all_sprites_group = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites_group.add(self.player)
        #initialize ghosts
        for spawn in map.get_ghost_spawn():
            ghost = Ghost(spawn)
            self.all_sprites_group.add(ghost)

    def controls(self):
        for event in pygame.event.get(): #stops the game, if required
            if event.type==pygame.QUIT:
                global done
                done = True
        #player controls        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.set_turn(0)
        elif keys[pygame.K_UP]:
            self.player.set_turn(1)
        elif keys[pygame.K_LEFT]:
            self.player.set_turn(2)
        elif keys[pygame.K_DOWN]:
            self.player.set_turn(3)

    def logic(self):
        self.controls()
        self.all_sprites_group.update()
        self.update_screen()

    def update_screen(self):
        screen.fill(BLACK)
        map.draw()
        self.all_sprites_group.draw(screen)
        pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        global h
        self.corner = map.get_player_spawn()
        self.image = pygame.Surface([h,h])
        self.image.fill(YELLOW) 
        self.rect = self.image.get_rect()
        self.rect.x = map.get_corner(self.corner).get_x()
        self.rect.y = map.get_corner(self.corner).get_y()

        #turn around to face a corridor
        self.dir = 0
        while map.get_next(self.corner, self.dir) == -1: #no way
            self.dir = (self.dir+1)%4 #rotate 90deg anticlockwisely
        self.turn = 0
        self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)
        self.d = 0
        self.speed = 0
        self.default_speed = 3

    def update(self):
        self.d += self.speed #move
        #update x and y
        if self.dir == 0:
            self.rect.x += self.speed
        elif self.dir == 1:
            self.rect.y -= self.speed
        elif self.dir == 2:
            self.rect.x -= self.speed
        elif self.dir == 3:
            self.rect.y += self.speed

        if abs(self.turn - self.dir) == 2: #turn is opposite to dir, the player turns around
            self.d = self.dist - self.d #change d to the distance from the next node
            self.corner = map.get_next(self.corner, self.dir) #change corner to next corner
            self.dir = self.turn

        if self.d >= self.dist: #reached the next corner
            self.d = 0
            self.corner = map.get_next(self.corner, self.dir) #switch to the next corner

            
            #assume the corner's position
            self.rect.x = map.get_corner(self.corner).get_x()
            self.rect.y = map.get_corner(self.corner).get_y()

            if map.get_next(self.corner, self.turn) == -1: #impossible to turn in the desired direction
                if map.get_next(self.corner, self.dir) == -1: #impossible to keep moving:
                    self.dir = (self.dir+2)%4 #turn around
                    self.speed = 0 #stop
            else:    
                self.dir = self.turn
            
            self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)

        self.turn = self.dir #reset turn

    def set_turn(self, turn):
        self.turn = turn
        if self.speed == 0: #move when a key is pressed
            if map.get_next(self.corner, self.turn) != -1: #there is a neighbour
                self.speed = self.default_speed
                self.dir = self.turn
                self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, spawn):
        super().__init__()
        global h
        self.corner = spawn
        self.image = pygame.Surface([h,h])
        self.image.fill(RED) 
        self.rect = self.image.get_rect()
        self.rect.x = map.get_corner(self.corner).get_x()
        self.rect.y = map.get_corner(self.corner).get_y()

        #turn around to face a corridor
        self.dir = 0
        while map.get_next(self.corner, self.dir) == -1: #no way
            self.dir = (self.dir+1)%4 #rotate 90deg anticlockwisely
        self.turn = 0
        self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)
        self.d = 0

        self.speed = 2
        self.nav = []

    def update(self):
        self.d += self.speed #move
        #update x and y
        if self.dir == 0:
            self.rect.x += self.speed
        elif self.dir == 1:
            self.rect.y -= self.speed
        elif self.dir == 2:
            self.rect.x -= self.speed
        elif self.dir == 3:
            self.rect.y += self.speed

        if self.d >= self.dist: #reached the next corner
            self.d = 0
            self.corner = map.get_next(self.corner, self.dir) #switch to the next corner
            
            #assume the corner's position
            self.rect.x = map.get_corner(self.corner).get_x()
            self.rect.y = map.get_corner(self.corner).get_y()
            
            
            dir0 = (self.dir+2)%4 #the direction the ghost came from

            if type(map.get_corner(self.corner)) == Node: #at a node

                if self.nav == []: #no directions given
                    self.dir = random.randint(0,3) #face a random direction
                else:
                    self.dir = self.nav.pop() #remove the first turn from the list and go there

            #if not at a node or impossible to turn, check for directions different than the one you came from
            count = 0
            while (map.get_next(self.corner, self.dir) == -1 or self.dir == dir0) and count < 4:
                self.dir = (self.dir+1)%4 #turn left
                count += 1

            if count == 4: #checked all directions and it's only possible to go backwards (at dead end)
                self.dir = dir0
            
            self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.Surface([h, h])
        self.image.fill(WHITE)
        
        # Draw the player
        pygame.draw.circle(self.image, WHITE, (h//2, h//2), 5)

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