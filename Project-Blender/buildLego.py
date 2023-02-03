import bpy
import sys
import os
import numpy as np

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
    x_size = 7
    y_size = 5
    z_size = 3
    matrix = np.random.randint(2, size=(x_size, y_size, z_size))
    matrix_copy = np.copy(matrix)

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

    if (visited == matrix).all() and checkLargestAxis():

        return matrix.tolist()
        #return np.any(matrix[:, 2, :] == 1)
    else:

        return create_connected_matrix()
