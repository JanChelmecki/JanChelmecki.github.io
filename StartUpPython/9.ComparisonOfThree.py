x = int(input("Input an integer: "))
y = int(input("Input an integer: "))
z = int(input("Input an integer: "))

def maximum(L):
    m=L[0]
    for i in range(1,len(L)):
        if L[i]>m:
            m=L[i]
    return m

print("Maximum is", maximum([x,y,z]))

## Very good