import matplotlib.pyplot as plt
import numpy as np

def display_maze_with_path(rows, cols, walls, path):
    # Initialize maze grid with 0 (unvisited cells)
    maze = np.zeros((rows, cols), dtype=int)

    # Mark walls as 1
    for wall in walls:
        r, c = wall
        maze[r, c] = 1

    # Define colors: 0 -> Grey (unvisited), 1 -> Black (wall)
    # 2 -> White (path), 3 -> Green (start), 4 -> Red (end)
    color_map = {
        0: "grey",  # Unvisited
        1: "black", # Wall
        2: "white", # Path
        3: "green", # Start
        4: "red"    # End
    }

    # Mark the path
    for cell in path:
        r, c = cell
        maze[r, c] = 2

    # Mark start and end
    start = path[0]
    end = path[-1]
    maze[start[0], start[1]] = 3
    maze[end[0], end[1]] = 4

    # Create a color matrix
    color_matrix = [[color_map[cell] for cell in row] for row in maze]

    # Plot the maze
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow([[0] * cols for _ in range(rows)], cmap="Greys", vmin=0, vmax=4)

    # Color each cell
    for i in range(rows):
        for j in range(cols):
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color_matrix[i][j]))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    plt.title("Maze with Path", fontsize=16)
    plt.show()


# Example Usage
rows = 5
cols = 5
walls = [(1, 1), (1, 3), (2, 3), (3, 1), (3, 3)]
path = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]

display_maze_with_path(rows, cols, walls, path)
