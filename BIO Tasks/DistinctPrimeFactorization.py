n = int(input("n = "))
"""
For a given integer n, program outpust the product of its distinct prime factors.
For example: n = 12 = 2*2*3 gives 6 = 2*3. It works analogously to Factorization.py 
The only  differences are:
1. instead of the factorization list, we store the prod integer as our output
2. if we find that n is divisible by p, we multiply prod by p ONCE and then keep reducing n
"""
prod = 1 #output
L = [l for l in range(2, n+1)]

while n>1:
    p = L[0] #the first element of L is a prime
    L = [l for l in L if l%p!=0 and l<=n] #we remove multiples of p from L
    if n%p==0:
        prod *= p
        n = n//p
        while n%p == 0:
            n = n//p

print(prod)