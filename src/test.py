from geometry import volume_nunitsphere_exact, volume_nunitsphere_hitmiss
from mc_tools import Configuration, vis_RMSE

###################################################################################################################################################################################
## Test
################################################################################################################################################################################### 
def test(exp=12):
    vol2 = volume_nunitsphere_exact(n=2)
    vol3 = volume_nunitsphere_exact(n=3)
    vol10 = volume_nunitsphere_exact(n=10)
    vol100 = volume_nunitsphere_exact(n=100)
    
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
    
    
    vis_RMSE(f=f_w4, config=config, exact=vol3)
    vis_RMSE(f=f_w8, config=config, exact=vol3)