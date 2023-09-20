# fitnessPlots.py
# Copyright (C) 2018 flossCoder
# 
# fitnessPlots.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# fitnessPlots.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import matplotlib as mpl

plt.rcParams['text.latex.preamble'] = [ # change latex praeambel
    r'\usepackage{amsmath}',
    r'\usepackage{amsfonts}',
    r'\usepackage{amssymb}',
    r'\usepackage{amsthm}',
    r'\usepackage{upgreek}',
    r'\usepackage{siunitx}', # for units
    r'\sisetup{detect-all}' # force siunitx to actually use your fonts
]

#plt.rc('text', usetex=True)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

#plt.rc('text', usetex=True)
plt.rcParams['font.size'] = (15)
#plt.rcParams['font.family'] = ('sans-serif')
#plt.rcParams['mathtext.fontset'] = ('dejavusans')
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 10

# plot the sphere function

X = np.arange(-8, 8.1, 0.5)
Y = np.arange(-8, 8.1, 0.5)
X, Y = np.meshgrid(X, Y)
Z = X**2 + Y**2

fig = plt.figure()
fig.set_size_inches(4.5, 4, forward=True)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$f(x, y)$")
#ax.set_title(r"\noindent Sphere\\ $f(\vec{x}) = \sum\limits_{i = 1}^n x_i^2$")
ax.set_title("Sphere\n"+r"$f(\vec{x}) = \sum_{i = 1}^n x_i^2$")
plt.tight_layout()
plt.savefig("sphere.svg")
#plt.show()

# plot the rosenbrock function

X = np.arange(-2, 2.1, 0.1)
Y = np.arange(-0.5, 3.1, 0.1)
X, Y = np.meshgrid(X, Y)
Z = (1.0 - X)**2 + 100.0 * (Y - X**2)**2

fig = plt.figure()
fig.set_size_inches(4.5, 4, forward=True)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$f(x, y)$")
#ax.set_title(r"\noindent Rosenbrock\\ $f(x, y) = (a-x)^2 + b(y-x^2)^2$")
ax.set_title("Rosenbrock\n"+r"$f(x, y) = (a-x)^2 + b(y-x^2)^2$")
plt.tight_layout()
plt.savefig("rosenbrock.svg")
#plt.show()

# plot the rastrigin function

X = np.arange(-5, 5.1, 0.05)
Y = np.arange(-5, 5.1, 0.05)
X, Y = np.meshgrid(X, Y)
Z = 10.0 * 2.0 + X**2 - 10.0 * np.cos(2.0 * np.pi * X) + Y**2 - 10.0 * np.cos(2.0 * np.pi * Y)

fig = plt.figure()
fig.set_size_inches(4.5, 4, forward=True)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$f(x, y)$")
#ax.set_title(r"\noindent Rastrigin\\ $f(\vec{x}) = A n + \sum\limits_{i=1}^n \left(x_i^2 - A \cos(2 \pi x_i)\right)$")
ax.set_title("Rastrigin\n"+r"$f(\vec{x}) = A n + \sum_{i=1}^n \left(x_i^2 - A \cos(2 \pi x_i)\right)$")
plt.tight_layout()
plt.savefig("rastrigin.svg")
#plt.show()

# plot the schwefel function

X = np.arange(-500, 500, 1)
Y = np.arange(-500, 500, 1)
X, Y = np.meshgrid(X, Y)
Z = 418.9829 * 2.0 - X * np.sin(np.sqrt(np.abs(X))) - Y * np.sin(np.sqrt(np.abs(Y)))

fig = plt.figure()
fig.set_size_inches(4.5, 4, forward=True)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$f(x, y)$")
#ax.set_title(r"\noindent Schwefel\\ $f(\vec{x}) = 418.9828d - \sum\limits_{i=1}^d x_i \sin\left(\sqrt{\left| x_i \right|}\right)$")
ax.set_title("Schwefel\n"+r"$f(\vec{x}) = 418.9828d - \sum_{i=1}^d x_i \sin\left(\sqrt{\left| x_i \right|}\right)$")
plt.tight_layout()
plt.savefig("schwefel.svg")
#plt.show()
