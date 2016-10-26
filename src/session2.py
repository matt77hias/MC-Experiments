import numpy as np

def integral_exact(a, n, low=0.0, high=np.pi):
    n = int(n)
    if n == 1:
        return (np.sin(a*high) - np.sin(a*low)) / a
    elif n == 0:
        return (high - low)
    
    def f(high, low, n):
        return (((np.cos(a*high)**(n-1)) * np.sin(a*high)) - ((np.cos(a*low)**(n-1)) * np.sin(a*low))) / (a*n)
        
    I = f(high, low, n)
    M = ((n - 1.0) / n)
    while True:
        n -= 2
        if n == 1:
            I += M * (np.sin(a*high) - np.sin(a*low)) / a
            return I
        elif n == 0:
            I += M * (high - low)
            return I
        else:
            I += M * f(high, low, n)
            M *= ((n - 1.0) / n)
 
def evaluate_integrand(x, a, n):
    return np.cos(a*x)**int(n)
    
def integral_uniform(a, n, low=0.0, high=np.pi, samples=1000, rng=np.random):
    delta = (high - low)
    I = 0.0
    for s in range(samples):
        x = low + rng.random() * delta
        I += evaluate_integrand(x=x, a=a, n=n)
    return delta * I / samples