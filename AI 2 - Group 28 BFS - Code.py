import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Enum for different cell types
class CellType:
    EMPTY = ' '
    TRAP_1 = 'T1'
    TRAP_2 = 'T2'
    TRAP_3 = 'T3'
    TRAP_4 = 'T4'
    REWARD_1 = 'R1'
    REWARD_2 = 'R2'
    TREASURE = 'TR'
    OBSTACLE = 'OB'

# Object for each Hexagon / Cell
class Hex:
    def __init__(self, q, r, cellType):
        self.q = q
        self.r = r
        self.cellType = cellType

# Dictionary to hold maze information
maze_data = [
    ((1,0), CellType.EMPTY),
    ((1,2), CellType.EMPTY),
    ((1,4), CellType.OBSTACLE),
    ((1,6), CellType.EMPTY),
    ((1,8), CellType.EMPTY),
    ((1,10), CellType.EMPTY),

    ((2,1), CellType.EMPTY),
    ((2,3), CellType.EMPTY),
    ((2,5), CellType.REWARD_1),
    ((2,7), CellType.EMPTY),
    ((2,9), CellType.TRAP_2),
    ((2,11), CellType.EMPTY),

    ((3,0), CellType.EMPTY),
    ((3,2), CellType.TRAP_2),
    ((3,4), CellType.EMPTY),
    ((3,6), CellType.OBSTACLE),
    ((3,8), CellType.EMPTY),
    ((3,10), CellType.EMPTY),

    ((4,1), CellType.EMPTY),
    ((4,3), CellType.TREASURE),
    ((4,5), CellType.OBSTACLE),
    ((4,7), CellType.EMPTY),
    ((4,9), CellType.TRAP_4),
    ((4,11), CellType.EMPTY),

    ((5,0), CellType.EMPTY),
    ((5,2), CellType.OBSTACLE),
    ((5,4), CellType.EMPTY),
    ((5,6), CellType.OBSTACLE),
    ((5,8), CellType.TREASURE),
    ((5,10), CellType.REWARD_1),

    ((6,1), CellType.REWARD_2),
    ((6,3), CellType.EMPTY),
    ((6,5), CellType.TRAP_3),
    ((6,7), CellType.EMPTY),
    ((6,9), CellType.EMPTY),
    ((6,11), CellType.EMPTY),

    ((7,0), CellType.EMPTY),
    ((7,2), CellType.OBSTACLE),
    ((7,4), CellType.OBSTACLE),
    ((7,6), CellType.EMPTY),
    ((7,8), CellType.TRAP_3),
    ((7,10), CellType.EMPTY),

    ((8,1), CellType.EMPTY),
    ((8,3), CellType.OBSTACLE),
    ((8,5), CellType.TREASURE),
    ((8,7), CellType.REWARD_2),
    ((8,9), CellType.EMPTY),
    ((8,11), CellType.EMPTY),

    ((9,0), CellType.EMPTY),
    ((9,2), CellType.EMPTY),
    ((9,4), CellType.EMPTY),
    ((9,6), CellType.TRAP_1),
    ((9,8), CellType.OBSTACLE),
    ((9,10), CellType.EMPTY),

    ((10,1), CellType.EMPTY),
    ((10,3), CellType.EMPTY),
    ((10,5), CellType.TREASURE),
    ((10,7), CellType.EMPTY),
    ((10,9), CellType.EMPTY),
    ((10,11), CellType.EMPTY)
]

# Convert dictionary data into list of Hex objects
maze = {}
for coord, cellType in maze_data:
    q, r = coord
    maze[(q,r)] = Hex(q, r, cellType)


# Function to plot the maze
def plot_maze(maze, paths=[]):
    fig, ax = plt.subplots(1, figsize=(10, 6))

    for (q, r), hex in maze.items():
        
        # Calculation positions of Hex Grids
        # From https://www.redblobgames.com/grids/hexagons/ (Spacing Section)
        x = q * 3/2
        y = r * np.sqrt(3) / 2
        
        # Diffrent colours for each cell type
        if hex.cellType == CellType.OBSTACLE:
            hexagon = plt.Polygon(hex_corners(x, y), edgecolor='k', facecolor='gray')
        elif hex.cellType == CellType.TREASURE:
            hexagon = plt.Polygon(hex_corners(x, y), edgecolor='k', facecolor='gold')
        elif hex.cellType == CellType.REWARD_1 or hex.cellType == CellType.REWARD_2:
            hexagon = plt.Polygon(hex_corners(x, y), edgecolor='k', facecolor='lightblue')
        elif hex.cellType == CellType.TRAP_1 or hex.cellType == CellType.TRAP_2 or hex.cellType == CellType.TRAP_3 or hex.cellType == CellType.TRAP_4:
            hexagon = plt.Polygon(hex_corners(x, y), edgecolor='k', facecolor='violet')
        else:
            hexagon = plt.Polygon(hex_corners(x, y), edgecolor='k', facecolor='white')
        
        ax.add_patch(hexagon)
        ax.text(x, y, f'{hex.cellType} ({q}, {r})', ha='center', va='center', fontsize=8)

    # Draw path lines
    for path in paths:
        path_x = [q * 3/2 for q, r in path]
        path_y = [r * np.sqrt(3) / 2 for q, r in path]
        ax.plot(path_x, path_y, color='red', linewidth=1, marker='o', markerfacecolor='black')
        
        
    ax.set_aspect('equal')
    plt.xlim(-2, 20)
    plt.ylim(-2, 11)
    plt.grid(False)
    plt.axis('off')
    plt.show()

