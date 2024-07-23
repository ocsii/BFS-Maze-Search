This code executes a Breadth First Search on the Maze outlined in the image:

![image](https://github.com/user-attachments/assets/c4327714-5e03-4685-83c6-5b7963a43d3f)

The state / maze is represented with the Doubled Coordinate system with offsets on odd and even rows to maintain staggering pattern. The calcluations to plot the axes and 
angles are derived from (https://www.redblobgames.com/grids/hexagons/)

![image](https://github.com/user-attachments/assets/f318dfd9-4c1c-44f6-b99c-ec04a8f47051)


The output is the shortest path (least amount of nodes travelled to) to collect every piece of treasure in the maze. Utilises trap 3 which propels you forward
to reduce the amount of nodes travelled to utimately reducing path length.
