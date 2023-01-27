import random
R = 10**10 #resolution
n_birds = 10**3
bird = [random.randint(0,R) for i in range(n_birds)]

lines = []
for i in range(n_birds):
    closest = (i+1)%n_birds
    for j in range(n_birds):
        if j!=i:
            if abs(bird[i]-bird[j]) < abs(bird[i]-closest):
                closest = bird[j]
    if closest<bird[i]:
        lines.append((closest, bird[i]))
    else:
        lines.append((bird[i], closest))

bird.sort()
painted = 0
for i in range(len(bird)-1):
    marked = False
    for (a,b) in lines:
        if a<=bird[i] and bird[i+1]<=b:
            marked = True
    if marked:
        painted += bird[i+1]-bird[i]
    
painted = painted/R
print(painted)

