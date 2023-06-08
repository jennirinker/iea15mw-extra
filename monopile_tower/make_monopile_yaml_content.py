"""Make the yaml content for the monopile based on the original design.
"""
import numpy as np


STN = np.array([-75, -30., -29.999, -25., -24.999, -20., -19.999, -15., -14.999, -10., -9.999, -5., -4.999, 0., 0.001, 5., 5.001, 10., 10.001, 15.])
OUT_DIAM = np.array([10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.])
THICK = np.array([0.055341, 0.055341, 0.055341, 0.055341, 0.053449, 0.053449, 0.051509, 0.051509, 0.049527, 0.049527, 0.047517, 0.047517, 0.045517, 0.045517, 0.043527, 0.043527, 0.042242, 0.042242, 0.041058, 0.041058])


# get grid values from normalized STN
grid = (STN - STN[0]) / (STN[-1] - STN[0])

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

STN_str = np.array2string(STN, formatter={'float_kind':lambda x: '%.3f' % x}, **kwargs)
od_str = np.array2string(OUT_DIAM, formatter={'float_kind':lambda x: '%.3f' % x}, **kwargs)
thick_str = np.array2string(THICK, formatter={'float_kind':lambda x: '%.6f' % x}, **kwargs)

space = '    '
with open('yaml_content_monopile.yaml', 'w', encoding='utf-8') as f:
    f.write(space + 'x:\n')
    f.write(2*space + 'grid: ' + grid_str + '\n')
    f.write(2*space + 'values: ' + x_str + '\n')
    f.write(space + 'y:\n')
    f.write(2*space + 'grid: ' + grid_str + '\n')
    f.write(2*space + 'values: ' + y_str + '\n')
    f.write(space + 'z:\n')
    f.write(2*space + 'grid: ' + grid_str + '\n')
    f.write(2*space + 'values: ' + STN_str + '\n')
    f.write('outer_diameter:\n')
    f.write(space + 'grid: ' + grid_str + '\n')
    f.write(space + 'values: ' + od_str + '\n')
    f.write('\n')
    f.write('thickness:\n')
    f.write(space + 'grid: ' + grid_str + '\n')
    f.write(space + 'values: ' + thick_str + '\n')
