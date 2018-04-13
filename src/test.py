from mc_tools import Configuration, vis_RMSE

###############################################################################
## Test: Session 1
############################################################################### 
from session1 import volume_nunitsphere_exact, volume_nunitsphere_hitmiss

def test_session1(exp=12):
    vol2 = volume_nunitsphere_exact(n=2)
    vol3 = volume_nunitsphere_exact(n=3)
    vol10 = volume_nunitsphere_exact(n=10)
    
    config = Configuration()
    config.nb_samples = [2**i for i in range(1, exp+1)]
    
    # Reference: n=3 window=2.0
    def f_n3(s): return volume_nunitsphere_hitmiss(n=2, samples=s)
    # Reference: increasing n window=2.0
    def f_n2(s):  return volume_nunitsphere_hitmiss(n=2, samples=s)
    def f_n10(s): return volume_nunitsphere_hitmiss(n=10, samples=s)
    # Reference: n=3 increasing window
    def f_w4(s): return volume_nunitsphere_hitmiss(n=3, samples=s, window=4.0)
    def f_w8(s): return volume_nunitsphere_hitmiss(n=3, samples=s, window=8.0)
    
    vis_RMSE(f=f_n2, config=config, exact=vol2)
    vis_RMSE(f=f_n3, config=config, exact=vol3)
    vis_RMSE(f=f_n10, config=config, exact=vol10)
    vis_RMSE(f=f_w4, config=config, exact=vol3)
    vis_RMSE(f=f_w8, config=config, exact=vol3)
    
###############################################################################
## Test: Session 2
############################################################################### 
from session2 import integral_exact, integral_hitmiss, integral_uniform, integral_stratified, integral_halton

def test_session2(a, n, exp=12):
    area = integral_exact(a, n)
    
    config = Configuration()
    config.nb_samples = [2**i for i in range(1, exp+1)]
    
    def f_hm(s):  return integral_hitmiss(a=a, n=n, samples=s, plot=False)
    def f_u(s): return integral_uniform(a=a, n=n, samples=s, plot=False)
    def f_s(s): return integral_stratified(a=a, n=n, samples=s, plot=False)
    def f_h(s): return integral_halton(a=a, n=n, samples=s, plot=False)
    
    vis_RMSE(f=f_hm, config=config, exact=area)
    vis_RMSE(f=f_u, config=config, exact=area)
    vis_RMSE(f=f_s, config=config, exact=area)
    vis_RMSE(f=f_h, config=config, exact=area, biased=True)
