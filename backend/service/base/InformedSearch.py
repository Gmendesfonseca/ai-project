from collections import deque
from .NodeP import NodeP
import logging

class InformedSearch(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    # -------------------------------------------------------------------------
    # SUCCESSORS FOR GRAPH
    # -------------------------------------------------------------------------
    def graph_successors(self, index, graph, step=1):
        """
        Return successors for node at index in graph. The graph is expected to
        be an adjacency list where graph[index] is an iterable of (neighbor, cost)
        tuples. step controls slicing direction in case the original data was reversed.
        """
        return [s for s in graph[index][::step]]

    # -------------------------------------------------------------------------
    # INSERT IN LIST KEEPING IT ORDERED
    # -------------------------------------------------------------------------
    def insert_ordered(self, list_nodes, node):
        """
        Insert node into list_nodes keeping it ordered by node.v1 (priority).
        """
        for i, n in enumerate(list_nodes):
            if node.v1 < n.v1:
                list_nodes.insert(i, node)
                break
        else:
            list_nodes.append(node)

    # -------------------------------------------------------------------------
    # DISPLAY THE PATH FOUND IN THE SEARCH TREE
    # -------------------------------------------------------------------------
    def display_path(self, node):
        """
        Reconstruct the path from the start node to the given node.
        """
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    # -------------------------------------------------------------------------
    # GRAPH HEURISTIC (precomputed table)
    # -------------------------------------------------------------------------
    def graph_heuristic(self, nodes, destination, n):
        """
        Return the heuristic cost from node n to the destination.
        """
        i_destination = nodes.index(destination)
        i_n = nodes.index(n)
        h = [
            [0, 97, 59, 100, 53, 71, 66, 72, 91, 70, 74, 58, 62, 88, 70, 77, 67, 50, 93, 70],
            [70, 0, 80, 70, 62, 80, 97, 87, 100, 64, 57, 67, 72, 96, 72, 86, 84, 76, 54, 98],
            [78, 92, 0, 66, 50, 99, 71, 99, 56, 77, 52, 55, 64, 96, 96, 97, 72, 86, 91, 95],
            [69, 70, 99, 0, 68, 82, 85, 53, 60, 88, 64, 79, 78, 75, 96, 58, 92, 58, 73, 72],
            [83, 64, 83, 100, 0, 84, 99, 82, 86, 98, 56, 84, 83, 70, 76, 57, 51, 62, 95, 91],
            [88, 96, 73, 77, 83, 0, 87, 95, 50, 50, 78, 59, 52, 97, 88, 95, 84, 99, 77, 90],
            [56, 52, 73, 64, 97, 70, 0, 58, 69, 58, 95, 94, 89, 72, 53, 70, 96, 89, 75, 83],
            [51, 64, 93, 67, 67, 63, 88, 0, 93, 52, 97, 52, 100, 71, 87, 78, 55, 99, 69, 90],
            [84, 75, 90, 89, 62, 95, 91, 81, 0, 88, 60, 55, 71, 70, 82, 55, 90, 85, 63, 100],
            [82, 72, 69, 92, 52, 98, 61, 62, 100, 0, 87, 68, 63, 63, 73, 99, 75, 93, 91, 85],
            [94, 55, 100, 57, 77, 59, 62, 92, 86, 98, 0, 85, 67, 75, 87, 75, 84, 64, 79, 74],
            [85, 69, 84, 84, 55, 65, 56, 92, 54, 99, 98, 0, 99, 90, 68, 77, 86, 59, 75, 98],
            [92, 76, 77, 85, 51, 76, 88, 55, 75, 73, 60, 92, 0, 85, 80, 93, 82, 96, 66, 98],
            [92, 95, 65, 57, 90, 96, 73, 94, 96, 66, 75, 82, 50, 0, 87, 52, 70, 100, 61, 73],
            [88, 95, 76, 56, 72, 86, 59, 100, 85, 88, 58, 100, 98, 74, 0, 77, 91, 75, 79, 89],
            [95, 74, 96, 62, 95, 93, 66, 98, 70, 66, 61, 59, 70, 82, 92, 0, 77, 67, 90, 52],
            [63, 68, 83, 99, 61, 96, 81, 59, 83, 76, 86, 77, 94, 51, 74, 100, 0, 100, 85, 65],
            [54, 60, 65, 52, 68, 51, 91, 66, 89, 93, 87, 86, 75, 63, 64, 67, 82, 0, 60, 55],
            [51, 93, 100, 96, 57, 83, 50, 55, 59, 79, 81, 71, 76, 56, 93, 70, 93, 78, 0, 76],
            [83, 73, 53, 51, 95, 93, 93, 59, 90, 78, 70, 55, 71, 52, 84, 92, 91, 78, 88, 0],
        ]
        return h[i_destination][i_n]
    # -------------------------------------------------------------------------
    # UNIFORM COST
    # -------------------------------------------------------------------------
    def uniform_cost(self, start, goal, nodes, graph):
        """
        Uniform-cost search (Dijkstra-like) where NodeP.v2 stores the g-cost.
        """
        if start == goal:
            return [start]

        queue = deque()
        root = NodeP(None, start, 0, None, None, 0)
        queue.append(root)

        visited = {start: root}

        while queue:
            current = queue.popleft()
            current_g = current.v2

            if current.state == goal:
                return self.display_path(current), current.v2

            idx = nodes.index(current.state)
            children = self.graph_successors(idx, graph, 1)

            for child in children:
                g_cost = current_g + child[1]
                f_cost = g_cost

                if (child[0] not in visited) or (g_cost < visited[child[0]].v2):
                    new_node = NodeP(current, child[0], f_cost, None, None, g_cost)
                    visited[child[0]] = new_node
                    self.insert_ordered(queue, new_node)
        return None

    # -------------------------------------------------------------------------
    # GREEDY BEST-FIRST SEARCH
    # -------------------------------------------------------------------------
    def greedy(self, start, goal, nodes, graph):
        """
        Greedy best-first search (GBFS) where the priority is given by the heuristic.
        """
        if start == goal:
            return [start]

        queue = deque()
        root = NodeP(None, start, 0, None, None, 0)
        queue.append(root)

        visited = {start: root}

        while queue:
            current = queue.popleft()
            current_g = current.v2

            if current.state == goal:
                return self.display_path(current), current.v2

            idx = nodes.index(current.state)
            children = self.graph_successors(idx, graph, 1)

            for child in children:
                g_cost = current_g + child[1]
                f_cost = self.graph_heuristic(nodes, child[0], goal)

                if (child[0] not in visited) or (g_cost < visited[child[0]].v2):
                    new_node = NodeP(current, child[0], f_cost, None, None, g_cost)
                    visited[child[0]] = new_node
                    self.insert_ordered(queue, new_node)
        return None

    # -------------------------------------------------------------------------
    # A* SEARCH
    # -------------------------------------------------------------------------
    def a_star(self, start, goal, nodes, graph):
        """
        A* search where NodeP.v1 = g + h and NodeP.v2 = g.
        """
        if start == goal:
            return [start]

        queue = deque()
        root = NodeP(None, start, 0, None, None, 0)
        queue.append(root)

        visited = {start: root}

        while queue:
            current = queue.popleft()
            current_g = current.v2

            if current.state == goal:
                return self.display_path(current), current.v2

            idx = nodes.index(current.state)
            children = self.graph_successors(idx, graph, 1)

            for child in children:
                g_cost = current_g + child[1]
                f_cost = g_cost + self.graph_heuristic(nodes, child[0], goal)

                if (child[0] not in visited) or (g_cost < visited[child[0]].v2):
                    new_node = NodeP(current, child[0], f_cost, None, None, g_cost)
                    visited[child[0]] = new_node
                    self.insert_ordered(queue, new_node)
        return None

    # -------------------------------------------------------------------------
    # IDA* (iterative deepening A*)
    # -------------------------------------------------------------------------
    def ida_star(self, start, goal, nodes, graph):
        """
        Iterative Deepening A* (IDA*) search where the depth limit is increased
        until a solution is found.
        """
        if start == goal:
            return [start]

        bound = self.graph_heuristic(nodes, start, goal)

        while True:
            over_bound = []

            queue = deque()
            root = NodeP(None, start, 0, None, None, 0)
            queue.append(root)

            visited = {start: root}

            while queue:
                current = queue.popleft()
                current_g = current.v2

                if current.state == goal:
                    return self.display_path(current), current.v2

                idx = nodes.index(current.state)
                children = self.graph_successors(idx, graph, 1)

                for child in children:
                    g_cost = current_g + child[1]
                    f_cost = g_cost + self.graph_heuristic(nodes, child[0], goal)

                    if f_cost <= bound:
                        if (child[0] not in visited) or (g_cost < visited[child[0]].v2):
                            new_node = NodeP(current, child[0], f_cost, None, None, g_cost)
                            visited[child[0]] = new_node
                            self.insert_ordered(queue, new_node)
                    else:
                        over_bound.append(f_cost)

            if not over_bound:
                return None

            bound = sum(over_bound) / len(over_bound)