import bpy
import sys
import os
import numpy as np

# Set up imports
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
print("dir: " + str(dir))

import CleanScene 

# Delete EVERYTHING!

CleanScene.clean_scene()

# Create an empty 3x3x3 matrix
import numpy as np


def create_connected_matrix():
    # Create an empty 3x3x3 matrix
    matrix = np.random.randint(2, size=(3, 3, 3))
    matrix_copy = np.copy(matrix)

    # Define the neighbors of a given cell
    neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    indices_of_1s = []
    while True:
        # Identify the isolated 1s
        indices_of_1s = np.argwhere(matrix == 1)
        isolated_indices = []
        for x, y, z in indices_of_1s:
            is_isolated = True
            for dx, dy, dz in neighbors:
                if 0 <= x+dx < 3 and 0 <= y+dy < 3 and 0 <= z+dz < 3 and matrix[x+dx, y+dy, z+dz] == 1:
                    is_isolated = False
                    break
            if is_isolated:
                isolated_indices.append((x, y, z))
        if not isolated_indices:
            break
        for x, y, z in isolated_indices:
            matrix[x, y, z] = 0

    # check if the object is connected
    indices = np.argwhere(matrix == 1)
    if indices.size == 0:
        return create_connected_matrix()
    start = indices[0]
    visited = np.zeros((3,3,3))

    def DFS(x, y, z):
        visited[x][y][z] = 1
        for dx, dy, dz in neighbors:
            if 0 <= x+dx < 3 and 0 <= y+dy < 3 and 0 <= z+dz < 3 and matrix[x+dx][y+dy][z+dz]==1 and   visited[x+dx][y+dy][z+dz]==0:
                DFS(x+dx, y+dy, z+dz)

    DFS(*start)

    if (visited == matrix).all():
        if np.any(matrix[:, 2, :] == 1):
            return matrix.tolist()
    return create_connected_matrix()
