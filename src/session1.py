import numpy as np

###############################################################################
## Point Inside n-Sphere
############################################################################### 
def point_in_nunitsphere(p, n):
    return np.all(np.dot(p, p) <= 1.0)
      
###############################################################################
## Volume
###############################################################################     
def volume_nunitsphere_hitmiss(n, window=None, samples=1000, rng=np.random):
    n = abs(int(n))
    if n == 0:
        return 1.0
    
    if window is None:
        window = 2.0
    p_in = 0
    for s in range(samples):
        p = (rng.random((n)) - 0.5) * window
        p_in += int(point_in_nunitsphere(p, n))
    return float(p_in) / samples * (window**n)
    
def volume_nunitsphere_exact(n):
    n = abs(int(n))
    if n == 0:
        return 1.0
    if n == 1:
        return 2.0
    elif n == 2:
        return np.pi
    else:
        return (2.0 * np.pi / n) * volume_nunitsphere_exact(n=n-2)