# Calculate the coordinates of each corner
# From https://www.redblobgames.com/grids/hexagons/
def hex_corners(x_center, y_center, size=1):
    angles = np.linspace(0, 2 * np.pi, 7)
    return [(x_center + size * np.cos(angle), y_center + size * np.sin(angle)) for angle in angles]

# The directions of all the neighbours for each cell
# The coordinate system is based on https://www.redblobgames.com/grids/hexagons/
# The Doubled Coordinates System
directions = [(0, -2), (0, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# To move the player in the a direction
# Used to move to next cell and for Trap 3
def move_in_direction(q, r, direction, steps=1):
    dq, dr = direction
    new_q, new_r = q + dq * steps, r + dr * steps
    
    # Return only if the cell is not an obstacle
    if (new_q, new_r) in maze and maze[(new_q, new_r)].cellType != CellType.OBSTACLE:
        return new_q, new_r
    return None

# Count total number of treasures in the maze
total_treasures = sum(1 for hex in maze.values() if hex.cellType == CellType.TREASURE)

def bfs_collect_all_treasures(start, maze):
    
    # (position, path, collected_treasures, last_direction, current_steps, current_energy, previous_energy, energy_multiplier)
    queue = deque([(start, [start], set(), None, 1, 1, 1, 1)]) 
    visited = set()
    
    while queue:
        (current, path, collected_treasures, last_direction, current_steps, current_energy, previous_energy, energy_multiplier) = queue.popleft()
        q, r = current
        
        # Default step to move from one cell to another is 1
        new_steps = 1
        
        # Check if node was visited
        # collected_treasured acts as a key to identify the diffrence between paths
        if (current, frozenset(collected_treasures)) in visited:
            continue
        
        visited.add((current, frozenset(collected_treasures)))
        
        hex = maze[(q, r)]
        
        # If the current hex has a treasure, add it to the collected set
        if hex.cellType == CellType.TREASURE:
            collected_treasures = collected_treasures | {current}
        elif hex.cellType == CellType.TRAP_1:
            energy_multiplier *= 2
        elif hex.cellType == CellType.TRAP_2:
            new_steps += 1
        elif hex.cellType == CellType.TRAP_4:
            continue; # Stop searching this branch
        elif hex.cellType == CellType.REWARD_1:
            energy_multiplier /= 2
        elif hex.cellType == CellType.REWARD_2:
            new_steps = 0.5
            
        # Calculate energy and steps
        new_energy = previous_energy * energy_multiplier

        current_steps += new_steps
        current_energy += new_energy
      
        # Goal check - if collected treasures same length as total treasures
        if len(collected_treasures) == total_treasures:
            return path, current_steps, current_energy
        
        # Add neighbors to the queue
        for direction in directions:
            neighbour = move_in_direction(q, r, direction)
            
            # If neighbour has not been visited
            if neighbour and (neighbour, frozenset(collected_treasures)) not in visited:
                new_q, new_r = neighbour
                new_path = path + [neighbour]
                
                # Check for Trap 3
                if maze[(new_q, new_r)].cellType == CellType.TRAP_3:
                    teleported_cell = move_in_direction(new_q, new_r, direction, steps=2)
                    
                    # If teleported cell is valid (not obstacle)
                    if teleported_cell:
                        queue.append((teleported_cell, new_path + [teleported_cell], collected_treasures, direction, current_steps, current_energy, new_energy, energy_multiplier))
                        continue
                
                queue.append((neighbour, new_path, collected_treasures, direction, current_steps, current_energy, new_energy, energy_multiplier))
    
    # If no path found
    return None, 0, 0 

start = (1, 10)
path, steps, energy = bfs_collect_all_treasures(start, maze)


plot_maze(maze, paths=[path])
print(f"Shortest path: {path}\n")
print(f"Path length: {len(path)}")
print(f"Steps Taken: {steps}")
print(f"Energy Used: {energy}")

