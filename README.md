# WARNING: DEPRECATED CODE
This code has been entirely superseded by [The Journal version](https://github.com/pfittipaldi/DynSchedSimulator_Journal), which features a major reimplementation and cleanup of the entire code.
Readers are advised to refer to the new repository, which reproduces the results of this code in full. This repo is kept for reproducibility purposes only.




# DynSchedSimulator
This repository contains the code employed to produce the results presented in ["A Linear Algebraic Framework for Quantum Internet Dynamic Scheduling"](https://arxiv.org/pdf/2205.10000.pdf).

## Description of the code
The repository is divided in three main folders: GS houses the code for the Greedy Scheduler, while MWFK and MWPK host respectively the Full Information and Partial Information Max Weight schedulers.
The directories are numbered to make manipulating the code from command line more convenient.
### Breakdown of the code
- `Q_class.py` contains the implementation of the queue object, both qubit and demand, representing a quantum link;
- `GlobalFunctions.py` defines a set of functions that affect all queues in the system;
- `MainSim.py` is the actual simulation engine
- `ParSweep.py` runs several parallel instances of 'MainSim.py' to perform the simulation and collect data.

### Exclusive to the Max Weight Schedulers
- `MWSolve_gurobi.py` is an interface to the [Gurobi](https://www.gurobi.com/) linear solver.

#### Exclusive to the Local Information Max Weight Scheduler
-`ImpossibleOrders.py` implements the rank-based conflict management system discussed in the paper.

### Additional code
- `Fred.py` collects FG's code for M matrix generation and network graph drawing;
- `KnockOffRand.py` is a simple pseudorandom generator which works by pregenerating a pool of samples and iterating through it.

### Running Simulations
The simulator is run by executing the `ParSweep.py` file in each of the folders. The simulation scenario can be customized by editing the variables inside the `Sim_input.py` file.

