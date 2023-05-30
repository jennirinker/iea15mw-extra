"""Helper functions for scripts for onshore tower analysis.
"""
import numpy as np


PI = np.pi  # for convenience


def load_body_properties(bodyname, yamldict, start_from_zero=False):
    """Get body geometry and material properties from yaml data.

    tower station, outer diameter, thickness, E, G, rho.
    """
    # body dictionary
    bodydict = yamldict['components'][bodyname]
    # get tower dimensions
    twr_stn = np.array(bodydict['outer_shape_bem']['reference_axis']['z']['values'])
    if start_from_zero:
        twr_stn -= twr_stn[0]
    outfitting_factor = bodydict['internal_structure_2d_fem']['outfitting_factor']
    out_diam = np.array(bodydict['outer_shape_bem']['outer_diameter']['values'])
    wall = bodydict['internal_structure_2d_fem']['layers'][0]
    assert wall['name'] == bodyname + '_wall'
    thick = np.array(wall['thickness']['values'])
    # get material properties
    material = wall['material']
    mat_props = [d for d in yamldict['materials'] if d['name'] == material][0]
    E, G, rho = mat_props['E'], mat_props['G'], mat_props['rho']
    return twr_stn, out_diam, thick, E, G, rho, outfitting_factor


def calculate_area(out_diam, thick):
    """Calculate area of tower."""
    r_out = out_diam / 2  # outer diameter [m]
    r_in = r_out - thick  # inner diameter [m]
    return PI * (r_out**2 - r_in**2)  # cross-sectional area [m^2]


def calculate_mpl(out_diam, thick, rho, outfitting_factor=1):
    """Calculate mass per unit length, including outfitting."""
    area = calculate_area(out_diam, thick)
    return rho * area * outfitting_factor
