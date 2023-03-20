import pygame, random

#colours
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(50,50,255)
YELLOW=(255,255,0)
RED = (255, 50, 50)
GOLD = (255, 215, 0)
PURPLE = (225, 00, 225)

pygame.font.init()
myfont = pygame.font.SysFont(None, 40)
bigfont = pygame.font.SysFont(None, 200)

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

def permutations(L): #all permutations of a list
    if len(L) <= 1:
        return [L]
    else:
        output = []
        repeating = [] #aldready considered l's
        for l in L: #add all permutations ending with l
            if l not in repeating:
                output += [perm+[l] for perm in permutations(delete(L, l))]
                repeating.append(l) #mark
        return output

def delete(L, deleted): #remove a one element of a value from a list
    found = False
    i = 0
    output = []
    while i<len(L) and not found:
        if L[i] != deleted:
            output.append(L[i])
        else:
            found = True
        i+=1
    while i<len(L):
        output.append(L[i])
        i+=1
    return output

def random_grid():
    N = 8
    grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ] #this is a bit baroque but Python does not like L = k*[k*[...]] (bug in item assignments)
    unvisited = [(2*i, 2*j) for i in range(1, N) for j in range(1, N)] #mark all pegs as unvisited
    leafs = [] #the leaf queue
    roots = [] #the queue of correspondent roots
    tree_size = {}
    max_size = {} #dictionary root:maximum size of the tree

    while len(leafs)<10: #pick roots at random
        i = 2*random.randint(1,N-1)
        j = 2*random.randint(1,N-1)
        if (i,j) not in leafs:
            leafs.append( (i,j) ) #make it a leaf
            unvisited.remove((i,j)) #mark it as visited

            roots.append( (i,j) ) #make the leaf its own root
            tree_size[(i,j)] = 1
            max_size[(i,j)] = random.randint(3,5) #decide on the maximal size of the tree

    while unvisited != []:
        if len(leafs)<=1: #make new roots
            root = unvisited.pop( random.randint(0,len(unvisited)-1) )
            tree_size[root] = 1
            max_size[root] = 6 #decide on the maximal size of the tree
            (i,j) = root
        else:
            (i,j) = leafs.pop(0) #take the first leaf
            root = roots.pop(0) #its root

        for trial in range(4):
            #choose the direction of expansion
            if (i,j) == root: #root of the tree, choose any direction
                dir = random.randint(0,3)
            else:
                dir = 1 #direction of the wall
                (k,l) = next(i, j, dir)
                while grid[k][l] == 0:
                    dir = (dir+1)%4
                    (k,l) = next(i, j, dir)
                x = random.randint(0,6)
                if x == 0:
                    dir = (dir+2)%4 #straight ahead
                elif x <= 4:
                    dir = (dir+3)%4 #one side
                else:
                    dir = (dir+1)%4 #other side
                
                
            (k,l) = next(i, j, dir) #middle
            new = next(k, l, dir) #next peg

            if new in unvisited and new[0] != 0 and new[0] != 2*N and new[1] != 0 and new[1] != 2*N and tree_size[root]<max_size[root]:
                tree_size[root] += 1
                grid[k][l] = 1
                unvisited.remove(new) #visit new
                leafs.append(new) #make it a leaf
                roots.append(root) #mark what tree it's coming from
                    
    tunnel_heights = []
    while len(tunnel_heights)<random.randint(1,2): #add new element
        valid = False #whether it's away from other tunnels
        while not valid:
            h = 2*random.randint(1,N-2)+1 #pick new at random
            valid = True #assume it's valid
            for height in tunnel_heights:
                if abs(height-h)<3:
                    valid = False
        tunnel_heights.append(h)

    for h in tunnel_heights:
        grid[h][0] = 2
        grid[h][2*N] = 2
                
    return grid

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
        self.up = 60
        self.left = (size[0]-h*len(grid[0]))//2
        self.h = h
        #initialize corners
        self.corner = []
        self.tunnel_corners = []

        #find all the corners
        corner_pos = [] #mark corners 'on the grid', list where n'th item is the corner's grid coordinates
        self.node_nums = []
        for i in range(1, len(grid)-1):
            for j in range(1, len(grid[i])-1):
                if grid[i][j] == 0: #not a wall
                    vert = 0 #count vertical neighbours
                    if grid[i+1][j]!=1:
                        vert += 1
                    if grid[i-1][j]!=1:
                        vert += 1

                    hor = 0 #count horizontal neighbours
                    if grid[i][j+1]!=1:
                        hor += 1
                    if grid[i][j-1]!=1:
                        hor += 1

                    if hor*vert != 0 or hor+vert == 1: #junction/branch/turn or dead end
                        if hor + vert == 2: #not a node, just a corner
                            new = Corner(j*h+self.left, i*h+self.up) #create a new corner, with no neighbours yet
                        else:
                            new = Node(j*h+self.left, i*h+self.up)
                            self.node_nums.append(len(self.corner)) #mark the corner as a node

                        if grid[i][j+1] == 2 or grid[i][j-1] == 2:
                            self.tunnel_corners.append(len(self.corner))

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

                    elif grid[k][l] == 2: #a tunnel of the screen
                        found = corner_pos.index((i, len(grid[0])-j-1)) #corner on the same height but on other edge
                        self.corner[current].set_neighbour(dir, found) #connect current to found
                        self.corner[found].set_neighbour((dir+2)%4, current) #connect found to current
                        
        #connect the nodes
        for node in self.node_nums:
            for dir in range(4): #look in each direction
                if self.corner[node].get_neighbour(dir) != -1: #there is a neighbour
                    if self.corner[node].get_adjacent(dir) == -1: #adjacent unknown
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

        self.player_spawn = self.node_nums[0]
        self.ghost_spawn = [self.node_nums[-1], self.node_nums[-2], self.node_nums[-3]]

        self.g = {} #distance between two nodes

    def get_next(self, corner_num, dir):
        return self.corner[corner_num].get_neighbour(dir)

    def get_adjacent(self, node_num, dir):
        return self.corner[node_num].get_adjacent(dir)

    def get_dist(self, node_num, dir):
        return self.corner[node_num].get_dist(dir)

    def get_corner(self, corner_num):
        return self.corner[corner_num]

    def dir_back(self, corner_num, dir): #returns the direction to come from corner's node neighbour in dir direction back to corner
        corner_num = self.corner[corner_num].get_neighbour(dir)
        while corner_num not in self.node_nums: #not a node
            dir0 = (dir+2)%4 #direction you came from
            while self.corner[corner_num].get_neighbour(dir) == -1 or dir==dir0: #while no further neighbour
                dir = (dir+1)%4 #rotate
            corner_num = self.corner[corner_num].get_neighbour(dir) #then jump to next corner, until reaching a node
        return (dir+2)%4 #the direction you came from           

    def dist(self, corner1, corner2, dir): #works only for connected corners, dir is the direction of the connection
        if dir%2 == 0: #dir is horizontal
            if corner1 in self.tunnel_corners and self.get_next(corner1, dir) in self.tunnel_corners: # a tunnel
                return size[0]-abs(self.corner[corner1].get_x()-self.corner[corner2].get_x())+h
            else:
                return abs(self.corner[corner1].get_x()-self.corner[corner2].get_x())
        else: #dir is vertical
            return abs(self.corner[corner1].get_y()-self.corner[corner2].get_y())

    def draw(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(screen,BLUE,(j*self.h+self.left, i*self.h+self.up, self.h, self.h))
        #draw tunnels
        for i in range(len(self.grid)):
            if self.grid[i][0] == 2:
                x = self.left-h #go left until the edge
                while x>-h:
                    pygame.draw.rect(screen,BLUE,(x, i*self.h+self.up-h, self.h, self.h))#block above
                    pygame.draw.rect(screen,BLUE,(x, i*self.h+self.up+h, self.h, self.h))#block below
                    x = x-h
                x = self.left + h*len(self.grid[0]) #go right until the edge
                while x<size[0]:
                    pygame.draw.rect(screen,BLUE,(x, i*self.h+self.up-h, self.h, self.h))#block above
                    pygame.draw.rect(screen,BLUE,(x, i*self.h+self.up+h, self.h, self.h))#block below
                    x+=h

    def get_player_spawn(self):
        return self.player_spawn

    def get_ghost_spawn(self):
        return self.ghost_spawn

    def get_grid(self):
        return self.grid

    def get_up(self):
        return self.up

    def get_left(self):
        return self.left

    def heuristic(self, node1, node2):
        try:
            return self.g[node1, node2]
        except KeyError:
            return ( abs(self.corner[node1].get_x()-self.corner[node2].get_x())
            + abs(self.corner[node1].get_y()-self.corner[node2].get_y()) )

    def route(self, start, end): #finds optimal path from start to end, BOTH start and end have to be nodes
        visited = {} 
        prev_dir = {}
        prev_node = {}
        g = {} #best known distances from start
        for node in self.node_nums:
            visited[node] = False
            g[node] = -1 #-1 is used as infinity here

        g[start] = 0
        if start not in self.node_nums:
            print("Corner", start, "is not a node.")
            return [], 0
        
        while not visited[end]:
            #find the unvisited node with the shortest distance from start and save it as current
            dist_min = -1 #infinite
            for node in self.node_nums:
                if not visited[node] and g[node] != -1: #unvisited but already discovered
                    if g[node]+self.heuristic(node, end) < dist_min or dist_min == -1: #found a node that has better estimated distance
                        dist_min = g[node] + self.heuristic(node, end)
                        current = node
            visited[current] = True #mark the current node as visited

            self.g[start, current] = g[current] #improve heuristic with known distance
            self.g[current, start] = g[current]

            for dir in range(4): #look in every direction
                next = self.corner[current].get_adjacent(dir)
                if next != -1: #there is a neighbour
                    if not visited[next]:
                        new_dist = g[current] + self.corner[current].get_dist(dir) #compute distance from current
                        if g[next] == -1 or new_dist < g[next]: #undiscovered or found a shorter path
                            g[next] = new_dist #overwrite distance
                            prev_dir[next] = dir
                            prev_node[next] = current
        #trace back to start, current is currently end
        nav = []
        while current != start:
            nav.insert(0, prev_dir[current])
            current = prev_node[current] #move one node back
        return nav, g[end]

    def is_node(self, corner):
        return corner in self.node_nums

    def away_from(self, node): #node far away from the given position
        furthest = node
        max_dist = 0
        for node1 in self.node_nums:
            if self.heuristic(node, node1) > max_dist:
                max_dist = self.heuristic(node, node1)
                furthest = node1
        return furthest
    
    def escape_node(self, ghost_pos, player_pos): #finds a node such that player is far from the line joining the node and the ghost
        gp = self.heuristic(player_pos, ghost_pos)

        best_difference = 0 #find the highest |GP|+|PN|-|GN|
        for node in self.node_nums:
            if gp + self.heuristic(player_pos, node) - self.heuristic(ghost_pos, node) > best_difference:
                best_difference = gp+ self.heuristic(player_pos, node) - self.heuristic(ghost_pos, node)

        escape = ghost_pos
        max_dist = 0
        for node in self.node_nums: #find the furthest node in the right direction
            dist = self.heuristic(player_pos, node)
            if gp + dist - self.heuristic(ghost_pos, node) >= (7*best_difference)//10: #in the right direction
                if dist>max_dist:
                    max_dist = node
                    escape = node
        return escape

class Game():
    def __init__(self, level):
        self.level = level
        self.all_sprites_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.token_group = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites_group.add(self.player)

        #initialize ghosts
        for spawn in map.get_ghost_spawn():
            ghost = Ghost(spawn)
            self.all_sprites_group.add(ghost)
            self.ghost_group.add(ghost)

        #initialize dots
        self.dot_group= pygame.sprite.Group() #they are not in all_sprites_group because they do not need updating
        grid = map.get_grid()
        up = map.get_up()
        left = map.get_left()

        zeros = [] #mark zeros on the grid
        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if grid[j][i] == 0:
                    zeros.append((i*h+h//2+left, j*h+h//2+up))
        for j in range(len(grid)): #tunels towards the left edge
            if grid[j][0] == 2:
                x = left+h//2
                y = j*h+h//2+up
                while x > 0:
                    zeros.append((x,y))
                    x = x-h
        for j in range(len(grid)): #tunels towards the right edge
            if grid[j][len(grid[j])-1] == 2:
                x = (len(grid[j])-1)*h+left+h//2
                y = j*h+h//2+up
                while x < size[0]:
                    zeros.append((x,y))
                    x = x+h

        energizers = [] #choose positions of the energizers
        while len(energizers)<2:
            energizers.append(zeros[random.randint(0, len(zeros)-1)])

        for (x,y) in zeros:
            if (x,y) in energizers:
                dot = Energizer(x, y)
            else:
                dot = Dot(x, y)
            self.dot_group.add(dot)
        

        self.tracking = True #flag determining whether to compute new routes
        self.energized_due = 0 #time until which the energizer boost works
        self.start_respawning_in = 0 #time of creating the next ghost (if there are any missing)
        self.speed_boost_due = 0
        self.confuse_boost_due = 0
        self.next_token_in = 5000 #do not make any tokens until 5 seconds into the game

        #level difficulty variation
        self.energizer_duration = 4000+1000*max(4-level, 0) #7s, 6s, 5s, 4s, 4s, 4s, etc.
        self.token_waiting_time = 8000+2000*level #10s, 12s, 14s, 16s, etc.
        self.boost_duration = 6000+1000*max(3-level,0) #8s, 7s, 6s, 6s, etc.


    def controls(self):
        for event in pygame.event.get(): #stops the game, if required
            if event.type==pygame.QUIT:
                global done
                done = True
        #player controls        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.set_turn(0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.set_turn(1)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.set_turn(2)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.set_turn(3)

    def logic(self):
        global score, nextscreen, level, lives

        self.controls()

        #handle collisions with dots
        for dot in pygame.sprite.spritecollide(self.player, self.dot_group, True):
            score += 5
            if type(dot) == Energizer:
                self.energized_due = pygame.time.get_ticks()+self.energizer_duration #activate the boost
                for ghost in self.ghost_group:
                    ghost.set_nav([-1]) #make all ghosts turn around

        if len(self.dot_group) == 0: #all dots eaten
            level += 1 #next level
            nextscreen = "Game"

        #handle collisions with tokens
        for token in pygame.sprite.spritecollide(self.player, self.token_group, True):
            if type(token) == SpeedToken:
                self.player.set_default_speed(4)
                self.speed_boost_due = pygame.time.get_ticks()+7500 #activate the boost for 7.5 seconds
            elif type(token) == ConfuseToken:
                for ghost in self.ghost_group:
                    ghost.set_nav([-1]) 
                self.confuse_boost_due = pygame.time.get_ticks()+7500 #confuse ghosts for 7.5 seconds

        #handle collisions with ghosts
        if len(pygame.sprite.spritecollide(self.player, self.ghost_group, False)) != 0:
            if pygame.time.get_ticks()<=self.energized_due: #boosted
                self.start_respawning_in = pygame.time.get_ticks() + 5000 #start respawning ghosts in 5 seconds
                for ghost in pygame.sprite.spritecollide(self.player, self.ghost_group, True):
                    score += 200                
            else:
                lives += -1
                if lives <= 0:
                    nextscreen = "GameOverScreen"
                pygame.time.wait(200) #wait 0.2 seconds
                #reset sprites
                self.all_sprites_group = pygame.sprite.Group()
                self.ghost_group = pygame.sprite.Group()
                self.player = Player()
                self.all_sprites_group.add(self.player)
                for spawn in map.get_ghost_spawn():
                    ghost = Ghost(spawn)
                    self.all_sprites_group.add(ghost)
                    self.ghost_group.add(ghost)

                self.tracking = True #enable tracking
                self.speed_boost_due = 0 #cancel boosts
                self.confuse_boost_due = 0

        t = pygame.time.get_ticks() #check time effects

        if t > self.start_respawning_in: #make new ghost, if necessary
            if len(self.ghost_group) < 3:
                ghost = Ghost(map.away_from(self.player.get_corner()))
                self.all_sprites_group.add(ghost)
                self.ghost_group.add(ghost)
                if len(self.ghost_group) < 3: #note to make another
                    self.start_respawning_in += 5000
        
        if t > self.next_token_in: #try to make new tokens
            self.next_token_in = t + self.token_waiting_time  #retry later
            if random.randint(0,1) == 0: #only make tokens once every 2 trials
                
                if random.randint(0,1)==0: #in 50% of cases, make a speed token
                    token = SpeedToken(map.away_from(self.player.get_corner()))
                else: #in other cases, make a confuse token
                    token = ConfuseToken(map.away_from(self.player.get_corner()))

                self.token_group.add(token) #it is not in the all_sprites_group because it does not need updating

        if self.player.is_at_node(): #direct ghosts
            if self.tracking and t>self.confuse_boost_due: #if no routes have been computed so far and the confuse boost is uncative
                if t<=self.energized_due: #run away from the boosted player
                    self.escape_player()
                else:
                    self.navigate_ghosts() #chase the player
                self.tracking = False #disable tracking
        else:
            self.tracking = True #enable tracking

        if t>self.speed_boost_due: #set player's speed to normal, if their speed boost has expired
            self.player.set_default_speed(3)

        self.all_sprites_group.update()
        self.update_screen()

    def update_screen(self):
        screen.fill(BLACK)
        map.draw()
        self.dot_group.draw(screen)
        self.token_group.draw(screen)
        self.all_sprites_group.draw(screen)
        self.scoreboard()
        pygame.display.flip()

    def scoreboard(self):
        screen.blit(myfont.render("Level "+str(self.level), 1, YELLOW), (200, 5))
        screen.blit(myfont.render("Score: "+str(score), 1, WHITE), (430, 5))
        screen.blit(myfont.render("Lives: "+str(lives), 1, WHITE), (700, 5))
        if pygame.time.get_ticks()<=self.energized_due: #boosted
            if self.energized_due-pygame.time.get_ticks() < 1000: #less than a second left
                screen.blit(myfont.render("BOOSTED", 1, (100, 0, 0)), (835, 5)) #RED but darker
            else:
                screen.blit(myfont.render("BOOSTED", 1, RED), (835, 5))

    def estimate_dist(self, ghost_num, node): #estimate the distance from the ghost to the given node
            count = 0
            for ghost in self.ghost_group:
                if count == ghost_num:
                    dist1 = ghost.get_node_d() + map.heuristic(node, ghost.get_node()) #dist if turning around
                    dist2 = map.get_dist(ghost.get_node(), ghost.get_node_dir()) - ghost.get_node_d()
                    + map.heuristic(node, map.get_adjacent(ghost.get_node(), ghost.get_node_dir())) #dist if going straight
                    if (3*dist1)//2 < dist2:
                        dist2 = dist1
                count+=1
            return dist2 #return the smaller of dist1 and dist2

    def navigate_ghosts(self):
        global map
        player_pos = self.player.get_corner()
        ahead = map.get_adjacent(player_pos, self.player.get_dir()) #node in front of the player
        back_dir = map.dir_back(player_pos, self.player.get_dir()) #direction from ahead to player_pos

        #classify all possible destination nodes and further directions to the player
        end_dir = {} #path from a node to the player
        end_dir[player_pos] = [self.player.get_dir()]
        end_dir[ahead] = [back_dir]
        target = [] #nodes behind the node ahead
        for dir in range(4):
            if dir != back_dir:
                if map.get_adjacent(ahead, dir) != -1:
                    target.append(map.get_adjacent(ahead, dir))
                    end_dir[map.get_adjacent(ahead, dir)] = [map.dir_back(ahead, dir), back_dir] #directions from that node to the player

        dist = {} #estimate distances from each ghost to each (potential) destination node
        ghost_num = 0
        for ghost_num in range(len(self.ghost_group)):
            for node in target+[ahead, player_pos]:
                dist[ghost_num, node] = self.estimate_dist(ghost_num, node)

        if len(self.ghost_group) == 3:
            trapping_sets = [3*[player_pos], [player_pos, player_pos, ahead], [player_pos, ahead, ahead]] #basic strategies
            if len(target) == 2: #possible to spread ghosts, add more strategies
                trapping_sets.append([player_pos]+target)
                for node in target:
                    trapping_sets.append([player_pos, ahead, node])
        elif len(self.ghost_group) == 2:
            trapping_sets = [[player_pos, ahead], [player_pos, player_pos]]
        elif len(self.ghost_group) == 1:
            trapping_sets = [[player_pos]]
        else:
            trapping_sets = []


        perms = [] #all trapping assignments
        for set in trapping_sets:
            perms+=permutations(set)

        end_node = [] #choose a permutation which minimizes the time left for player to escape
        shortest_time = None #infinite
        for perm in perms:
            time_left = None #minus infinity
            for ghost_num in range(len(self.ghost_group)):
                time = dist[ghost_num, perm[ghost_num]]//2-map.heuristic(player_pos, perm[ghost_num])//3
                if time_left==None:
                    time_left = time #maximum
                elif time<time_left:
                    time_left = time #maximum

            if shortest_time == None:
                end_node = perm
                shortest_time = time_left #minimum
            elif time_left<shortest_time:
                end_node = perm
                shortest_time = time_left #minimum

        #compute the routes
        ghost_num = 0
        for ghost in self.ghost_group:
            end = end_node[ghost_num]
            start1 = ghost.get_node() #node behind
            start2 = map.get_adjacent(start1, ghost.get_node_dir()) #node ahead
            route1, dist1 = map.route(start1, end) #compute the route if turning around
            route2, dist2 = map.route(start2, end) #route if going ahead

            #account for the distances to the starting nodes
            dist1 += ghost.get_node_d()
            dist2 += map.get_dist(ghost.get_node(), ghost.get_node_dir()) - ghost.get_node_d()

            if (3*dist1)//2<dist2: #it is better to turn around (fovourizes going ahead)
                route1.insert(0, -1) #-1 tells the ghost to turn around
                nav = route1
            else:
                nav = route2

            nav = nav + end_dir[end_node[ghost_num]] #add directions from target to player

            ghost.set_nav(nav)
            ghost_num += 1

    def escape_player(self):
        for ghost in self.ghost_group:
            ghost_pos = map.get_adjacent(ghost.get_node(), ghost.get_node_dir()) #node ahead of the ghost
            route, dist = map.route( ghost_pos, map.escape_node( ghost.get_node(), self.player.get_corner() ) )
            ghost.set_nav(route)

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

        #check if beyond the screen edge (when going through a tunnel)
        if self.rect.x < -h:
            self.rect.x = size[0]
        elif self.rect.x>size[0]:
            self.rect.x = -h

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

    def get_corner(self):
        return self.corner

    def get_dir(self):
        return self.dir

    def get_d(self):
        return self.d

    def is_at_node(self):
        if self.d==0 and map.is_node(self.corner):
            return True
        else:
            return False

    def set_default_speed(self, s):
        self.default_speed = s
        if self.speed != 0: #if they are moving...
            self.speed = s #...change their speed straight away

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

        self.node = self.corner
        self.node_d = 0 #keep track of position relative to nodes
        self.node_dir = self.dir

        self.speed = 2
        self.nav = []

    def update(self):
        self.d += self.speed #move
        self.node_d += self.speed #update distance from the last node
        #update x and y
        if self.dir == 0:
            self.rect.x += self.speed
        elif self.dir == 1:
            self.rect.y -= self.speed
        elif self.dir == 2:
            self.rect.x -= self.speed
        elif self.dir == 3:
            self.rect.y += self.speed

        #check if beyond the screen edge (when going through a tunnel)
        if self.rect.x < -h:
            self.rect.x = size[0]
        elif self.rect.x>size[0]:
            self.rect.x = -h

        if self.d >= self.dist: #reached the next corner
            self.d = 0
            self.corner = map.get_next(self.corner, self.dir) #switch to the next corner
            
            #assume the corner's position
            self.rect.x = map.get_corner(self.corner).get_x()
            self.rect.y = map.get_corner(self.corner).get_y()

            #decide dir
            dir0 = (self.dir+2)%4 #the direction the ghost came from

            if map.is_node(self.corner) and self.nav != []: #at a node and given directions
                self.dir = self.nav.pop(0) #remove the first turn from the list and go there
                if map.get_next(self.corner, self.dir) == -1:
                    print("Wrong directions") #for the purposes of testing only

            else: #at a corner or no directions given
                self.dir = random.randint(0,3) #face a random direction
                count = 0 #check for directions different than the one you came from
                while (map.get_next(self.corner, self.dir) == -1 or self.dir == dir0) and count < 4:
                    self.dir = (self.dir+1)%4 #turn left
                    count += 1
                if count == 4: #checked all directions and it's only possible to go backwards (at dead end)
                    self.dir = dir0

            #once dir is decided, compute node parameters and dist
            if map.is_node(self.corner): #update position with respect to the node structures
                self.node = self.corner
                self.node_d = 0
                self.node_dir = self.dir
            self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)

    def set_nav(self, nav):
        self.nav = nav
        if len(nav) != 0:
            if nav[0] == -1: #turn around
                self.nav.pop(0)
                #update node coordinates
                if self.d == 0: #at a corner
                    if map.is_node(self.corner) and self.nav != []: #at a node and given directions
                        self.dir = self.nav.pop(0) #remove the first turn from the list and go there
                        if map.get_next(self.corner, self.dir) == -1:
                            print("Wrong directions when turning around at a node") #for the purposes of testing only
                    else: #at a corner or no directions, go anywhere
                        self.dir = (self.dir+1)%4
                        while map.get_next(self.corner, self.dir) == -1:
                            self.dir = (self.dir+1)%4
                    #once dir is decided, compute node parameters and dist
                    if map.is_node(self.corner): #update position with respect to the node structures
                        self.node = self.corner
                        self.node_d = 0
                        self.node_dir = self.dir
                    self.dist = map.dist(self.corner, map.get_next(self.corner, self.dir), self.dir)

                else:
                    self.node_d = map.get_dist(self.node, self.node_dir)-self.node_d
                    self.node = map.get_adjacent(self.node, self.node_dir)
                    self.node_dir = map.dir_back(self.corner, self.dir)
                    
                    self.d = self.dist - self.d #change d to the distance from the next corner
                    self.corner = map.get_next(self.corner, self.dir) #change corner to next corner
                    self.dir = (self.dir+2)%4

    def get_node(self):
        return self.node
    
    def get_node_dir(self):
        return self.node_dir

    def get_node_d(self):
        return self.node_d

    def get_dir(self):
        return self.dir

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([h//5,h//5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = (x, y))

class Energizer(Dot):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.Surface([(2*h)//5,(2*h)//5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = (x, y))

class SpeedToken(pygame.sprite.Sprite):
    def __init__(self, corner) -> None:
        super().__init__()
        self.image = pygame.Surface([(2*h)//3,(2*h)//3])
        self.image.fill(GOLD) 
        self.rect = self.image.get_rect(center = (map.get_corner(corner).get_x()+h//2, map.get_corner(corner).get_y()+h//2))

class ConfuseToken(pygame.sprite.Sprite):
    def __init__(self, corner) -> None:
        super().__init__()
        self.image = pygame.Surface([(2*h)//3,(2*h)//3])
        self.image.fill(PURPLE) 
        self.rect = self.image.get_rect(center = (map.get_corner(corner).get_x()+h//2, map.get_corner(corner).get_y()+h//2))

class WelcomeMenu():
    def __init__(self):
        self.options = ["START", "QUIT"]
        self.current = 0
        self.scroll = True #a flag indicating whether it is currently possible to change between options
        global level, score, lives
        level = 1 #reset game parameters
        score = 0
        lives = 3

    def logic(self):
        global done, nextscreen

        for event in pygame.event.get(): #stops the game, if required
            if event.type==pygame.QUIT:
                done = True

        #player controls        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.scroll:
                self.current = (self.current-1)%len(self.options) #change the option to the previous one
                self.scroll = False #disable scrolling until the user lets go off the key
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.scroll:
                self.current = (self.current+1)%len(self.options)
                self.scroll = False
        else: #if no keys are pressed, enable to scroll
            self.scroll = True

        if keys[pygame.K_SPACE]:
            if self.current == 0:
                nextscreen = "Game"
            else:
                done = True
        
        screen.fill(BLACK)
        
        screen.blit(bigfont.render("PAC-MAN", 1, YELLOW), (180, 10))
        for i in range(len(self.options)):
            if i == self.current:
                screen.blit(myfont.render(self.options[i], 1, WHITE), (440, 200+50*i)) #highlight the current option
            else:
                screen.blit(myfont.render(self.options[i], 1, (50, 50, 50)), (440, 200+50*i)) #make other options a bit darker
        pygame.display.flip()

class GameOverScreen():
    def __init__(self) -> None:
        self.ready_to_exit = False #a flag indicating whether the space bar has been pressed

    def logic(self):
        global done, score, level, nextscreen

        for event in pygame.event.get(): #stops the game, if required
            if event.type==pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed() 

        if keys[pygame.K_SPACE]:
            self.ready_to_exit = True

        if not keys[pygame.K_SPACE] and self.ready_to_exit: #the user has let go off the space bar
            nextscreen = "WelcomeMenu"
        
        screen.fill(BLACK)
        screen.blit(bigfont.render("GAME OVER", 1, YELLOW), (80, 200))
        screen.blit(myfont.render("You have reached level "+str(level)+" and scored "+str(score), 1, WHITE), (200, 350))


        pygame.display.flip()

#initialize PyGame
pygame.init()
size = (1000,750)
screen = pygame.display.set_mode(size)

h = 40 #tile width
score = 0
level = 1
lives = 3
nextscreen = "N" #do not change screens

#title of new window
pygame.display.set_caption("PacMan")

done=False

#Manages how fast screen refreshes
clock = pygame.time.Clock()

g = WelcomeMenu()

while not done:
    g.logic()
    clock.tick(60)
    if nextscreen != "N": #change screens
        if nextscreen == "Game":
            map = Map(random_grid(), h)
            g = Game(level)
        elif nextscreen == "WelcomeMenu":
            g = WelcomeMenu()
        elif nextscreen == "GameOverScreen":
            g = GameOverScreen()
        nextscreen = "N" #stop changing screens

pygame.quit()