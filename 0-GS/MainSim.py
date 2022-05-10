#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:29:20 2021

@author: paolo
"""


import GlobalFunctions as AllQueues
from itertools import combinations
from Q_class import Queue
import Fred as fg
import numpy as np

with open("inputs.in") as f: # Importing variables
    exec(f.read())


def Sim(BatchInput,memoDict):
    flatInput = tuple(zip(*BatchInput.items())) # List of tuples
    # memoDict = dict() # Uncomment to DISABLE memoization
    for i in memoDict.keys():
        flatMemo = i
        if flatInput[1][0] >= flatMemo[1][0] and flatInput[1][1] >= flatMemo[1][1]:
            output = memoDict[i]
            return output
    ######################################## INPUTS 
    
    
    # See inputs.in file!
    
    ######################################## READING INPUT
    
    if PhotonLifeTime == "Inf":
        LossParam = 1
    else:
        LossParam = 1 - t_step/PhotonLifeTime
    
    # Deriving the scheduling matrix and the lists of queues and scheduling rates
    # from FG's code, see fg.smalltest() for more information    
    qnet = fg.eswapnet()
    for rt in routes:
        qnet.addpath(rt)
    M, qs, ts = qnet.QC.matrix(with_sinks=True)
    
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
    
      
    
    ######################################## MAIN LOOP
    for Maintimestep in range(time_steps):
        AllQueues.Demand(Q)
        AllQueues.Loss(Q, LossParam)
        AllQueues.Generate(Q)
        AllQueues.Consume(Q)
        R = AllQueues.Schedule(Q,ConnectedTo,ts)
        AllQueues.Evolve(Q,M,R)
    D_final = [q.demands for q in Q]
    Q_final = [q.Qdpairs for q in Q]
    Tot_dem_rate = sum(BatchInput.values())
    unserved = sum(D_final)/(t_step*time_steps*Tot_dem_rate) #Unserved demands at the end divided by an approximation of the total incoming demand
    if unserved >= 0.18:
        to_store = tuple(zip(*BatchInput.items()))
        memoDict[to_store] = (unserved, Q_final, D_final) 
    return unserved, Q_final, D_final
    
