import matplotlib.pyplot as plt
import numpy as np

def display_maze_with_path(maze):
    rows, cols = len(maze), len(maze[0])
    color_map = {
        0: "dimgray", 1: "lightgray", 3: "limegreen", 4: "tomato"
    }
    color_matrix = [[color_map[cell] for cell in row] for row in maze]
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow([[0] * cols for _ in range(rows)], cmap="Greys", vmin=0, vmax=4)
    for i in range(rows):
        for j in range(cols):
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color_matrix[i][j]))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    plt.title("Maze with Path", fontsize=18)
    plt.show()
maze = [
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0]
]
maze[0][0] = 3
maze[-1][-1] = 4
display_maze_with_path(maze)
