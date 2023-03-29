# setup so you can view newton iteration
# for each step render
# surface
# target dir
# current dir
# notice if something is up with the algorithm
# and then fix accordingly
# also output vars like u & v and new U & v and change vector
# etc..

from mpl_toolkits.mplot3d import axes3d
#import matplotlib.pyplot as plt
import matplotlib.animation as animation

from geomdl import knotvector
from geomdl import BSpline
from geomdl.visualization import VisMPL
from geomdl import utilities
import matplotlib.pyplot as plt
from geomdl import multi
import argparse
import ast

parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("--line1", help="Line 1.", default="[[0.0, 0.0, 0.0], [4.0, 4.0, 4.0]]")
parser.add_argument("--line2", help="Line 2.", default="[[0.0, 4.0, 0.0], [4.0, 0.0, 4.0]]")
args = parser.parse_args()
l1arr = ast.literal_eval(args.line1)
l2arr = ast.literal_eval(args.line2)
print(l1arr)
print(l2arr)
"""
ctrlpts = [
    [[-25.0, -25.0, -10.0], [-25.0, -15.0, -5.0], [-25.0, -5.0, 0.0], [-25.0, 5.0, 0.0], [-25.0, 15.0, -5.0], [-25.0, 25.0, -10.0]],
    [[-15.0, -25.0, -8.0], [-15.0, -15.0, -4.0], [-15.0, -5.0, -4.0], [-15.0, 5.0, -4.0], [-15.0, 15.0, -4.0], [-15.0, 25.0, -8.0]],
    [[-5.0, -25.0, -5.0], [-5.0, -15.0, -3.0], [-5.0, -5.0, -8.0], [-5.0, 5.0, -8.0], [-5.0, 15.0, -3.0], [-5.0, 25.0, -5.0]],
    [[5.0, -25.0, -3.0], [5.0, -15.0, -2.0], [5.0, -5.0, -8.0], [5.0, 5.0, -8.0], [5.0, 15.0, -2.0], [5.0, 25.0, -3.0]],
    [[15.0, -25.0, -8.0], [15.0, -15.0, -4.0], [15.0, -5.0, -4.0], [15.0, 5.0, -4.0], [15.0, 15.0, -4.0], [15.0, 25.0, -8.0]],
    [[25.0, -25.0, -10.0], [25.0, -15.0, -5.0], [25.0, -5.0, 2.0], [25.0, 5.0, 2.0], [25.0, 15.0, -5.0], [25.0, 25.0, -10.0]]
]"""

arr = [[0]*4 for i in range(4)]
#print(arr)
arr[0][0] = [0, 0, 0]
arr[0][1] = [1, 0, 1]
arr[0][2] = [2, 0, -1]
arr[0][3] = [3, 0, 0]

arr[1][0] = [0, 1, 0]
arr[1][1] = [1, 1, 1]
arr[1][2] = [2, 1, -1]
arr[1][3] = [3, 1, 0]

arr[2][0] = [0, 2, 0]
arr[2][1] = [1, 2, 1]
arr[2][2] = [2, 2, -1]
arr[2][3] = [3, 2, 0]

arr[3][0] = [0, 3, 0]
arr[3][1] = [1, 3, 1]
arr[3][2] = [2, 3, -1]
arr[3][3] = [3, 3, 0]

# Create a BSpline surface
surf = BSpline.Surface()

# Set degrees
surf.degree_u = 3
surf.degree_v = 3

# Set control points
surf.ctrlpts2d = arr

# Set knot vectors
#
#print(knotvector.generate(3,16))
print(arr)
surf.knotvector_u = [0.0,0.0,0.0,0.33,0.66,1.0,1.0,1.0] 
surf.knotvector_v = [0.0,0.0,0.0,0.33,0.66,1.0,1.0,1.0] 
# Set evaluation delta
surf.delta = 0.025

# Evaluate surface points
surf.evaluate()

# Import and use Matplotlib's colormaps
from matplotlib import cm

# Plot the control points grid and the evaluated surface
surf.vis = VisMPL.VisSurface()

# Create a B-Spline curve
l1 = BSpline.Surface()
l1.degree_u = 1
l1.degree_v = 1
print([l1arr,l1arr])
l1.ctrlpts2d = [l1arr,l1arr]
l1.knotvector_u = knotvector.generate(1, 2)
l1.knotvector_v = knotvector.generate(1, 2)
l1.delta = 0.01
l1.vis = VisMPL.VisSurface()

l2 = BSpline.Surface()
l2.degree_u = 1
l2.degree_v = 1
l2.ctrlpts2d = [l2arr,l2arr]
l2.knotvector_u = knotvector.generate(1, 2)
l2.knotvector_v = knotvector.generate(1, 2)
l2.delta = 0.01
l2.vis = VisMPL.VisSurface()
# Auto-generate knot vector
#curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

# Set evaluation delta
#curve.delta = 0.01


# Plot the control point polygon and the evaluated curve
#curve.vis = VisMPL.VisCurve2D()
#s2.vis = VisMPL.VisCurve3D()
#curve.render()

c=multi.SurfaceContainer([surf, l1, l2])
c.vis=VisMPL.VisSurface()
vertical_axis = 'y'
elev, azim, roll = 30, 0, 0
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# FIGURE OUT HOW TO GET PROJECTION 3D FOR BETTTER DEBUG
# HOW CAN I GET MATPLOT FIGURE FROM VISSURFACE c.VIS
ax.view_init(vertical_axis=vertical_axis)
c.render()