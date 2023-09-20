# mc.py
# Copyright (C) 2018 flossCoder
# 
# mc.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# mc.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import es as evolution

def accept(temp, fitness, candFitness, ascending):
    if ascending:
        dF = fitness - candFitness
    else:
        dF = candFitness - fitness
    return np.random.random(len(dF)) <= np.exp(dF / temp)

def mcStep(args):
    x = args[0]
    f = args[1]
    sigma = args[2]
    temp = args[3]
    fitness = args[4]
    fitnessArgs = args[5]
    ascending = args[6]
    # generate candidate state
    x_ = evolution.gaussianMutation(x, sigma)
    f_ = fitness(x_, fitnessArgs)
    if accept(temp, f, f_, ascending):
        return [x_, f_]
    else:
        return [x, f]
