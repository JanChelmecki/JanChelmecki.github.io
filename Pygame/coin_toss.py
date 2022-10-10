import random
A = "HTH"
B = "HHT"
coin = ["H", "T"]

num_games = 10**4
score = 0 #games won by A

for game in range(num_games):
    finished = False
    Q = "" #results of tosses
    count = 0
    while not finished and count <= 20000: #toss untill a patter occurs or safety limit is reached
        toss = coin[random.randint(0,1)] 
        Q += toss
        if Q[len(Q)-len(A)::] == A: #A's patter has shown
            finished = True
            score += 1
        elif Q[len(Q)-len(B)::] == B: #B's patter has shown
            finished = True
        count += 1

print(score/num_games) #estimated probability of A winning