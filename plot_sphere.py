# plot_sphere.py
# Copyright (C) 2018 flossCoder
# 
# plot_sphere.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# plot_sphere.py is distributed in the hope that it will be useful, but
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
plt.rcParams['font.size'] = (10)
#plt.rcParams['font.family'] = ('sans-serif')
#plt.rcParams['mathtext.fontset'] = ('dejavusans')
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 10

pt = np.loadtxt("sphere_pt/f_0.csv", delimiter=",")
sa = np.loadtxt("sphere_sa/f_0.csv", delimiter=",")
es = np.loadtxt("sphere_es/f_3.csv", delimiter=",")
gmrc = np.loadtxt("sphere_gmrc/f_1.csv", delimiter=",")
gm = np.loadtxt("sphere_gm/f_0.csv", delimiter=",")
ws = np.loadtxt("sphere_ws/f_1.csv", delimiter=",")

if True:
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(9, 9))
    
    axes[0, 0].set_title("Parallel Tempering")
    axes[0, 0].semilogy(pt[:10000,0], pt[:10000,3], "o")
    axes[0, 0].set_xlabel(r"$step$")
    axes[0, 0].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[0, 1].set_title("Simulated Annealing")
    axes[0, 1].semilogy(sa[:,0], sa[:,3], "o")
    axes[0, 1].set_xlabel(r"$step$")
    axes[0, 1].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[1, 0].set_title("GMRC-ES")
    axes[1, 0].semilogy(gmrc[:1500,0], gmrc[:1500,3], "o")
    axes[1, 0].set_xlabel(r"$step$")
    axes[1, 0].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[1, 1].set_title("ES")
    axes[1, 1].semilogy(es[:100,0], es[:100,3], "o")
    axes[1, 1].set_xlabel(r"$step$")
    axes[1, 1].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[2, 0].set_title("Parallel Tempered restarts")
    axes[2, 0].semilogy(gm[:100,0], gm[:100,3], "o")
    axes[2, 0].set_xlabel(r"$step$")
    axes[2, 0].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[2, 1].set_title("Parallel Tempered mutation")
    axes[2, 1].semilogy(ws[:,0], ws[:,3], "o")
    axes[2, 1].set_xlabel(r"$step$")
    axes[2, 1].set_ylabel(r"$f(\vec{x}_{step})$")
    
    fig.tight_layout()
else:
    plt.style.use('dark_background')
    
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 7))
    
    axes[0, 0].set_title("Parallel Tempering")
    axes[0, 0].semilogy(pt[:10000,0], pt[:10000,3], "o")
    axes[0, 0].set_xlabel(r"$step$")
    axes[0, 0].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[1, 0].set_title("Simulated Annealing")
    axes[1, 0].semilogy(sa[:,0], sa[:,3], "o")
    axes[1, 0].set_xlabel(r"$step$")
    axes[1, 0].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[0, 1].set_title("ES")
    axes[0, 1].semilogy(es[:100,0], es[:100,3], "o")
    axes[0, 1].set_xlabel(r"$step$")
    axes[0, 1].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[1, 1].set_title("GMRC-ES")
    axes[1, 1].semilogy(gmrc[:1500,0], gmrc[:1500,3], "o")
    axes[1, 1].set_xlabel(r"$step$")
    axes[1, 1].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[0, 2].set_title("Parallel Tempered mutation")
    axes[0, 2].semilogy(ws[:,0], ws[:,3], "o")
    axes[0, 2].set_xlabel(r"$step$")
    axes[0, 2].set_ylabel(r"$f(\vec{x}_{step})$")
    
    axes[1, 2].set_title("Parallel Tempered restarts")
    axes[1, 2].semilogy(gm[:100,0], gm[:100,3], "o")
    axes[1, 2].set_xlabel(r"$step$")
    axes[1, 2].set_ylabel(r"$f(\vec{x}_{step})$")
    
    fig.tight_layout()
