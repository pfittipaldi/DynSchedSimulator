import numpy as np
PhotonLifeTime = 10e-6 #s, average photon lifetime inside the quantum memories. Should be always higher than time step.
                       # Set to "Inf" for lossless simulation
t_step = 1e-6; # Length of the time step, s
time_steps = int(1e4); # Number of steps to simulate per pixel
memo_len=int(time_steps/2) # How many configurations should be memoized - this refers to the memoization inside the pixels
beta = 1  # Demand weight in the scheduling calculation     

ArrRates = {
            frozenset(('A','B')) : 1000000,  # Physical pairs and their arrival rates, Hz
            frozenset(('C','B')) : 1000000,
            frozenset(('C','D')) : 1000000,
            frozenset(('E','D')) : 1000000,
            frozenset(('E','F')) : 1000000
            }

topologyname = "5 Link Chain" # Just for the plot, type whatever you want here

routes = ['ABCDE','BCDEF'] # Routes to serve the service pairs. Notice that this is separate from the SPair variables, so that several routes may be specified for a single pair.

n_points = 65 # Number of pixels for the stability plot

SPair_1 = ("A","E") #Service pairs
SPair_2 = ("B","F")
    
DemRates1 = np.linspace(1,1000000,n_points) # points along the first and second pair directions
DemRates2 = np.linspace(1,1000000,n_points)

PlotDiag= True

ParallelRun = True    # Huge performance gain if True. This should be set to False only for debugging reasons (multiprocessing does not support breakpoints)
