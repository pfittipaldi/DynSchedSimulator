#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 11:13:27 2021

@author: paolo

This class contains functions that interface to all queues in the system, both of pairs and of demands.
"""
import random as rd
import numpy as np

               
def Demand(Q):
    for i in range(len(Q)):
        Q[i].Demand();

def Loss(Q,LossParam):
    for q in Q:
        q.Loss(LossParam)

def Generate(Q):
    for queue in Q:
        queue.Generate();
                
def Consume(Q):
    for queue in Q:
        if (queue.serv == "service"):
            queue.Consume();
            
def Schedule(Q,connectedto,transitions):
    transitions = np.array(transitions)
    R = np.zeros(len(transitions)) # Output scheduling decision
    nodes = connectedto.keys()
    nodes = rd.sample(nodes,k=len(nodes))
    for ActiveNode in nodes:
        Q_Ready = [q for q in connectedto[ActiveNode] if q.Qdpairs> 0]
        while len(Q_Ready) >= 2:
            parent1, parent2 = rd.sample(Q_Ready,2)
            childnode1 = next(i for i in parent1.nodes if i != ActiveNode); 
            childnode2 = next(i for i in parent2.nodes if i != ActiveNode); 
            
            tr1 = childnode1 + "[" + ActiveNode + "]" + childnode2
            tr2 = childnode2 + "[" + ActiveNode + "]" + childnode1
            Rindex_toincrease = np.where((transitions == tr1) + (transitions == tr2))
            R[Rindex_toincrease]+=1
            
            parent1.ScheduleOUT() # This removes the scheduled pairs from the queues' pair counters
            parent2.ScheduleOUT()
            
            Q_Ready = [q for q in connectedto[ActiveNode] if q.Qdpairs> 0]
    return R
 
def Evolve(Q,M,R):
    Q_t = np.array([q.Qdpairs for q in Q])
    Q_t1 = Q_t + M@R
    for i in range(len(Q)):
        Q[i].Qdpairs = Q_t1[i]
    
    