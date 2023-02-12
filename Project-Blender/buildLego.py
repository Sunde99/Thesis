import bpy
import sys
import os
import numpy as np
import random

if __name__ == "__main__":
    # Set up imports
    dir = os.path.dirname(bpy.data.filepath)
    if not dir in sys.path:
        sys.path.append(dir )
    print("dir: " + str(dir))

    import CleanScene 

    # Delete EVERYTHING!

    CleanScene.clean_scene()


def create_connected_matrix():
    # Create an empty 3x3x3 matrix
    x_max_size = 7
    x_size = random.randint(2, x_max_size)

    y_max_size = 5
    y_size = random.randint(1, min(y_max_size, x_size-1))

    z_max_size = 3
    z_size = random.randint(1, z_max_size)
    print(x_size, y_size, z_size)
    matrix = np.random.randint(2, size=(x_size, y_size, z_size))
    matrix_copy = np.copy(matrix)
    #matrix = np.pad(matrix, ((0, x_max_size-x_size), (0, y_max_size-y_size), (z_max_size-z_size, 0)),  mode='constant', constant_values=0)

    # Define the neighbors of a given cell
    neighbors = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
    indices_of_1s = []
    while True:
        # Identify the isolated 1s
        indices_of_1s = np.argwhere(matrix)

        isolated_indices = []
        for x, y, z in indices_of_1s:
            is_isolated = True
            for dx, dy, dz in neighbors:
                if 0 <= x+dx < x_size and 0 <= y+dy < y_size and 0 <= z+dz < z_size and matrix[x+dx, y+dy, z+dz] == 1:
                    is_isolated = False
                    break
            if is_isolated:
                isolated_indices.append((x, y, z))
        if not isolated_indices:
            break
        for x, y, z in isolated_indices:
            matrix[x, y, z] = 0


    # check if the object is connected
    indices = np.argwhere(matrix)
    if indices.size == 0:
        return create_connected_matrix()
    start = indices[0]
    visited = np.zeros((x_size,y_size,z_size))

    def DFS(x, y, z):
        visited[x][y][z] = 1
        for dx, dy, dz in neighbors:
            if 0 <= x+dx < x_size and 0 <= y+dy < y_size and 0 <= z+dz < z_size and matrix[x+dx][y+dy][z+dz]==1 and visited[x+dx][y+dy][z+dz]==0:
                DFS(x+dx, y+dy, z+dz)

    DFS(*start)

    def checkLargestAxis():
        smallest_x_index = np.min(indices[:, 0])
        largest_x_index = np.max(indices[:, 0])

        smallest_y_index = np.min(indices[:, 1])
        largest_y_index = np.max(indices[:, 1])

        x_diff = largest_x_index - smallest_x_index
        y_diff = largest_y_index - smallest_y_index

        return x_diff > y_diff

    def fillsGrid(matrix):
        x_planes = [matrix[0,:,:], matrix[x_size-1,:,:]]
        y_planes = [matrix[:,0,:], matrix[:,y_size-1,:]]
        z_planes = [matrix[:,:,0], matrix[:,:,z_size-1]]
        return all(np.any(plane == 1) for plane in x_planes + y_planes + z_planes)


    if (visited == matrix).all() and checkLargestAxis() and fillsGrid(matrix):
        #print(matrix_copy.tolist())
        matrix = np.pad(matrix, ((0, x_max_size-x_size), (0, y_max_size-y_size), (z_max_size-z_size, 0)),  mode='constant', constant_values=0)
        return (matrix.tolist(), x_size, y_size, z_size)
        #return np.any(matrix[:, 2, :] == 1)
    else:

        return create_connected_matrix()
