# simulation.py
# Copyright (C) 2018 flossCoder
# 
# simulation.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# simulation.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from multiprocessing import Pool
import cPickle as pickle
import gzip
from es import initializeSystem, initializeES, simulationStep, simulateEpsilon, restart
from mc import mcStep

generateNeighbors = lambda positionArray : [[positionArray[i + 1]] if i == 0 else [positionArray[i - 1]] if (i + 1) == len(positionArray) else [positionArray[i - 1], positionArray[i + 1]] for i in xrange(len(positionArray))]

def getBestValue(expName, resultX, resultF):
    index = resultF.index(min(resultF))
    return np.concatenate(([index], [resultX[index][0]], [resultX[index][1]], [resultF[index]]))

def saveCurrentState(expName, step, **kwargs):
    with gzip.GzipFile('%s/%s.pgz'%(str(expName), str(step)), 'w') as f:
        pickle.dump(kwargs, f)

def doSimulationWithSwaps(expName, xWidth, muSolutions, lambdaSolutions, sigmaArray, swapSteps, measureSteps, maxSteps, numberOfSwaps, numberOfProcesses, fitness, fitnessArgs, swapFunction, save = True, ascending = True):
    numberOfReplicas = len(sigmaArray)
    # initialize the system
    system = initializeSystem(numberOfReplicas, xWidth, muSolutions, fitness, fitnessArgs)
    positionArray = [i for i in xrange(numberOfReplicas)]
    neighborArray = generateNeighbors(positionArray)
    resultX = []
    resultF = []
    if save:
        saveCurrentState(expName, 0, system = system, positionArray = positionArray, sigmaArray = sigmaArray, neighborArray = neighborArray)
    for step in np.arange(1, maxSteps + 1):
        # set up args for parallel processing
        args = []
        for sysIndex in xrange(numberOfReplicas):
            args.append([system[sysIndex][0],
                         system[sysIndex][1],
                         muSolutions,
                         lambdaSolutions,
                         sigmaArray[sysIndex],
                         fitness,
                         fitnessArgs,
                         ascending])
        # simulate systems in parallel
        p = Pool(numberOfProcesses)
        simResult = p.map(simulationStep, args)
        p.close()
        # postprocess results
        system = [[aux[0], aux[1]] for aux in simResult]
        minIndex = sigmaArray.index(min(sigmaArray))
        if (step % measureSteps) == 0:
            resultX.append(system[minIndex][0][0])
            resultF.append(system[minIndex][1][0])
        if save:
            saveCurrentState(expName, step, system = system, positionArray = positionArray, sigmaArray = sigmaArray, neighborArray = neighborArray)
        # do swapping
        if step % swapSteps == 0:
            [positionArray, sigmaArray, neighborArray] = swapFunction(system, positionArray, sigmaArray, neighborArray, numberOfSwaps)
    return [resultX, resultF]

def doSimulationGlobalMutation(expName, xWidth, muSolutions, lambdaSolutions, sigma, globalSigmaArray, epsilon, epsilon_, swapSteps, measureSteps, maxSteps, numberOfSwaps, numberOfProcesses, fitness, fitnessArgs, swapFunction, save = True, ascending = True):
    numberOfReplicas = len(globalSigmaArray)
    # initialize the system
    system = initializeSystem(numberOfReplicas, xWidth, muSolutions, fitness, fitnessArgs)
    positionArray = [i for i in xrange(numberOfReplicas)]
    neighborArray = generateNeighbors(positionArray)
    resultX = []
    resultF = []
    minHistory = [[] for x in xrange(numberOfReplicas)]
    if save:
        saveCurrentState(expName, 0, system = system, minHistory = minHistory, globalSigmaArray = globalSigmaArray)
    for step in np.arange(1, maxSteps + 1):
        # set up args for parallel processing
        args = []
        for sysIndex in xrange(numberOfReplicas):
            args.append([epsilon,
                         system[sysIndex][0],
                         system[sysIndex][1],
                         muSolutions,
                         lambdaSolutions,
                         sigma,
                         fitness,
                         fitnessArgs,
                         ascending])
        # simulate systems in parallel
        p = Pool(numberOfProcesses)
        simResult = p.map(simulateEpsilon, args)
        p.close()
        # postprocess results
        system = [[aux[0], aux[1]] for aux in simResult]
        auxX = []
        auxF = []
        # check for each replic, if it reached a certain minimum (which we allready found)
        for sysIndex in xrange(numberOfReplicas):
            # obtain the minimum of the current population
            minIndex = np.where(system[sysIndex][1] == min(system[sysIndex][1]))[0][0]
            # save the minimum
            minHistory[sysIndex].append(system[sysIndex][0][minIndex])
            auxX.append(system[sysIndex][0][minIndex])
            auxF.append(system[sysIndex][1][minIndex])
            if foundRecentMinimum(system[sysIndex][0][minIndex], minHistory[sysIndex], epsilon_):
                # simulate the system with a large mutation rate
                args = [system[sysIndex][0], muSolutions, lambdaSolutions, globalSigmaArray[sysIndex], fitness, fitnessArgs, ascending]
                a = restart(args)
                system[sysIndex][0] = a[0]
                system[sysIndex][1] = a[1]
        if (step % measureSteps) == 0:
            index = auxF.index(min(auxF))
            resultX.append(auxX[index])
            resultF.append(auxF[index])
        if save:
            saveCurrentState(expName, step, system = system, minHistory = minHistory, globalSigmaArray = globalSigmaArray)
    if step % swapSteps == 0:
            [positionArray, globalSigmaArray, neighborArray] = swapFunction(system, positionArray, globalSigmaArray, neighborArray, numberOfSwaps)
    return [resultX, resultF]

