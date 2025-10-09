from collections import deque
from .Node import Node
import logging

class UninformedSearch(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    #--------------------------------------------------------------------------
    # SUCCESSORS FOR GRAPH
    #--------------------------------------------------------------------------
    def successors_graph(self,idx,graph,order):
        """
        Returns the successors of a given node in the graph.

        :param idx: Index of the node in the nodes list.
        :param graph: Adjacency list representing the graph.
        :param order: Order of traversal (1 for normal, -1 for reverse).
        
        :return: List of successor nodes.
        """
        successors = []
        for suc in graph[idx][::order]:
            successors.append(suc)
        return successors
    #--------------------------------------------------------------------------    
    # SHOW PATH FOUND IN SEARCH TREE
    #--------------------------------------------------------------------------    
    def show_path(self,node):
        """
        Reconstructs the path from the start node to the given node.
        
        :param node: The end node of the path.
        
        :return: A list representing the path from start to the given node.
        """
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path
    #--------------------------------------------------------------------------    
    # REPEATED NODE CONTROL
    #--------------------------------------------------------------------------
    def show_path_bidirectional(self,meeting_point,visited1, visited2):
        """
        Reconstructs the path from start to goal given a meeting point and visited nodes from both searches.
        
        
        :param meeting_point: The node where both searches met.
        :param visited1: Visited nodes from the start side.
        :param visited2: Visited nodes from the goal side.
        
        :return: A list representing the path from start to goal.
        """
        # node from the start side
        meeting1 = visited1[meeting_point]  
        # node from the goal side
        meeting2 = visited2[meeting_point]
    
        path1 = self.show_path(meeting1)
        path2 = self.show_path(meeting2)
    
        # Reverse the path
        path2 = list(reversed(path2[:-1]))
    
        return path1 + path2
    #--------------------------------------------------------------------------
    # BREADTH-FIRST SEARCH
    #--------------------------------------------------------------------------
    def breadth_first_search(self,start,goal,nodes,graph):   # graph
        """
        Performs a breadth-first search on a graph.
        
        :param start: The starting node.
        :param goal: The goal node.
        :param nodes: List of all nodes in the graph.
        :param graph: Adjacency list representing the graph.
        
        :return: A list representing the path from start to goal, or None if no path is found.
        """
        print("nodes, graph:", nodes, graph)
        self.logger.info(f"Starting breadth-first search from {start} to {goal}")
        # Finish if start equals goal
        if start == goal:
            self.logger.info(f"Start equals goal: {start}")
            return [start]
        
        # List for search tree - QUEUE
        queue = deque()
    
        # Include start as root node of search tree
        root = Node(None,start,0,None,None)    # graph
        queue.append(root)
    
        # Mark start as visited
        visited = {start: root}           # graph
        self.logger.debug(f"Initial queue size: 1, visited nodes: {len(visited)}")
        
        while queue:
            # Remove first from QUEUE
            current = queue.popleft()
            self.logger.debug(f"Exploring node: {current.state}, depth: {current.depth}")
    
            # Generate successors from graph
            idx = nodes.index(current.state)    # graph
            children = self.successors_graph(idx, graph, 1) # graph
            self.logger.debug(f"Generated {len(children)} children for node {current.state}")
    
            for new in children:
                if new not in visited:   # graph
                    child = Node(current,new,current.depth + 1,None,None)  # graph
                    queue.append(child)
                    visited[new] = child   # graph
                    self.logger.debug(f"Added new node {new} to queue, depth: {child.depth}")
                    
                    # Check if found the goal
                    if new == goal:        # graph
                        path = self.show_path(child)
                        self.logger.info(f"Goal found! Path: {path}, steps: {len(path)-1}")
                        return path
        
        self.logger.warning("No path found from start to goal")
        return None
    #--------------------------------------------------------------------------
    # DEPTH-FIRST SEARCH
    #--------------------------------------------------------------------------
    def depth_first_search(self, start, goal, nodes, graph):
        """
        Performs a depth-first search on a graph.
        
        :param start: The starting node.
        :param goal: The goal node.
        :param nodes: List of all nodes in the graph.
        :param graph: Adjacency list representing the graph.
        
        :return: A list representing the path from start to goal, or None if no path is found.
        """
        self.logger.info(f"Starting depth-first search from {start} to {goal}")
        # Finish if start equals goal
        if start == goal:
            self.logger.info(f"Start equals goal: {start}")
            return [start]
        
        # List for search tree - STACK
        stack = deque()
    
        # Include start as root node of search tree
        root = Node(None,start,0,None,None)    # graph
        stack.append(root)
    
        # Mark start as visited
        visited = {start: root}           # graph
        self.logger.debug(f"Initial stack size: 1, visited nodes: {len(visited)}")
        
        while stack:
            # Remove last from STACK
            current = stack.pop()
            self.logger.debug(f"Exploring node: {current.state}, depth: {current.depth}")
    
            # Generate successors from graph
            idx = nodes.index(current.state)    # graph
            children = self.successors_graph(idx,graph,-1) # graph
            self.logger.debug(f"Generated {len(children)} children for node {current.state}")
    
            for new in children:
                if new not in visited:   # graph
                    child = Node(current,new,current.depth + 1,None,None)  # graph
                    stack.append(child)
                    visited[new] = child   # graph
                    self.logger.debug(f"Added new node {new} to stack, depth: {child.depth}")
                    
                    # Check if found the goal
                    if new == goal:        # graph
                        path = self.show_path(child)
                        self.logger.info(f"Goal found! Path: {path}, steps: {len(path)-1}")
                        return path
        
        self.logger.warning("No path found from start to goal")
        return None
    #--------------------------------------------------------------------------
    # DEPTH-LIMITED SEARCH
    #--------------------------------------------------------------------------
    def depth_limited_search(self,start,goal,nodes,graph,limit):
        """
        Performs a depth-limited search on a graph.

        :param start: The starting node.
        :param goal: The goal node.
        :param nodes: List of all nodes in the graph.
        :param graph: Adjacency list representing the graph.
        :param limit: The depth limit for the search.

        :return: A list representing the path from start to goal, or None if no path is found.
        """
        self.logger.info(f"Starting depth-limited search from {start} to {goal}, limit: {limit}")
        # Finish if start equals goal
        if start == goal:
            self.logger.info(f"Start equals goal: {start}")
            return [start]
        
        # List for search tree - STACK
        stack = deque()
    
        # Include start as root node of search tree
        root = Node(None,start,0,None,None)    # graph
        stack.append(root)
    
        # Mark start as visited
        visited = {start: root}           # graph
        self.logger.debug(f"Initial stack size: 1, visited nodes: {len(visited)}, depth limit: {limit}")
        
        while stack:
            # Remove last from STACK
            current = stack.pop()
            
            if current.depth<limit:
                self.logger.debug(f"Exploring node: {current.state}, depth: {current.depth} (within limit {limit})")
                # Generate successors from graph
                idx = nodes.index(current.state)    # graph
                children = self.successors_graph(idx,graph,-1) # graph
                self.logger.debug(f"Generated {len(children)} children for node {current.state}")
        
                for new in children:
                    if new not in visited:   # graph
                        child = Node(current,new,current.depth + 1,None,None)  # graph
                        stack.append(child)
                        visited[new] = child   # graph
                        self.logger.debug(f"Added new node {new} to stack, depth: {child.depth}")
                        
                        # Check if found the goal
                        if new == goal:        # graph
                            path = self.show_path(child)
                            self.logger.info(f"Goal found! Path: {path}, steps: {len(path)-1}")
                            return path
            else:
                self.logger.debug(f"Node {current.state} at depth {current.depth} exceeds limit {limit}")
        
        self.logger.warning(f"No path found within depth limit {limit}")
        return None
    #--------------------------------------------------------------------------
    # ITERATIVE DEEPENING SEARCH
    #--------------------------------------------------------------------------
    def iterative_deepening_search(self,start,goal,nodes,graph,max_limit):
        """
        Performs an iterative deepening search on a graph.
        
        :param start: The starting node.
        :param goal: The goal node.
        :param nodes: List of all nodes in the graph.
        :param graph: Adjacency list representing the graph.
        :param max_limit: The maximum depth limit for the search.

        :return: A list representing the path from start to goal, or None if no path is found.
        """
        self.logger.info(f"Starting iterative deepening search from {start} to {goal}, max limit: {max_limit}")
        for limit in range(1,max_limit):
            self.logger.info(f"Trying depth limit: {limit}")
            # Finish if start equals goal
            if start == goal:
                self.logger.info(f"Start equals goal: {start}")
                return [start]
            
            # List for search tree - STACK
            stack = deque()
        
            # Include start as root node of search tree
            root = Node(None,start,0,None,None)    # graph
            stack.append(root)
        
            # Mark start as visited
            visited = {start: root}           # graph
            
            while stack:
                # Remove last from STACK
                current = stack.pop()
                
                if current.depth<limit:
                    # Generate successors from graph
                    idx = nodes.index(current.state)    # graph
                    children = self.successors_graph(idx,graph,-1) # graph
            
                    for new in children:
                        if new not in visited:   # graph
                            child = Node(current,new,current.depth + 1,None,None)  # graph
                            stack.append(child)
                            visited[new] = child   # graph
                            
                            # Check if found the goal
                            if new == goal:        # graph
                                path = self.show_path(child)
                                self.logger.info(f"Goal found at depth limit {limit}! Path: {path}, steps: {len(path)-1}")
                                return path
        
        self.logger.warning(f"No path found within max depth limit {max_limit}")
        return None
    #--------------------------------------------------------------------------
    # BIDIRECTIONAL SEARCH
    #--------------------------------------------------------------------------
    def bidirectional_search(self, start, goal, nodes, graph):
        """
        Performs a bidirectional search on a graph.
        
        :param start: The starting node.
        :param goal: The goal node.
        :param nodes: List of all nodes in the graph.
        :param graph: Adjacency list representing the graph.

        :return: A list representing the path from start to goal, or None if no path is found.
        """
        self.logger.info(f"Starting bidirectional search from {start} to {goal}")
        if start == goal:
            self.logger.info(f"Start equals goal: {start}")
            return [start]

        # List for search tree from origin - QUEUE
        queue1 = deque()
        
        # List for search tree from destination - QUEUE
        queue2 = deque()  
        
        # Include start and goal as root nodes of search tree
        root = Node(None,start,0,None,None)    # graph
        queue1.append(root)
        root = Node(None,goal,0,None,None)    # graph
        queue2.append(root)
    
        # Visited mapping state -> Node (to reconstruct path)
        visited1 = {start: queue1[0]}
        visited2 = {goal:    queue2[0]}
        
        level = 0
        self.logger.debug("Initial setup: forward queue size: 1, backward queue size: 1")
    
        while queue1 and queue2:
            
            # ****** Execute BREADTH-FIRST from START *******
            # Number of nodes in current level
            level = len(queue1)  
            for _ in range(level):
                # Remove first from QUEUE
                current = queue1.popleft()

                # Generate successors
                idx = nodes.index(current.state)
                children = self.successors_graph(idx, graph, 1)

                for new in children:
                    if new not in visited1:
                        child = Node(current,new,current.depth + 1,None, None)
                        visited1[new] = child

                        # Found meeting point with other BREADTH-FIRST
                        if new in visited2:
                            path = self.show_path_bidirectional(new, visited1, visited2)
                            self.logger.info(f"Meeting point found at {new}! Path: {path}, steps: {len(path)-1}")
                            return path

                        # Insert in QUEUE
                        queue1.append(child)
            
            # ****** Execute BREADTH-FIRST from GOAL *******
            # Number of nodes in current level
            level = len(queue2)  
            for _ in range(level):
                # Remove first from QUEUE
                current = queue2.popleft()

                # Generate successors
                idx = nodes.index(current.state)
                children = self.successors_graph(idx, graph, 1)

                for new in children:
                    if new not in visited2:
                        child = Node(current,new,current.depth + 1,None, None)
                        visited2[new] = child

                        # Found meeting point with other BREADTH-FIRST
                        if new in visited1:
                            path = self.show_path_bidirectional(new, visited1, visited2)
                            self.logger.info(f"Meeting point found at {new}! Path: {path}, steps: {len(path)-1}")
                            return path

                        # Insert in QUEUE
                        queue2.append(child)
        
        self.logger.warning("No path found in bidirectional search")
        return None
