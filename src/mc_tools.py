import matplotlib.pyplot as plt
import numpy as np

###################################################################################################################################################################################
## Configuration
################################################################################################################################################################################### 
class Configuration(object):
    
    def __init__(self, nb_merges=128, nb_experiments=1024, nb_samples=[2**i for i in range(1, 16)]):
        # Number of merges for bootstrapping
        self.nb_merges = nb_merges
        # Number of runs to obtain one estimator _beta_ of the MSE/RMSE of one estimator _alpha_
        self.nb_experiments = nb_experiments
        # Number of samples to obtain one estimator _alpha_
        self.nb_samples = nb_samples
        
###################################################################################################################################################################################
## Calculation
###################################################################################################################################################################################  
from global_configuration import nb_cpus
from multiprocessing.pool import ThreadPool as Pool

def calculate_values(f, config=Configuration()):
    return np.array([f(s) for s in config.nb_samples])

def calculate_experiments(f, config=Configuration()):
    pool = Pool(nb_cpus())
    experiments = np.array(pool.map(lambda x: calculate_values(f=f, config=config) , range(config.nb_experiments)))
    pool.close()
    pool.join() 
    return experiments
    
def calculate_RMSE(data, biased=False, exact=None):
    if biased:
        if exact is not None:
            return np.sqrt(np.mean((data - exact)**2, axis=0))
        else:
            return np.sqrt(np.mean((data - np.mean(data, axis=0))**2, axis=0, ddof=1))
    else:
        return np.std(data, axis=0, ddof=1)
    
###################################################################################################################################################################################
## Bootstrap sampling
################################################################################################################################################################################### 
def bootstrapping(data, config=Configuration(), biased=False, exact=None):
    log_nb_samples = np.log2(config.nb_samples)
    RMSEs = np.zeros((config.nb_merges, len(config.nb_samples)))
    coefficients = np.zeros((config.nb_merges, 2))
    for m in range(config.nb_merges):
        # Merging
        size = config.nb_experiments
        mdata = np.zeros((size, len(config.nb_samples)))
        for j in range(size):
            for s in range(len(config.nb_samples)):
                re = np.random.randint(low=0, high=config.nb_experiments)
                mdata[j, s] = data[re, s]
        RMSEs[m,:] = calculate_RMSE(data=mdata, biased=biased, exact=exact)
        log_RMSE = np.log2(RMSEs[m,:])
        # Fitting     
        # uniform weights due to loglog scale 
        coefficients[m,:] = np.polyfit(log_nb_samples, log_RMSE, 1)
    
    # RMSE of RMSEs and coefficients 
    return np.std(RMSEs, axis=0, ddof=1), np.std(coefficients, axis=0, ddof=1)
 
###################################################################################################################################################################################
## Visualization
###################################################################################################################################################################################
def vis_RMSE(f, config=Configuration(), biased=False, exact=None, plot=True, save=True):
    # nb_experiments x len(nb_samples)
    data = calculate_experiments(f=f, config=config)
    # Select 1 RMSE
    RMSE = calculate_RMSE(data=data, biased=biased, exact=exact)
    # Bootstrapping coefficients
    RMSE_RMSE, coefficient_RMSE = bootstrapping(data=data, config=config, biased=biased, exact=exact)
    print('slope RMSE:\t' + str(coefficient_RMSE[0]))
    print('intercept RMSE:\t' + str(coefficient_RMSE[1]))
    # Visualization
    _vis_RMSE(name=f.__name__, xs=config.nb_samples, ys=RMSE, yerr=RMSE_RMSE, exact=exact, plot=plot, save=save)

def _vis_RMSE(name, xs, ys, yerr, exact=None, plot=True, save=True, ref_offset=1.5):
    plt.figure()
    
    if exact is not None and exact != 0:
        ys /= abs(exact)
        yerr /= abs(exact)
    
    # RMSE errorbar
    plt.errorbar(xs, ys, yerr=yerr, ls='None', marker='o', color='g', label=name)
    # 1 degree polynomial fit
    log_xs = np.log2(xs)
    log_ys = np.log2(ys)
    fitted_coefficients = np.polyfit(log_xs, log_ys, 1)
    fitted_polygon = np.poly1d(fitted_coefficients)
    fitted_ys = [2**fitted_polygon(s) for s in log_xs]
    plt.plot(xs, fitted_ys, ls='-', color='g', label='fit')
    # 1 degree polynomial reference
    ref_coefficients = [-0.5, ref_offset * fitted_coefficients[1]]
    ref_polygon = np.poly1d(ref_coefficients)
    ref_ys = [2**ref_polygon(s) for s in log_xs]
    plt.plot(xs, ref_ys, ls='-', color='b', label='ref')
    
    plt.title('Root Mean Square Errors [slope={0:0.4f}]'.format(fitted_coefficients[0]))
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('# samples')
    plt.ylabel('RMSE')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    if save:
        plt.savefig('RMSE_' + name + '.png', bbox_inches='tight')
    if not plot:
        plt.close()