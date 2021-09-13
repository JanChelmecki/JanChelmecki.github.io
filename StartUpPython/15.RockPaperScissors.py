from random import *

RPS = {"R": "P", "P": "S", "S": "R"}

A = input("Choose Rock (R), Paper (P) or Scissors (S): ")
B = list(RPS)[randint(0,2)]

if A==RPS[B]:
    print(B, "You've won.")
elif A==B:
    print(B, "It's a draw.")
else:
    print(B, "You've lost.")