import time, timeit

def fib(n): #recursive
	if n <= 1:
	    return n
	else:
		return fib(n-1) + fib(n-2) 
		#terribly inefficient, exponential time complexity

def fibonacci2(n): #iterative
    fibNumbers = [0,1]  #list of first two Fibonacci numbers
	# now append the sum of the two previous numbers to the list    
    for i in range(2,n+1):
        fibNumbers.append(fibNumbers[i-1] + fibNumbers[i-2])
    return fibNumbers[n] 

def fibonacci(n): #my implementation
    a = 1
    b = 1
    index = 2
    while index<n:
        temp = b
        b = a + b
        a = temp
        index += 1
    return b


n = 10

time1 = timeit.timeit(setup = "from __main__ import fib", stmt = "fib(30)", number = 10)
time2 = timeit.timeit(setup = "from __main__ import fibonacci2", stmt = "fibonacci2(30)", number = 10)
time3 = timeit.timeit(setup = "from __main__ import fibonacci", stmt = "fibonacci(30)", number = 10)

print(time1)
print(time2)
print(time3)

print("t1/t3 = ", time1/time3) #how much faster the third one is