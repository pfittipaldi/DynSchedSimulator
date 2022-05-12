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
    B = np.zeros(len(Q))
    for i in range(len(B)):
        B[i] = Q[i].Demand();
    return B

def Loss(Q,LossParam):
    L = np.zeros(len(Q))
    for i in range(len(L)):
        L[i] = Q[i].Loss(LossParam)
    return L

def Generate(Q):
    A = np.zeros(len(Q))
    for i in range(len(A)):
        A[i] = Q[i].Generate();
    return A
                
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
        Q_Ready = {q.nodes:q for q in connectedto[ActiveNode] if q.Qdpairs> 0}
        TransitionPool = [tr for tr in transitions if frozenset((tr[0],tr[2])) in Q_Ready.keys() and frozenset((tr[4],tr[2])) in Q_Ready.keys()] # This behemoth of a list comprehension is horrible.
        
        #AllowedTransitions = set((tr for tr in transitions if tr[2] == ActiveNode)) # These transitions are ALLOWED: the routing permits them.
        
        #PossibleTransitions = GeneratePossibleTransitions(Q_Ready) # These transitions are POSSIBLE: there are pairs to perform them, but they are not necessarily included in the routing.
        
        #FinalTransitions = AllowedTransitions.intersect(PossibleTransitions) # We need transitions that are both ALLOWED and POSSIBLE.
        
        while len(TransitionPool) >= 1:
            ActiveTransition = rd.sample(TransitionPool, 1)[0]
            
            childnode1 = ActiveTransition[0]
            childnode2 = ActiveTransition[4] 
            Rindex_toincrease = np.where(transitions == ActiveTransition)
            R[Rindex_toincrease]+=1
            
            
            parent1_Nodes = frozenset((ActiveTransition[0],ActiveTransition[2]))
            parent2_Nodes = frozenset((ActiveTransition[4],ActiveTransition[2]))

            parent1 = Q_Ready[parent1_Nodes]
            parent2 = Q_Ready[parent2_Nodes]

            parent1.ScheduleOUT() # This removes the scheduled pairs from the queues' pair counters
            parent2.ScheduleOUT()
            
            Q_Ready = {q.nodes:q for q in connectedto[ActiveNode] if q.Qdpairs> 0}
            TransitionPool = [tr for tr in transitions if frozenset((tr[0],tr[2])) in Q_Ready.keys() and frozenset((tr[4],tr[2])) in Q_Ready.keys()] # This behemoth of a list comprehension is horrible.
    return R

def Evolve(Q,M,R):
    Q_t = np.array([q.Qdpairs + q.scheduledout for q in Q]) # I have to consider both "free" stored pairs and "scheduled out" stored pairs
    Q_t1 = Q_t + M@R
    for i in range(len(Q)):
        Q[i].Qdpairs = Q_t1[i]
    
    