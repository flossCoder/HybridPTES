# es.py
# Copyright (C) 2018 flossCoder
# 
# es.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# es.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from mc import accept

def initializeES(xWidth, muSolutions, fitness, fitnessArgs):
    x = None
    if xWidth == 1:
        x = np.random.random([muSolutions]) * 10
    else:
        x = np.random.random([muSolutions, xWidth]) * 10
    f = fitness(x, fitnessArgs)
    return([x, f])

def initializeSystem(numberOfReplicas, xWidth, muSolutions, fitness, fitnessArgs):
    system = []
    aux = initializeES(xWidth, muSolutions, fitness, fitnessArgs)
    for i in xrange(numberOfReplicas):
        system.append([np.copy(i) for i in aux])
    return(system)

def crossover(x, lambdaSolutions):
    return((x[[int(np.round(np.random.random() * (len(x) - 1))) for i in xrange(lambdaSolutions)]] + x[[int(np.round(np.random.random() * (len(x) - 1))) for i in xrange(lambdaSolutions)]]) / 2.0)

def crossover_(x):
    indexArray = np.arange(len(x))
    np.random.shuffle(indexArray)
    return((x + x[indexArray]) / 2.0)

def gaussianMutation(x, sigma):
    if len(x.shape) == 1:
        return(x + sigma * np.random.standard_normal([len(x)]))
    else:
        return(x + sigma * np.random.standard_normal([len(x), len(x[0])]))

def selection(x, f, muSolutions, ascending = True):
    if ascending:
        index = np.argsort(f)
    else:
        index = np.argsort(f)[::-1]
    return([x[index][0:muSolutions], f[index][0:muSolutions]])

def simulationStep(args):
    x = args[0]
    f = args[1]
    muSolutions = args[2]
    lambdaSolutions = args[3]
    sigma = args[4]
    fitness = args[5]
    fitnessArgs = args[6]
    ascending = args[7]
    x_ = crossover(x, lambdaSolutions)
    x_ = gaussianMutation(x_, sigma)
    f_ = fitness(x_, fitnessArgs)
    xInter = np.concatenate((x, x_), axis = 0)
    fInter = np.concatenate((f, f_), axis = 0)
    return(selection(xInter, fInter, muSolutions, ascending))

def restart(args):
    x = args[0]
    muSolutions = args[1]
    lambdaSolutions = args[2]
    sigma = args[3]
    fitness = args[4]
    fitnessArgs = args[5]
    ascending = args[6]
    x_ = crossover(x, lambdaSolutions)
    x_ = gaussianMutation(x_, sigma)
    f_ = fitness(x_, fitnessArgs)
    [x__, f__] = selection(x_, -1 * f_, muSolutions, ascending)
    return([x__, -1*f__])

def simulateEpsilon(args):
    epsilon = args[0]
    x = args[1]
    f = args[2]
    muSolutions = args[3]
    lambdaSolutions = args[4]
    sigma = args[5]
    fitness = args[6]
    fitnessArgs = args[7]
    ascending = args[8]
    xHistory = [x]
    fHistory = [f]
    deviation = [np.inf for i in xrange(muSolutions)]
    while all([i >= epsilon for i in deviation]):
        [x, f] = simulationStep([x, f, muSolutions, lambdaSolutions, sigma, fitness, fitnessArgs, ascending])
        deviation = np.abs(fHistory[len(fHistory) - 1] - f)
        xHistory.append(x)
        fHistory.append(f)
    return([x, f, xHistory, fHistory])
