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

    def show(self, corner_num):
        print(corner_num, self.neighbours)

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

    def display(self, n): #just for testing, to be removed from the final code
        print(n, self.adjacent, self.dist)

class Map():
    def __init__(self, grid):
        self.grid = grid

        #initialize corners
        self.corner = []

        #find all the corners and nodes
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
                        if hor + vert == 2: #not a node
                            new = Corner(j, i) #create a new corner, with no neighbours yet
                        else:
                            new = Node(j, i)
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

    def get_next(self, corner_num, dir):
        return self.corner[corner_num].get_neighbour(dir)

    def dist(self, corner1, corner2, dir): #works only for connected corners, dir is the direction of the connection
        if dir%2 == 0:
            return abs(self.corner[corner1].get_x()-self.corner[corner2].get_x())
        else:
            return abs(self.corner[corner1].get_y()-self.corner[corner2].get_y())

    def show(self):
        print("Node number, adjacent, dist")
        for n in self.node_nums:
            self.corner[n].display(n)

    def h(self, corner1, corner2):
        return ( abs(self.corner[corner1].get_x()-self.corner[corner2].get_x())
        + abs(self.corner[corner1].get_y()-self.corner[corner2].get_y()) )

    def route(self, start, end):

        current = start
        visited = [False for n in self.node_nums]
        g = [-1 for n in self.node_nums]
        from_dir = [0 for n in self.node_nums]
        while True:
            for dir in range(4):
                if self.corner[current].get_adjacent(dir) != -1:
                    pass



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

map = Map(grid1)

i = 1
for grid in [grid1, grid2, grid3]:
    print(); print("grid",i)
    map = Map(grid)
    map.show()
    i+=1