# fitness.py
# Copyright (C) 2018 flossCoder
# 
# fitness.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# fitness.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np

def sphere(x, args = None):
    if len(np.shape(x)) == 1:
        return x**2
    else:
        return np.sum(x**2, axis = 1)

def rosenbrock(x, args = [1.0, 100.0]):
    if len(np.shape(x)) == 1:
        raise Exception("invalid x dimension")
    if np.shape(x)[1] != 2:
        raise Exception("invalid x dimension")
    if len(args) != 2:
        raise Exception("invalid number of arguments")
    return (args[0] - x[:,0])**2 + args[1] * (x[:,1] - x[:,0]**2)**2

def rastrigin(x, args = [10.0]):
    return args[0] * np.shape(x)[1] + np.sum(x**2 - args[0] * np.cos(2.0 * np.pi * x), axis = 1)

def schwefel(x, args = [418.9829]):
    return (args[0] * np.shape(x)[1] - np.sum(x * np.sin(np.sqrt(np.abs(x))), axis = 1))

def ackley(x, args = None):
    if len(np.shape(x)) == 1:
        raise Exception("invalid x dimension")
    if np.shape(x)[1] != 2:
        raise Exception("invalid x dimension")
    return(-20 * np.exp(-0.2 * np.sqrt(0.5 * (x[:,0]**2 + x[:,1]**2))) - np.exp(0.5 * (np.cos(2.0 * np.pi * x[:,0]) + np.cos(2.0 * np.pi * x[:,1]))) + np.exp(1.0) + 20)
