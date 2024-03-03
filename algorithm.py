from resources import Resources
from collections import deque
import heatmap


class Algorithm:
    def __init__(self, num_best_nodes_considered=3, days_to_look_ahead=1):
        self.world_state = [Resources(i) for i in range(1, 31)]
        self.top_n = num_best_nodes_considered
        self.depth = days_to_look_ahead

    def run_algorithm(self, days_to_look_ahead):
        start_node = self.find_best_start()
        moves = list()
        for current_day in range(1, 31):
            moves_today = list()
            end_day = current_day + days_to_look_ahead
            if end_day > 30:
                end_day = 30
            start_node = self.regional_search(start_node, current_day, end_day)
            moves_today.append(start_node.path)
            moves.append(moves_today)
        stop_color = "yellow"
        moving_color = "white"
        path = moves, stop_color, moving_color
        heatmap.rig_paths.append(path)

    '''
    Finds the optimal start position
    '''

    def find_best_start(self):
        return Node(2, 2, -1, list())

    '''
    Returns a list of valid moves from the current node on the current day
    '''

    def valid_moves(self, node, day):
        x = node.x
        y = node.y
        world = self.world_state[day].world
        moves = list()
        for xi in range(x - 1, x + 1):
            for yi in range(y - 1, x + 1):
                try:
                    if world[xi, yi] == 0:
                        moves.append(Node(xi, yi, -1, node.path))
                except:
                    pass
        return moves

    '''
    Searches in the area reachable inbetween days
    start is a Node that represents the start of the search
    day is the day the search is performed on
    '''

    def local_search(self, start_node, day):
        resources_today = self.world_state[day - 1]
        best_nodes = []
        queue = deque()
        explored = set()
        queue.append(start_node)
        while len(queue):
            node = queue.pop()
            # Only keep searching if length of path is 5 or less (includes current position)
            if len(node.path) <= 5:
                for move in self.valid_moves(node, day):
                    queue.append(move)
                node.calculate_value(resources_today)
                if len(best_nodes) < self.top_n:
                    best_nodes.append(node)
                elif best_nodes[0][0] < node.value:
                    min_object = min(best_nodes, key=lambda n: n.value)
                    best_nodes.remove(min_object)
                explored.add(node)
        return best_nodes

    '''
    Searches in the area reachable in N days
    start is a Node that represents the start of the search
    day is the day the search is performed on
    '''

    def regional_search(self, start_node, start_day, end_day):
        # Run search on the first day
        max_value = 0
        max_node = None
        best_candidate = None

        candidate_list = self.local_search(start_node, start_day)
        candidate_list.sort(key=lambda node: node.value)
        if candidate_list:
            best_candidate = candidate_list[-1]

        if start_day == end_day:
            return best_candidate

        for candidate_node in candidate_list:
            next_node = self.regional_search(candidate_node, start_day + 1, end_day)
            if next_node:
                candidate_node.value += next_node.value
        for candidate_node in candidate_list:
            if candidate_node.value > max_value:
                max_value = candidate_node.value
                max_node = candidate_node
        return max_node


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
