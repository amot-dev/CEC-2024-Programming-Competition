import tkinter as tk
from resources import Resources
import numpy as np
from collections import deque

class Algorithm:
    def __init__(self, top_n=1, depth=1):
        self.world_state = [Resources(i) for i in range(1, 31)]
        self.top_n = top_n
        self.depth = depth

    def find_best(self, node, n):
        q = deque()
        q.append(node)
        while q:
            curr_node = q.popleft()

        pass

    def search_init(self):
        nodes = []
        for iy, ix in np.ndindex(self.world_state[0].world.shape):
            if self.world_state[0].world[ix][iy] == 0: # Find all nodes that are not land.
                nodes.append(Node(x=ix, y=iy, parent_path=[]))
        self.search_nodes(nodes=nodes, depth=0, day=0) # Start searching through nodes that we can look at.

    def search_nodes(self, nodes, depth):
        best_nodes = []
        if depth == 0:
            return min(nodes, key=lambda node: -abs(self.world_state[day].endangered_species[node.x][node.y])
                + abs(self.world_state[day].oil[node.x][node.y])
                - abs(self.world_state[day].coral_reef[node.x][node.y])
                - abs(self.world_state[day].helium[node.x][node.y])
                + abs(self.world_state[day].metals[node.x][node.y])
                + abs(self.world_state[day].ships[node.x][node.y])
            )
        for node in nodes:
            best_node = self.find_best(node)






class Node:
    def __init__(self, x, y, parent_path):
        self.x = x
        self.y = y
        self.path = parent_path
        self.path.append([x, y])
