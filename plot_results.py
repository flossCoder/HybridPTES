# plot_results.py
# Copyright (C) 2018 flossCoder
# 
# plot_results.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# plot_results.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
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

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

#plt.rc('text', usetex=True)
plt.rcParams['font.size'] = (15)
#plt.rcParams['font.family'] = ('sans-serif')
#plt.rcParams['mathtext.fontset'] = ('dejavusans')
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['lines.markersize'] = 10

def errorbar(x, y, err, **kwargs):
    (_, caps, _) = plt.errorbar(x, y, yerr=err, **kwargs)
    for cap in caps:
        cap.set_markeredgewidth(5)

ss_r_sphere = 1.824e-04
ss_r_rastrigin = 7.282e-02
pt_r_sphere = 5.718e-04
pt_s_sphere = 1.071e-04
pt_r_rastrigin = 1.854e-01
pt_s_rastrigin = 3.298e-2
sa_r_sphere = 1.943e-03
sa_s_sphere = 4.732e-04
sa_r_rastrigin = 1.264e-02
sa_s_rastrigin = 2.774e-03
gmcres_r_sphere = 3.842e-07
gmcres_s_sphere = 8.855e-07
gmcres_r_rastrigin = 3.666e-05
gmcres_s_rastrigin = 9.083e-06
es_r_sphere = 4.033e-07
es_s_sphere = 6.205e-08
es_r_rastrigin = 3.887e-05
es_s_rastrigin = 7.920e-06
ptr_r_sphere = 3.776e-09
ptr_s_sphere = 7.465e-10
ptr_r_rastrigin = 2.670e-03
ptr_s_rastrigin = 6.667e-04
ptm_r_sphere = 4.808e-06
ptm_s_sphere = 1.047e-06
ptm_r_rastrigin = 5.942e-04
ptm_s_rastrigin = 1.125e-04

sphere_results = [
        ss_r_sphere,
        pt_r_sphere,
        sa_r_sphere,
        es_r_sphere,
        gmcres_r_sphere,
        ptr_r_sphere,
        ptm_r_sphere
        ]

sphere_stddev = [
        pt_s_sphere,
        sa_s_sphere,
        es_s_sphere,
        gmcres_s_sphere,
        ptr_s_sphere,
        ptm_s_sphere
        ]

rastrigin_results = [
        ss_r_rastrigin,
        pt_r_rastrigin,
        sa_r_rastrigin,
        es_r_rastrigin,
        gmcres_r_rastrigin,
        ptr_r_rastrigin,
        ptm_r_rastrigin
        ]

rastrigin_stddev = [
        pt_s_rastrigin,
        sa_s_rastrigin,
        es_s_rastrigin,
        gmcres_s_rastrigin,
        ptr_s_rastrigin,
        ptm_s_rastrigin
        ]

xvalues = [0, 1, 2, 3, 4, 5, 6]
xlabels = [
           u'S. S.',#u'Simple Sampling',
           u'P. T.',#u'Parallel Tempering',
           u'S. A.',#u'Simulated Annealing',
           u'ES',#u'ES',
           u'GMRC-ES',#u'GMRC-ES',
           u'P. T. restarts',#u'Parallel Tempered restarts',
           u'P. T. mutation'#u'Parallel Tempered mutation'
           ]

fig = plt.figure()
fig.set_size_inches(7.0, 6.0, forward=True)
ax = fig.add_subplot(111)
errorbar(np.arange(1, len(sphere_results)), sphere_results[1:], sphere_stddev, fmt = "oC0", capsize = 5)
plt.plot(0, sphere_results[0], "oC0")
plt.xticks(xvalues, xlabels, rotation=40)
ax.set_xlabel(r"Experiment")
ax.set_ylabel(r"$f($"+"Experiment"+r"$)$")
ax.set_yscale("log")
plt.title(r"Sphere function")
fig.tight_layout()

fig = plt.figure()
fig.set_size_inches(7.0, 6.0, forward=True)
ax = fig.add_subplot(111)
errorbar(np.arange(1, len(rastrigin_results)), rastrigin_results[1:], rastrigin_stddev, fmt = "oC0", capsize = 5)
plt.plot(0, rastrigin_results[0], "oC0")
plt.xticks(xvalues, xlabels, rotation=40)
ax.set_xlabel(r"Experiment")
ax.set_ylabel(r"$f($"+"Experiment"+r"$)$")
ax.set_yscale("log")
plt.title(r"Rastrigin function")
fig.tight_layout()

fig = plt.figure()
fig.set_size_inches(7.0, 6.0, forward=True)
ax = fig.add_subplot(111)
errorbar(np.arange(1, len(sphere_results)), sphere_results[1:], sphere_stddev, fmt = "oC0", capsize = 5)
plt.plot(0, sphere_results[0], "oC0", label=r"Sphere function")
errorbar(np.arange(1, len(rastrigin_results)), rastrigin_results[1:], rastrigin_stddev, fmt = "sC1", capsize = 5)
plt.plot(0, rastrigin_results[0], "sC1", label=r"Rastrigin function")
plt.xticks(xvalues, xlabels, rotation=40)
ax.set_xlabel(r"Experiment")
ax.set_ylabel(r"$f($"+"Experiment"+r"$)$")
ax.set_yscale("log")
plt.legend()
fig.tight_layout()


#plt.style.use('dark_background')
