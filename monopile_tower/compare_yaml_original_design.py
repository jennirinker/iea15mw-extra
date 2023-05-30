"""Compare the yaml tower properties to the original design.

Requirements:
    - numpy, matplotlib, pyyaml
    - Update of IEA15MW_GIT_DIR variable (see below)

Tested on commit d994b401947caa491f30fece482d111ee008e98d of IEA 15 MW repo.

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

# load the yaml file as nested dictionaries
yamldata = myf.load_yaml(yaml_path)

# load values from yaml
twr_stn, out_diam, thick, E, G, rho, outfit = myf.load_body_properties('tower', yamldata)

# assign aliases to original parameters in _functions for convenience
out_diam_orig = myf.OUT_DIAM_ORIG
twr_stn_orig = myf.TWR_STN_ORIG
thick_orig = myf.THICK_ORIG

# plot the raw data in the yaml file and the original design
fig, (ax0, ax1) = plt.subplots(1, 2, num=1, figsize=(7, 3.5))
ax0.plot(out_diam, twr_stn, label='Currently in yaml')
ax0.plot(out_diam_orig, twr_stn_orig, '--', label='Original design')
ax0.set(xlabel='Outer diameter [m]', ylabel='Tower height [m]')
ax0.legend()
ax0.grid('on')
ax1.plot(thick*1000, twr_stn)
ax1.plot(thick_orig*1000, twr_stn_orig, '--')
ax1.set(xlabel='Wall thickness [mm]', ylabel='Tower height [m]')
ax1.grid('on')
fig.suptitle('Comparison of yaml and original design')
fig.tight_layout()

# calculate mass of tower (theory)
mpl = myf.calculate_mpl(out_diam, thick, rho, outfitting_factor=outfit)
mpl_orig = myf.calculate_mpl(out_diam_orig, thick_orig, rho, outfitting_factor=outfit)
mass = np.trapz(mpl, twr_stn)
mass_orig = np.trapz(mpl_orig, twr_stn_orig)
print('Tower mass, excl. transition piece, incl. outfitting')
print('-----------------------------------------------------')
print('In report (tons):', 760)
print('Original design (tons):', mass_orig * 1e-3)
print('"Raw" from yaml (tons):', mass * 1e-3)

plt.show()