def foundRecentMinimum(minimum, minHistory, epsilon_):
    for x in minHistory:
        if any([True if ((minimum[index] >= x[index] - epsilon_) and (minimum[index] <= x[index])) or ((minimum[index] >= x[index]) and (minimum[index] <= x[index] + epsilon_)) else False for index in xrange(len(minimum))]):
            return True
    return False

def doSimulationGlobalMutationRateControl(expName, xWidth, muSolutions, lambdaSolutions, numberOfReplicas, sigma, tau, epsilon, epsilon_, measureSteps, maxSteps, numberOfProcesses, fitness, fitnessArgs, save = True, ascending = True):
    # initialize the system
    system = initializeSystem(numberOfReplicas, xWidth, muSolutions, fitness, fitnessArgs)
    resultX = []
    resultF = []
    minHistory = [[] for x in xrange(numberOfReplicas)]
    bigSigmaArray = [sigma * 10 for x in xrange(numberOfReplicas)]
    if save:
        saveCurrentState(expName, 0, system = system, minHistory = minHistory, bigSigmaArray = bigSigmaArray)
    for step in np.arange(1, maxSteps + 1):
        # set up args for parallel processing
        args = []
        for sysIndex in xrange(numberOfReplicas):
            args.append([epsilon,
                         system[sysIndex][0],
                         system[sysIndex][1],
                         muSolutions,
                         lambdaSolutions,
                         sigma,
                         fitness,
                         fitnessArgs,
                         ascending])
        # simulate systems in parallel
        p = Pool(numberOfProcesses)
        simResult = p.map(simulateEpsilon, args)
        p.close()
        # postprocess results
        system = [[aux[0], aux[1]] for aux in simResult]
        auxX = []
        auxF = []
        minX = None
        minF = np.inf
        # check for each replic, if it reached a certain minimum (which we allready found)
        for sysIndex in xrange(numberOfReplicas):
            # obtain the minimum of the current population
            minIndex = np.where(system[sysIndex][1] == min(system[sysIndex][1]))[0][0]
            # save the minimum
            minHistory[sysIndex].append(system[sysIndex][0][minIndex])
            auxX.append(system[sysIndex][0][minIndex])
            auxF.append(system[sysIndex][1][minIndex])
            if (step % measureSteps) == 0 and minF > system[sysIndex][1][minIndex]:
            	minX = system[sysIndex][0][minIndex]
            	minF = system[sysIndex][1][minIndex]
            if (step % 50) == 0 and foundRecentMinimum(system[sysIndex][0][minIndex], minHistory[sysIndex], epsilon_):
                # simulate the system with a large mutation rate
                args = [system[sysIndex][0], muSolutions, lambdaSolutions, bigSigmaArray[sysIndex], fitness, fitnessArgs, ascending]
                a = restart(args)
                system[sysIndex][0] = a[0]
                system[sysIndex][1] = a[1]
                bigSigmaArray[sysIndex] = bigSigmaArray[sysIndex] * tau
            else:
                bigSigmaArray[sysIndex] = bigSigmaArray[sysIndex] / tau
        if (step % measureSteps) == 0:
            index = auxF.index(min(auxF))
            resultX.append(minX)
            resultF.append(minF)
        if save:
            saveCurrentState(expName, step, system = system, minHistory = minHistory, bigSigmaArray = bigSigmaArray)
    return [resultX, resultF, bigSigmaArray, minHistory]

