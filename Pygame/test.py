import numpy
x = 0.0
v = 1.0
t = 0.0
h = 10**(-3)

n = 0
while t<10:
    x1 = x + v*h
    v1 = v + (numpy.sin(x)+2*numpy.cos(x)+2*v-2*x)*h
    
    x = x1
    v = v1
    t += h

    n+=1
    if n%1000 == 0:
        print(t, x)