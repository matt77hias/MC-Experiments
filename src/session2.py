import numpy as np
from plotter import Plotter2D 

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
 
def integral_hitmiss(a, n, low=0.0, high=np.pi, samples=1000, rng=np.random, plot=True, plot_chain=False, plotter=None):
    if plot and plotter is None:
        plotter = Plotter2D()
    if plot and not plot_chain:
        plotter.plot_AABB([low, -1.0], [high, 1.0], color='k')
        plotter.plot_line([low, 0.0], [high, 0.0], color='k')
        plot_integrand(a=a, n=n, low=low, high=high, plotter=plotter)
    
    delta = (high - low)
    I = 0.0
    for s in range(samples):
        x = low + rng.random() * delta
        y = -1.0 + rng.random() * 2.0
        fx = evaluate_integrand(x=x, a=a, n=n)
        if fx < y and y <= 0.0:
            I -= 1
            color = 'lightgreen'
        elif fx > y and y >= 0.0:
            I += 1
            color = 'darkgreen'
        else:
            color = 'red'
        if plot:
            plotter.plot_point([x, y], color=color)
        
    return 2.0 * delta * I / samples
 
def evaluate_integrand(x, a, n):
    return np.cos(a*x)**int(n)
     
def integral_uniform(a, n, low=0.0, high=np.pi, samples=1000, rng=np.random, plot=True, plot_chain=False, plotter=None):
    if plot and plotter is None:
        plotter = Plotter2D()
    if plot and not plot_chain:
        plotter.plot_AABB([low, -1.0], [high, 1.0], color='k')
        plotter.plot_line([low, 0.0], [high, 0.0], color='k')
        plot_integrand(a=a, n=n, low=low, high=high, plotter=plotter)
    
    delta = (high - low)
    I = 0.0
    for s in range(samples):
        x = low + rng.random() * delta
        fx = evaluate_integrand(x=x, a=a, n=n)
        I += fx
        if plot:
            if fx < 0.0:
                plotter.plot_line([x, 0.0], [x, fx], color='lightgreen')
            else:
                plotter.plot_line([x, 0.0], [x, fx], color='darkgreen')
    return delta * I / samples
    
def integral_stratified(a, n, low=0.0, high=np.pi, samples=10000, strata=None, rng=np.random, plot=True, plot_chain=False, plotter=None):
    if plot and plotter is None:
        plotter = Plotter2D()
    if plot and not plot_chain:
        plotter.plot_AABB([low, -1.0], [high, 1.0], color='k')
        plotter.plot_line([low, 0.0], [high, 0.0], color='k')
        plot_integrand(a=a, n=n, low=low, high=high, plotter=plotter)
    
    if strata is None:
        strata = samples
    samples_per_strata = samples / strata
    
    delta = (high - low) / float(strata)
    I = 0.0
    for i in range(strata):
        I += integral_uniform(a=a, n=n, low=low+i*delta, high=low+(i+1)*delta, samples=samples_per_strata, rng=rng, plot=plot, plot_chain=True, plotter=plotter)
    return I
    
def plot_integrand(a, n, low=0.0, high=np.pi, samples=10000, plotter=None):
    if plotter is None:
        plotter = Plotter2D()
    xs = np.linspace(start=low, stop=high, num=samples)
    ys = evaluate_integrand(x=xs, a=a, n=n)
    plotter.ax.plot(xs, ys, color='b')