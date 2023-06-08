"""Make the yaml content for the tower based on the original design.
"""
import matplotlib.pyplot as plt
import numpy as np

from _functions import TWR_STN_NEW, OUT_DIAM_NEW, THICK_NEW


# get grid values from normalized twr_stn
grid = (TWR_STN_NEW - TWR_STN_NEW[0]) / (TWR_STN_NEW[-1] - TWR_STN_NEW[0])

# create x and y values
x = np.zeros_like(grid)
y = np.zeros_like(grid)

# constant formatter settings
kwargs = {'separator': ', ', 'max_line_width': 10000}

# make strings of all the arrays
grid_str = np.array2string(grid, formatter={'float_kind':lambda x: '%.17f' % x}, **kwargs)
grid_str = grid_str.replace('0.00000000000000000', '0.0')

x_str = np.array2string(x, formatter={'float_kind':lambda x: '%.1f' % x}, **kwargs)
y_str = np.array2string(y, formatter={'float_kind':lambda x: '%.1f' % x}, **kwargs)

twr_stn_str = np.array2string(TWR_STN_NEW, formatter={'float_kind':lambda x: '%.3f' % x}, **kwargs)
od_str = np.array2string(OUT_DIAM_NEW, formatter={'float_kind':lambda x: '%.3f' % x}, **kwargs)
thick_str = np.array2string(THICK_NEW, formatter={'float_kind':lambda x: '%.6f' % x}, **kwargs)

space = '    '
with open('yaml_content.yaml', 'w', encoding='utf-8') as f:
    f.write(space + 'x:\n')
    f.write(2*space + 'grid: ' + grid_str + '\n')
    f.write(2*space + 'values: ' + x_str + '\n')
    f.write(space + 'y:\n')
    f.write(2*space + 'grid: ' + grid_str + '\n')
    f.write(2*space + 'values: ' + y_str + '\n')
    f.write(space + 'z:\n')
    f.write(2*space + 'grid: ' + grid_str + '\n')
    f.write(2*space + 'values: ' + twr_stn_str + '\n')
    f.write('outer_diameter:\n')
    f.write(space + 'grid: ' + grid_str + '\n')
    f.write(space + 'values: ' + od_str + '\n')
    f.write('\n')
    f.write('thickness:\n')
    f.write(space + 'grid: ' + grid_str + '\n')
    f.write(space + 'values: ' + thick_str + '\n')
