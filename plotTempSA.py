# plotTempSA.py
# Copyright (C) 2018 flossCoder
# 
# plotTempSA.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# plotTempSA.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

#plt.rc('text', usetex=True)
plt.rcParams['font.size'] = (15)
#plt.rcParams['font.family'] = ('sans-serif')
#plt.rcParams['mathtext.fontset'] = ('dejavusans')
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 10

startTemp = 5.0
endTemp = 0.2
maxSteps = 1000
tempMult = (endTemp/startTemp)**(1.0/(maxSteps - 1.0))
temp = startTemp

temps = []
for step in np.arange(1, maxSteps + 1):
    temps.append(temp)
    temp *= tempMult

#plt.style.use('dark_background')

fig = plt.figure()
fig.set_size_inches(7.0, 4.0, forward=True)
plt.plot(temps)
ax = fig.add_subplot(111)
ax.set_xlabel(r"step")
ax.set_ylabel(r"$\Theta$")
ax.set_title(r"Temperature annealing scheme")
fig.tight_layout()
