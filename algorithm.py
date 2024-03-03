from resources import Resources
import numpy as np
from collections import deque
import heapq


class Algorithm:
    def __init__(self, num_best_nodes_considered=3, days_to_look_ahead=1):
        self.world_state = [Resources(i) for i in range(1, 31)]
        self.top_n = num_best_nodes_considered
        self.depth = days_to_look_ahead

    def run_algorithm(self, days_to_look_ahead):
        start_node = self.find_best_start()
        for current_day in range(1, 31):
            end_day = current_day + days_to_look_ahead
            if end_day > 30:
                end_day = 30
            end_node = self.regional_search(start_node, current_day, end_day)

    '''
    Finds the optimal start position
    '''

    def find_best_start(self):
        return Node(0, 0, -1, list())

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
        resources_today = self.world_state[day]
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
                    heapq.heappush(best_nodes, (node.value, node))
                elif best_nodes[0][0] < node.value:
                    heapq.heappop(best_nodes)
                    heapq.heappush(best_nodes, (node.value, node))
                explored.add(node)
        return best_nodes

    # def local_search(self, node, day):
    #     best_nodes = []
    #     q = deque()
    #     seen = set()
    #     q.append(node)
    #     while q:
    #         curr_node = q.popleft()
    #         if (curr_node.x, curr_node.y) in seen:
    #             continue
    #         elif self.world_state[day].world[curr_node.x][curr_node.y] == 1:
    #             continue
    #         elif curr_node.x < 0 or curr_node.y >= 100: # out of bounds
    #             continue
    #         elif curr_node.x > node.x + 5 or curr_node < node.x - 5:
    #             continue
    #         elif curr_node.y > node.y + 5 or curr_node.y < node.y - 5:
    #             continue
    #         else:
    #             seen.add((curr_node.x, curr_node.y))
    #             if len(best_nodes) < self.top_n:
    #                 heapq.heappush()
    #
    #             q.append(Node(x=curr_node.x + 1, y=curr_node.y + 1, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x + 1, y=curr_node.y + 0, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x + 1, y=curr_node.y - 1, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x + 0, y=curr_node.y + 1, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x + 0, y=curr_node.y - 1, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x - 1, y=curr_node.y + 1, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x - 1, y=curr_node.y + 0, parent_path=curr_node.path))
    #             q.append(Node(x=curr_node.x - 1, y=curr_node.y - 1, parent_path=curr_node.path))
    #     return list()

    '''
    Searches in the area reachable in N days
    start is a Node that represents the start of the search
    day is the day the search is performed on
    '''

    def regional_search(self, start_node, start_day, end_day):
        # Run search on the first day
        max_value = 0
        max_node = None

        candidate_list = self.local_search(start_node, start_day)
        candidate_list.sort(key=lambda node: node.value)
        best_candidate = candidate_list[-1]

        if start_day == end_day:
            return best_candidate

        for candidate_node in candidate_list:
            next_node = self.regional_search(candidate_node, start_day + 1, end_day)
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
