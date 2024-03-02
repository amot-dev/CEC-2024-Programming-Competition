import resources
from resources import Resources
import numpy as np
from collections import deque


class Node:
    def __init__(self, x, y, value, parent_path):
        self.x = x
        self.y = y
        self.value = value
        self.path = parent_path
        self.path.append([x, y])

    def __hash__(self):
        return hash((self.x, self.y))

    def calculate_value(self, res):
        self.value = res.calculate_value(self.x, self.y)



