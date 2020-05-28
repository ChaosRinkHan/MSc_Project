import os
import tempfile

import pyabc

from pyABC_study.ODE import ODESolver, PriorLimits
from pyABC_study.dataPlot import sim_data_plot, result_plot, result_data

# Get path

ROOT_DIR = os.path.abspath(os.curdir)
db_path = ("sqlite:///" +
           os.path.join(tempfile.gettempdir(), "test.db"))


# Generate synthetic data

# True parameters

paraInit = {'iBM': 8.475862809697531,
            'kMB': 3.7662920313110075,
            'kNB': 2.2961320437266535,
            'lambdaM': 8.509867878209329,
            'lambdaN': 1.5114114729225983,
            'muA': 5.903807936902964,
            'muB': 0.38726153092588084,
            'muM': 3.697974670181216,
            'muN': 2.6821274451686814,
            'sAM': 3.62381585701928,
            'sBN': 3.7176297747866545,
            'vNM': 0.4248874922862373}

# Using default time points
solver = ODESolver()
expData = solver.ode_model(paraInit)
print("Target data")
print(expData)

dict(((j,i), sol[i][j]) for i in range(len(sol)) for j in range(len(sol[0])) if i<j)
# Plot

sim_data_plot(solver.timePoint, expData)


# Define prior distribution of parameters
# Be careful that RV("uniform", -10, 15) means uniform distribution in [-10, 5], '15' here is the interval length

lim = PriorLimits(0, 10)

paraPrior = pyabc.Distribution(
    lambdaN=pyabc.RV("uniform", lim.lb, lim.interval_length),
    kNB=pyabc.RV("uniform", lim.lb, lim.interval_length),
    muN=pyabc.RV("uniform", lim.lb, lim.interval_length),
    vNM=pyabc.RV("uniform", lim.lb, lim.interval_length),
    lambdaM=pyabc.RV("uniform", lim.lb, lim.interval_length),
    kMB=pyabc.RV("uniform", lim.lb, lim.interval_length),
    muM=pyabc.RV("uniform", lim.lb, lim.interval_length),
    sBN=pyabc.RV("uniform", lim.lb, lim.interval_length),
    iBM=pyabc.RV("uniform", lim.lb, lim.interval_length),
    muB=pyabc.RV("uniform", lim.lb, lim.interval_length),
    sAM=pyabc.RV("uniform", lim.lb, lim.interval_length),
    muA=pyabc.RV("uniform", lim.lb, lim.interval_length)
)

# Define ABC-SMC model

#distance_adaptive = pyabc.AdaptivePNormDistance(p=2)
distanceP2 = pyabc.PNormDistance(p=2)



abc = pyabc.ABCSMC(models=solver.ode_model,
                   parameter_priors=paraPrior,
                   population_size=300,
                   #distance_function=distance_adaptive,
                   distance_function=distanceP2,
                   eps=pyabc.MedianEpsilon(100, median_multiplier=1)
                   )
abc.new(db_path, expData)

max_population = 15
history = abc.run(minimum_epsilon=0.1, max_nr_populations=max_population)

result_plot(history, max_population)
result_data(history, expData, max_population)

