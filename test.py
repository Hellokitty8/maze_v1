# File:         single_DeepQ_learning.py
# Date:          
# Description:   
# Author:   jia      
# Modifications: 

# or to import the entire module. Ex:
#  from controller import *

import sys 
sys.path.append('/usr/local/lib/python2.7/site-packages')
sys.path[2]='/usr/local/lib/python2.7/site-packages'
import os
from controller import *
from numpy import *
from math import *
from search import search
from retrieval import retrieval
from stagnation import stagnation
import epuck_basic
#from keras.models import Sequential
#from keras.layers.core import Dense, Dropout, Activation
#from keras.optimizers import RMSprop
import math
import time


Search = search()
Retrieval = retrieval()
Stagnation = stagnation(Search)

MIN_FEEDBACK = 1
MAX_FEEDBACK = 8
DISTANCE_TRESHOLD = 200
IR_TRESHOLD = 3500
ACTION=["go","left","right"]
# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class _crabs (epuck_basic.EpuckBasic):

    
    def initialization(self):
        #self.emitter = self.getEmitter('emitter')
        #self.emitter.setChannel(2)
        self.gps=self.getGPS('gps')
        
        self.speeds=[0.0,0.0]
        self.maxSpeed=1000
        self.setSpeed(500,500)
    
    def getGpsValue(self):
        self.gps.enable(self.timestep)
        gps_values=self.gps.getValues()
        return gps_values
  
   
    
    def scale_data(self,data):
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train = np.array(data) 
        print X_train
        X_train_minmax = min_max_scaler.fit_transform(X_train)
        return X_train_minmax
        
    def get_reward(self,sensor,gps):
        
        
        if (sensor[0]==1):
            print ("help,I ganna killed!!")
            reward=-100
        else:
            reward=-1
        if (gps[2]<-0.7):
            print ("wow! I am out!")
            reward=100
        return reward
        
    def makeMove(self,qval):
        if qval==2:
           self.set_wheel_speeds(0.5, 0.5)
        if qval==0:
           self.turn_left()
           
           #self.set_wheel_speeds(1, 1)
           #self.do_timed_action(duration = 5)
        if qval==1:
           self.turn_right()
           
           #self.set_wheel_speeds(1, 1)
           #self.do_timed_action(duration = 5)
           
    def makeMoveDo(self,qval):
        if qval==0:
           self.set_wheel_speeds(0.5, 0.5)
           self.do_timed_action(duration = 2)
        if qval==1:
           self.turn_left()
           self.set_wheel_speeds(0.5, 0.5)
           self.do_timed_action(duration = 2)
        if qval==2:
           self.turn_right()
           self.set_wheel_speeds(0.5, 0.5)
           self.do_timed_action(duration = 2)

        
    def run(self):

        reward=10
        self.basic_setup()
        i=0
        f1 = open('/Users/jiawang/Data1.txt','w')
        status=1
        flag=0
        replay = []   
        sensor=self.get_proximities()
        while (status == 1):
            action=[]
            epochs = 5
            gamma = 0.9 #since it may take several moves to goal, making gamma high
            epsilon = 1
            batchSize = 10
            buffer = 20
            h = 0
            
            sensor=self.get_proximities()
            norm = [float(i)/max(sensor) for i in sensor]
            print ("norm",norm)
            
            action=[i for i,v in enumerate(norm[:3]) if v<0.25]
            print action 
            
            
            
            
            if action==[]:
                doAction=0
            else:
                doAction=random.choice(action)
          
            
            print ACTION[doAction]
            self.makeMoveDo(doAction)
            action=[]
            sensor_next=self.get_proximities()
            norm_next = [float(i)/max(sensor) for i in sensor_next]
            print norm_next
            gps=self.getGpsValue()   
            reward = self.get_reward(norm_next,gps)   
            replay.append((sensor, reward, doAction))
                 
            if reward == 100:
                status = 0          
                f1.write(str(replay))
            if self.step(32) == -1:
            
                
                break
    
# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.


controller = _crabs()
controller.initialization()
controller.run()
#controller.model()
