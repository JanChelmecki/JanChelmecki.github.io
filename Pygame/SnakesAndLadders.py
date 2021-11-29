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
        self.snakes = {}
        for i in range(1, 10):
            start = 10*i+random.randint(1,9)
            end = 10*random.randint(0, i-1) + random.randint(1,9)
            self.snakes[start] = end

        self.ladders = {}
        for i in range(9):
            start = 10*i+random.randint(1,9)
            end = 10*random.randint(i, 9) + random.randint(1,9)
            self.ladders[start] = end

    def move_player(self, pos): #move the player according to snakes-ladders pattern
        if pos in self.snakes:
            pos = self.snakes[pos]
            print("They're on a snake. They move to", pos)
        if pos in self.ladders:
            pos = self.ladders[pos]
            print("They're on a ladder. They move to", pos)
        return pos

g = Game(2)
g.logic()