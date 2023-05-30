"""Compare the HAWC2, OpenFAST, and yaml towers.


NOTE
You must (1) have a local copy of the IEA 15 MW repo and (2) update the IEA15MW_GIT_DIR
variable in _iea15mwpath.py to run this script.
"""
import matplotlib.pyplot as plt
import numpy as np

import _functions as myf
from _iea15mwpath import IEA15MW_GIT_DIR


# paths
yaml_path = IEA15MW_GIT_DIR / 'WT_Ontology/IEA-15-240-RWT.yaml'  # yaml file with data
ed_path = IEA15MW_GIT_DIR / 'OpenFAST/IEA-15-240-RWT-Monopile/IEA-15-240-RWT-Monopile_ElastoDyn_tower.dat'  # elastodyn file
h2_st_path = IEA15MW_GIT_DIR / 'HAWC2/IEA-15-240-RWT-FixedSubstructure/data/IEA_15MW_RWT_Tower_st.dat'  # hawc2 st file

# load the yaml file as nested dictionaries
yamldata = myf.load_yaml(yaml_path)

# load the tower properties from the yaml, calculate what we need to plot
twr_stn, out_diam, thick, E, G, rho, outfit = myf.load_body_properties('tower', yamldata)
mpl_yaml = myf.calculate_mpl(out_diam, thick, rho, outfitting_factor=outfit)
EI_yaml = E * myf.calculate_mom_iner(out_diam, thick)

# calculate same values for the original design
mpl_orig = myf.calculate_mpl(myf.OUT_DIAM_ORIG, myf.THICK_ORIG, rho, outfitting_factor=outfit)
EI_orig = E * myf.calculate_mom_iner(myf.OUT_DIAM_ORIG, myf.THICK_ORIG)

# load the elastodyn tower properties
ed_st = myf.load_elastodyn_distprop(ed_path)

# load the hawc2 tower properties
h2_st = myf.load_hawc2_st(h2_st_path)

# visualize the difference
fig, axs = plt.subplots(1, 3, num=1, figsize=(8, 3.5))

# define y values
y_orig = myf.normalize_tower_station(myf.TWR_STN_ORIG)
y_yaml = myf.normalize_tower_station(twr_stn)
y_ed = myf.normalize_tower_station(ed_st[:, 0])
y_hawc2 = myf.normalize_tower_station(h2_st[:, 0])

# plot mass per length and two bending stiffnesses
for iax, ax in enumerate(axs):
    if iax == 0:  # mass per unit length
        x_orig = mpl_orig
        x_ed = ed_st[:, 1]
        x_yaml = mpl_yaml
        x_hawc2 = h2_st[:, 1]
        AXTITLE = 'Mass per unit length'
    elif iax == 1:  # bending stiffness -- x direction
        x_orig = EI_orig
        x_ed = ed_st[:, 2]
        x_yaml = EI_yaml
        x_hawc2 = h2_st[:, 8]*h2_st[:, 10]
        AXTITLE = 'Fore-aft bending stiff.'
    elif iax == 2:  # bending stiffness -- y direction
        x_orig = EI_orig
        x_ed = ed_st[:, 3]
        x_yaml = EI_yaml
        x_hawc2 = h2_st[:, 8]*h2_st[:, 11]
        AXTITLE = 'Side-side bending stiff.'
    ax.plot(x_orig, y_orig, c='k', label='Original design')
    ax.plot(x_yaml, y_yaml, c='C0', label='In yaml file')
    ax.plot(x_ed, y_ed, marker='.', c='C1', lw=1, label='OpenFAST')
    ax.plot(x_hawc2, y_hawc2, '--', c='C2', marker='+', lw=1, label='HAWC2')
    ax.grid()
    ax.set(title=AXTITLE)

axs[0].legend(fontsize='small')
axs[0].set(ylabel='Normalized tower height [-]')

fig.tight_layout()

plt.show()
