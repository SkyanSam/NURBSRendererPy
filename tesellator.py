from mpl_toolkits.mplot3d import axes3d
import matplotlib.animation as animation

from geomdl import knotvector
from geomdl import BSpline
from geomdl.visualization import VisMPL
from geomdl import utilities
import matplotlib.pyplot as plt
from geomdl import multi
import argparse
import ast
import numpy as np

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

def coords_to_index(x,y,sqrt_vertices):
    return int(y * sqrt_vertices) + (x)

def index_to_coords(index,sqrt_vertices):
    return (index % sqrt_vertices, int(index / sqrt_vertices))

ind = coords_to_index(1,1,4)
coo = index_to_coords(ind,4)
print(str(ind) + " , " + str(coo))

def evaluate(sqrt_vertices):
    surf.delta = 1.0 / sqrt_vertices
    surf.evaluate(start_u=0.0, stop_u=1.0, start_v=0.0, stop_v=1.0)
    positions = np.asarray(surf.evalpts)
    indices_arr = []
    for i in range(0,sqrt_vertices):
        coords = index_to_coords(i,4)
        if (coords[0] < sqrt_vertices - 1 and coords[1] < sqrt_vertices - 1):
            indices_arr.append(i)
            indices_arr.append(coords_to_index(coords[0] + 1,coords[1],sqrt_vertices))
            indices_arr.append(coords_to_index(coords[0] + 1,coords[1] + 1,sqrt_vertices))
            indices_arr.append(i)
            indices_arr.append(coords_to_index(coords[0],coords[1] + 1,sqrt_vertices))
            indices_arr.append(coords_to_index(coords[0] + 1,coords[1] + 1,sqrt_vertices))
    indices = np.asarray(indices_arr)
    return positions, indices
    #print(surf.evalpts)
    

print(evaluate(4))
