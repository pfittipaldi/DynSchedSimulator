#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:29:20 2021

@author: paolo
"""


import GlobalFunctions as AllQueues
from Q_class import Queue
import Fred as fg
import numpy as np
from Sim_inputs import *



def Sim(BatchInput,memoDict):
    flatInput = tuple(zip(*BatchInput.items())) # List of tuples
    # memoDict = dict() # Uncomment to DISABLE memoization
    for i in memoDict.keys(): # If a lower load was unstable, skip computation.
        flatMemo = i
        if flatInput[1][0] >= flatMemo[1][0] and flatInput[1][1] >= flatMemo[1][1]:
            output = memoDict[i]
            return output
    
    ######################################## READING INPUT
    
    if PhotonLifeTime == "Inf":
        LossParam = 1
    else:
        LossParam = np.exp(-t_step/PhotonLifeTime)
    
    # Deriving the scheduling matrix and the lists of queues and scheduling rates
    # from FG's code, see fg.smalltest() for more information    
    qnet = fg.eswapnet()
    for rt in routes:
        qnet.addpath(rt)
    M, qs, ts = qnet.QC.matrix()
    
    ### Building the model 
    
    
    nodeset = set()
    for tq in qs:
        nodeset = nodeset.union(set(tq))# Set of the nodes. May not be necessary now but will be useful going forward
    
    Q = [Queue(tq[0],tq[1]) for tq in qs]
   
    [q.SetPhysical(ArrRates[q.nodes],t_step) for q in Q if q.nodes in ArrRates]
    [q.SetService(BatchInput[q.nodes],t_step) for q in Q if q.nodes in BatchInput]
    
    
    # This next block builds a dictionary of neighbors for each queue, so that AC - BD is never checked as a potential entanglement swapping operation
    ConnectedTo = {}
    for label in nodeset:
        ConnectedTo[label] = [q for q in Q if (label in q.nodes)]
    
      
    watch = np.zeros(time_steps)
    ######################################## MAIN LOOP
    for Maintimestep in range(time_steps):
        Dt = [q.demands for q in Q]
        Qt = [q.Qdpairs for q in Q]
        AllQueues.Consume(Q)
        B = AllQueues.Demand(Q)
        L = AllQueues.Loss(Q, LossParam)
        A = AllQueues.Generate(Q) # B,L and A here are only for debugging purposes, since the queues' counters are implicitly updated.
        R = AllQueues.Schedule(Q,ConnectedTo,ts)
        watch[Maintimestep] = (M@R)[0]
        AllQueues.Evolve(Q,M,R)    
        # if sum(R) != 0 and Maintimestep >= 1000:
        #     breakpoint()
    D_final = [q.demands for q in Q]
    Q_final = [q.Qdpairs for q in Q]
    Tot_dem_rate = sum(BatchInput.values())
    unserved = sum(D_final)/(t_step*time_steps*Tot_dem_rate) #Unserved demands at the end divided by an approximation of the total incoming demand
    
    
    if unserved >= 0.18:
        to_store = tuple(zip(*BatchInput.items()))
        memoDict[to_store] = (unserved, Q_final, D_final) 
    return unserved, Q_final, D_final
    
