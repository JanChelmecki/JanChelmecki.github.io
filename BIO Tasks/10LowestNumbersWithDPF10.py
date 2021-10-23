"""
We will find the 10 lowest numbers whose Distinct Prime Factorization (DPF) is 10.
"""

def DPF(n):
    #From DistinctPrimeFactorization.py
    prod = 1
    L = [l for l in range(2, n+1)]

    while n>1:
        p = L[0] #the first element of L is a prime
        L = [l for l in L if l%p!=0 and l<=n] #we remove multiples of p from L
        if n%p==0:
            prod *= p
            n = n//p
            while n%p == 0:
                n = n//p
    return prod

List = []
n = 10
while len(List)<10:
    if DPF(n)==10:
        List += [n]
    n+=1

print(List)