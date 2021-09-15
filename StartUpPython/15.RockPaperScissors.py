from random import *

RPS = {"R": "P", "P": "S", "S": "R"}

A = input("Choose Rock (R), Paper (P) or Scissors (S): ")
B = list(RPS)[randint(0,2)]

display = {"R": "Rock.", "P": "Paper.", "S": "Scissors."} #this is just for displaying the score, it plays no role in the logic part

if A==RPS[B]:
    print("Computer picked", display[B], "You've won.")
elif A==B:
    print("Computer also picked", display[B], "It's a draw.")
else:
    print("Computer picked", display[B], "You've lost.")