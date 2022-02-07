import random

class Game():
    def __init__(self, num_players) -> None:
        self.players = [Player() for i in range(num_players)]
        self.board = Board()

    def logic(self):
        done = False
        round = 1
        while not done and round<100:
            print(); print("Round", round); round+=1
            i = 0
            while i<len(self.players) and not done:
                print(); print("Player", i+1, "turn. They're at", self.players[i].get_pos())
                self.players[i].roll()
                print("Player", i+1, "moves to", self.players[i].get_pos())
                self.players[i].set_pos(self.board.move_player(self.players[i].get_pos()))
                if self.players[i].get_pos() == 100:
                    done = True
                    print("Player", i+1, "won.")
                i += 1
        if round >= 100: #just for safety
            print("Maximal number of rounds exceeded.")
class Player():
    def __init__(self) -> None:
        self.pos = 0
    
    def roll(self): #roll the dice and move the player
        roll = random.randint(1,6); print("The dice rolled", roll)
        self.pos += roll
        if self.pos > 100: #bounce back
            self.pos = 200 - self.pos

    def set_pos(self, x):
        self.pos = x

    def get_pos(self):
        return self.pos

class Board():
    def __init__(self) -> None:
        self.snakes = {} #dictionary, start:end
        self.ladders = {}
        """
        We do not want neither starts to overlap nor a start to be an end.
        """
        #create lists of potential starts - in this implementation, some of the values may not become parts of snakes/ladders
        snakes_start = []
        ladders_start = []
        for i in range(9): #fill snakes_start randomly
            snakes_start.append(random.randint(11,99))
        for i in range(9): #fill ladders_start randomly, making sure the starts do not overlap with the snakes_start
            tile = random.randint(1,89)
            if tile not in snakes_start:
                ladders_start.append(tile)
        """
        Even is some value start is reapeted in snakes_snakes start, it is not a problem 
        - the snakes[start] value will be overwritten.
        """
        
        #find ends which ARE NOT in either of the start list
        for start in snakes_start:
            end = random.randint(1, start-start%10) #random tile on a lower level
            while (end in snakes_start or end in ladders_start) and end > 0:
                end -= 1 #go backwards
            if end>0: #if you did find an end, make an start:end pair
                self.snakes[start] = end
        
        for start in ladders_start:
            end = random.randint(start-start%10+11, 99) #random tile on a higher level
            while (end in snakes_start or end in ladders_start) and end < 100:
                end += 1 #go foreward
            if end<100: 
                self.ladders[start] = end
        
    def move_player(self, pos): #move the player according to snakes-ladders pattern
        if pos in self.snakes:
            pos = self.snakes[pos]
            print("They're on a snake. They move to", pos)
        elif pos in self.ladders:
            pos = self.ladders[pos]
            print("They're on a ladder. They move to", pos)
        return pos

g = Game(2)
g.logic()