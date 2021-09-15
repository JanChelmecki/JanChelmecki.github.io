from random import *
A = int(input("Choose Rock (0), Paper (1) or Scissors (2): "))
B = randint(0,2)
"""
We choose B randomly. If A-B mod 3 is:
- 0 we have a draw
- 1 player wins
- 2 player loses
"""
score = (A-B)%3
"""
All the logic (disregarding the input and output parts) is done in the above line of code, 
if you do not count 3rd line which could be inserted there 
by typing: score = (A-randint(0,2))%3, if we didn't want to print B later.
"""
#the displaying part
Result = {0: "It's a draw.", 1: "You've won.", 2: "You've lost."}
ComputerChoice = {0: "Rock.", 1: "Paper.", 2: "Scissors."}
print("Computer picked", ComputerChoice[B], Result[score])