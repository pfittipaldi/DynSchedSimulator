#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from KnockOffRand import KnockoffNpRandom


class Queue:

    def __init__(self,nd1,nd2):
        self.nodes = frozenset([nd1,nd2]) # This set will contain the extremes of the queue. A set was chosen because it is UNORDERED.
        self.type = "virtual" # Every queue is initialized as virtual.
        self.serv = "regular"
        self.Qdpairs = 0; # Queued pairs, initialized to zero.
        #self.scheduledout = 0
        self.demands = 0
        #self.rng = np.random.default_rng()
        self.rng = KnockoffNpRandom()
        
        
    def SetPhysical(self,arr_rate_s,tstep):
        self.type = "physical"
        arr_rate_steps = arr_rate_s*tstep # casting the rate per second to a rate per time step
        self.GenPParam = arr_rate_steps # Parameter for the Poisson Distribution of photon arrivals
    
    def SetVirtual(self):
        self.type = "virtual"
        
    def SetService(self,Reqrate_s,tstep):
        self.serv = "service"
        Reqrate_steps = Reqrate_s*tstep # casting the rate per second to a rate per time step
        self.PoissParam = Reqrate_steps # Parameter for the Poisson Distribution
        return self   
    
    def Demand(self): 
        B = 0;
        if self.serv == "service":
            B = self.rng.poisson(self.PoissParam)
            self.demands += B
        return B    
    
    def Loss(self,LossParam):
        rng=self.rng
        to_check = int(self.Qdpairs)
        lost = sum(rng.random(size=to_check) <= (1-LossParam))
        self.Qdpairs -= lost
        return lost

    def Generate(self):
        rng = self.rng
        if (self.type == "physical"): # Only physical queues generate, but implementing this check here allows to call...
                                      # ... the Generate method for all queues indistinctly.
            generated = rng.poisson(self.GenPParam)
            self.Qdpairs += generated
            return generated
        else:
            return 0
    
    def Consume(self):
        requested = max(self.demands,0)
        to_consume = min(requested,self.Qdpairs)
        self.Qdpairs -= to_consume
        self.demands -= to_consume
   
    def ScheduleOUT(self): 
        #self.scheduledout += 1
        self.Qdpairs -= 1
        
 
    
    
    
    
    
    