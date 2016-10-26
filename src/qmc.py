import numpy as np

def radical_inverse(index, base):
    result = 0.0
    f = 1.0
    i = index
    while (i > 0): 
        f /= base
        result += f * (i % base)
        # if base == 2, this corresponds to >> (right shift)
        i = np.floor(i / float(base))
    return result
    
def vanderCorput(index):
    return radical_inverse(index=index, base=2)
    
# The first 168 prime numbers (all the prime numbers less than 1000) 
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, \
          103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, \
          211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, \
          331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, \
          449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, \
          587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, \
          709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, \
          853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    
def halton(index, s=1):
    return np.array([radical_inverse(index=index, base=primes[i]) for i in range(0, s)])
    
def hammersley(index, N, s=1):
    if (index >= N):
        raise ValueError('index={0} should be smaller than N={1}'.format(index, N))
    return np.array([index / float(N)] + [radical_inverse(index=index, base=primes[i]) for i in range(0, s-1)])
    
def roth(index, N):
    return hammersley(index=index, N=N, s=2)