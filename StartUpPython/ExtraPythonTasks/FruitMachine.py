from random import *
Symbols = ["Cherry", "Bell", "Lemon", "Orange", "Star", "Skull"]
credit = 1
Roll = [False, False, False]

play = True #indicates whether player wants to (and affords to) play one more round
while play:
    credit -= 0.2
    for i in range(3):
        Roll[i] = Symbols[randint(0,5)]
    print()
    for r in Roll:
        print(r)
    print()
    play = False

