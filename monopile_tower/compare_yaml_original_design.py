"""Compare the yaml tower properties to the original design.

Requirements:
    - numpy, matplotlib, pyyaml
    - Update of IEA15MW_GIT_DIR variable (see below)

Tested on commit d994b401947caa491f30fece482d111ee008e98d of IEA 15 MW repo.

NOTE
You must (1) have a local copy of the IEA 15 MW repo and (2) update the IEA15MW_GIT_DIR
variable in _iea15mwpath.py to run this script.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import yaml

from _functions import load_body_properties, calculate_mpl
from _iea15mwpath import IEA15MW_GIT_DIR



# paths
yaml_path = IEA15MW_GIT_DIR / 'WT_Ontology/IEA-15-240-RWT.yaml'  # yaml file with data

# load the yaml file as nested dictionaries
with open(yaml_path, 'r') as stream:
    try:
        yamldata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# ------------- tower -------------
twr_stn, out_diam, thick, E, G, rho, outfit = load_body_properties('tower', yamldata)


# Original design
twr_stn_orig = np.array([15, 15.01, 28, 28.01, 41, 41.01, 54, 54.01, 67, 67.01, 80, 80.01, 93, 93.01, 106, 106.01, 119, 119.01, 132, 132.01, 144.386])
out_diam_orig = np.array([10., 10., 10., 10., 9.926, 9.926, 9.443, 9.443, 8.833, 8.833, 8.151, 8.151, 7.39, 7.39, 6.909, 6.909, 6.748, 6.748, 6.572, 6.572, 6.5])
thick_orig = np.array([0.041058, 0.039496, 0.039496, 0.036456, 0.036456, 0.033779, 0.033779, 0.032192, 0.032192, 0.030708, 0.030708, 0.029101, 0.029101, 0.027213, 0.027213, 0.024009, 0.024009, 0.020826, 0.020826, 0.023998, 0.023998])

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
mpl = calculate_mpl(out_diam, thick, rho, outfitting_factor=outfit)
mpl_orig = calculate_mpl(out_diam_orig, thick_orig, rho, outfitting_factor=outfit)
mass = np.trapz(mpl, twr_stn)
mass_orig = np.trapz(mpl_orig, twr_stn_orig)
print('Tower mass, excl. transition piece, incl. outfitting')
print('-----------------------------------------------------')
print('In report (tons):', 760)
print('Original design (tons):', mass_orig * 1e-3)
print('"Raw" from yaml (tons):', mass * 1e-3)

plt.show()
