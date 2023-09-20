# swap.py
# Copyright (C) 2018 flossCoder
# 
# swap.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# swap.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from simulation import generateNeighbors

def randomSwap(system, positionArray, sigmaArray, neighborArray, numberOfSwaps):
    swaps = 0
    while swaps < numberOfSwaps:
        index = np.random.randint(len(sigmaArray))
        neighbor = neighborArray[index][np.random.randint(len(neighborArray[index]))]
        auxPosition = positionArray[index]
        positionArray[index] = positionArray[neighbor]
        positionArray[neighbor] = auxPosition
        auxSigma = sigmaArray[index]
        sigmaArray[index] = sigmaArray[neighbor]
        sigmaArray[neighbor] = auxSigma
        neighborArray = generateNeighbors(positionArray)
        swaps += 1
    return([positionArray, sigmaArray, neighborArray])

def acceptSwap(temp1, temp2, fitness1, fitness2):
    if temp1 > temp2:
        d = (1.0 / temp2 - 1.0 / temp1) * (fitness2 - fitness1)
    else:
        d = (1.0 / temp1 - 1.0 / temp2) * (fitness1 - fitness2)
    return np.random.random() < np.exp(d)

def ptSwap(system, positionArray, tempArray, neighborArray, numberOfSwaps):
    swaps = 0
    while swaps < numberOfSwaps:
        index = np.random.randint(len(tempArray))
        neighbor = neighborArray[index][np.random.randint(len(neighborArray[index]))]
        if True:
            auxPosition = positionArray[index]
            positionArray[index] = positionArray[neighbor]
            positionArray[neighbor] = auxPosition
            auxTemp = tempArray[index]
            tempArray[index] = tempArray[neighbor]
            tempArray[neighbor] = auxTemp
            neighborArray = generateNeighbors(positionArray)
            swaps += 1
    return([positionArray, tempArray, neighborArray])