def doSimulationES(expName, xWidth, muSolutions, lambdaSolutions, sigma, measureSteps, maxSteps, fitness, fitnessArgs, save = True, ascending = True):
    # initialize the system
    system = initializeSystem(1, xWidth, muSolutions, fitness, fitnessArgs)
    resultX = []
    resultF = []
    minHistory = []
    if save:
        saveCurrentState(expName, 0, system = system, minHistory = minHistory)
    for step in np.arange(1, maxSteps + 1):
        # set up args for parallel processing
        args = [system[0][0],
                system[0][1],
                muSolutions,
                lambdaSolutions,
                sigma,
                fitness,
                fitnessArgs,
                ascending]
        # simulate systems in parallel
        simResult = simulationStep(args)
        # postprocess results
        system = [simResult]
        if (step % measureSteps) == 0:
            index = np.where(min(simResult[1]))[0][0]
            resultX.append(simResult[0][index])
            resultF.append(simResult[1][index])
        if save:
            saveCurrentState(expName, step, system = system, minHistory = minHistory)
    return [resultX, resultF, minHistory]


def doParallelTempering(expName, xWidth, sigma, tempArray, swapSteps, measureSteps, maxSteps, numberOfSwaps, numberOfProcesses, fitness, fitnessArgs, swapFunction, save = True, ascending = True):
    numberOfReplicas = len(tempArray)
    # initialize the system
    system = initializeSystem(numberOfReplicas, xWidth, 1, fitness, fitnessArgs)
    positionArray = [i for i in xrange(numberOfReplicas)]
    neighborArray = generateNeighbors(positionArray)
    resultX = []
    resultF = []
    if save:
        saveCurrentState(expName, 0, system = system, positionArray = positionArray, tempArray = tempArray, neighborArray = neighborArray)
    for step in np.arange(1, maxSteps + 1):
        # set up args for parallel processing
        args = []
        for sysIndex in xrange(numberOfReplicas):
            args.append([system[sysIndex][0],
                         system[sysIndex][1],
                         sigma,
                         tempArray[sysIndex],
                         fitness,
                         fitnessArgs,
                         ascending])
        # simulate systems in parallel
        p = Pool(numberOfProcesses)
        simResult = p.map(mcStep, args)
        p.close()
        # postprocess results
        system = [[aux[0], aux[1]] for aux in simResult]
        minIndex = tempArray.index(min(tempArray))
        if (step % measureSteps) == 0:
            resultX.append(system[minIndex][0][0])
            resultF.append(system[minIndex][1][0])
        if save:
            saveCurrentState(expName, step, system = system, positionArray = positionArray, tempArray = tempArray, neighborArray = neighborArray)
        # do swapping
        if step % swapSteps == 0:
            [positionArray, tempArray, neighborArray] = swapFunction(system, positionArray, tempArray, neighborArray, numberOfSwaps)
    return [resultX, resultF]

def doSimulatedAnnealing(expName, xWidth, sigma, startTemp, endTemp, equiSteps, maxSteps, fitness, fitnessArgs, save = True, ascending = True):
    resultX = []
    resultF = []
    [x, f] = initializeES(xWidth, 1, fitness, fitnessArgs)
    temp = startTemp
    tempMult = (endTemp/startTemp)**(1.0/(maxSteps-1.0))
    if save:
        saveCurrentState(expName, 0, x = x, f = f, temp = temp)
    for step in np.arange(1, maxSteps + 1):
        # equilibration
        for i in xrange(equiSteps):
            args = [x, f, sigma, temp, fitness, fitnessArgs, ascending]
            [x, f] = mcStep(args)
        resultX.append(x[0])
        resultF.append(f[0])
        if save:
            saveCurrentState(expName, step, x = x, f = f, temp = temp)
        temp *= tempMult
    return [resultX, resultF]

def doSimpleSampling(expName, xWidth, numberOfSamples, multFactor, bias, fitness, fitnessArgs, save = True, ascending = True):
    x = None
    if xWidth == 1:
        x = np.random.random([numberOfSamples]) * multFactor + np.ones([numberOfSamples]) * bias
    else:
        x = np.random.random([numberOfSamples, xWidth]) * multFactor + np.ones([numberOfSamples, xWidth]) * bias
    f = fitness(x, fitnessArgs)
    if save:
        saveCurrentState(expName, 0, x = x, f = f)
    return [x, np.ndarray.tolist(f)]
