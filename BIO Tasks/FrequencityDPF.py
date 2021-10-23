"""
We will find out what is the most frequent DPF for n between 1 and 1 000 000.
As we will need to use DPF multiple times, we will modify our algorythm.
"""

#first, we find all prime numbers less than 1 000 000, using the Erathosthenes Seive
L = [l for l in range(2, 100000+1)]
primes = []
while L!=[]:
    p = L[0]
    L = [l for l in L if l%p!=0]
    primes += [p]

print("Primes done.")
print(primes[-1])
#then we can use a new DPF function
def DPF(n):
    global primes
    """
    Iterating over the primes list, we chceck for prime divisors of n. If we find one, say p, 
    we multiply prod by p and reduce n by dividing it by p as long as possible. This continues
    until n reaches 1.
    """
    prod = 1
    i = 0 #counter
    p = 0
    while p<=n:
        p = primes[i]
        if n%p == 0:
            prod *= p
            n = n//p
            while n%p==0:
                n = n//p
        i += 1
    return prod

frequency = {} #this will be a dictionary, where to every DPF, there corresponds its frequencity

n = 1
while n<=100000:
    dpf = DPF(n)
    if dpf in frequency:
        frequency[dpf] += 1
    else:
        frequency[dpf] = 1
    n += 1

print(frequency)