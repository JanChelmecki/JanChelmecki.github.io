n = int(input("Input a positive integer: "))
print("Divisors:")
for k in range(1,n+1):
    if n%k==0:
        print(k)

## AC Very good