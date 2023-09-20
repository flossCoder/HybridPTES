# main_sphere_gm.py
# Copyright (C) 2018 flossCoder
# 
# main_sphere_gm.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# main_sphere_gm.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from swap import ptSwap
from simulation import getBestValue, doSimulationGlobalMutation
from fitness import sphere
import os

expName = "sphere_gm"
xWidth = 2
muSolutions = 10
lambdaSolutions = 100
swapSteps = 30
measureSteps = 1
maxSteps = 1000
numberOfSwaps = 1
numberOfProcesses = 4
fitness = sphere
fitnessArgs = None
swapFunction = ptSwap

sigma = 0.05
globalSigmaArray = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
epsilon = 0.0000000001
epsilon_ = 0.0000000001

os.makedirs(expName)
rows = 20
bestValues = np.zeros((rows, 5))

for j in xrange(rows):
    [resultX, resultF] = doSimulationGlobalMutation(expName, xWidth, muSolutions, lambdaSolutions, sigma, globalSigmaArray, epsilon, epsilon_, swapSteps, measureSteps, maxSteps, numberOfSwaps, numberOfProcesses, fitness, fitnessArgs, swapFunction, False)
    
    x = np.array(resultX)
    np.savetxt('%s/f_%i.csv'%(expName, j), np.transpose(np.array([[i for i in xrange(len(resultF))], x[:,0], x[:,1], resultF])), delimiter=',')
    
    bestValues[j,0] = j
    bestValues[j,1:5] = getBestValue(expName, resultX, resultF)

np.savetxt('%s/f_results.csv'%(expName), bestValues)
np.savetxt('%s/results.csv'%(expName), np.array([np.mean(bestValues[:,4]), np.sqrt(np.var(bestValues[:,4]) / (rows - 1))]))
