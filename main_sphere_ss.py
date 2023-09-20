# main_sphere_ss.py
# Copyright (C) 2018 flossCoder
# 
# main_sphere_ss.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# main_sphere_ss.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from simulation import getBestValue, doSimpleSampling
from fitness import sphere
import os

expName = "sphere_ss"
xWidth = 2
numberOfSamples = 100000
multFactor = 5.12
bias = 0.0
fitness = sphere
fitnessArgs = None

os.makedirs(expName)

[resultX, resultF] = doSimpleSampling(expName, xWidth, numberOfSamples, multFactor, bias, fitness, fitnessArgs, False, True)

x = np.array(resultX)
np.savetxt('%s/f.csv'%expName, np.transpose(np.array([[i for i in xrange(len(resultF))], x[:,0], x[:,1], resultF])), delimiter=',')

best = getBestValue(expName, resultX, resultF)

np.savetxt('%s/f_results.csv'%(expName), best)
