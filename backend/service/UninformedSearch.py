from collections import deque
from .Node import Node

class UninformedSearch(object):
    #--------------------------------------------------------------------------
    # SUCCESSORS FOR GRAPH
    #--------------------------------------------------------------------------
    def successors_graph(self,idx,graph,order):
        
        successors = []
        for suc in graph[idx][::order]:
            successors.append(suc)
        return successors
    #--------------------------------------------------------------------------
    # SUCCESSORS FOR GRID
    #--------------------------------------------------------------------------
    # SUCCESSORS FOR GRID (ADJACENCY LIST)
    def successors_grid(self,state,nx,ny,grid):
        successors = []
        x, y = state[0], state[1]
        # RIGHT
        if y+1<ny:
            if grid[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                successors.append(suc)
        # LEFT
        if y-1>=0:
            if grid[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                successors.append(suc)
        # DOWN
        if x+1<nx:
            if grid[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                successors.append(suc)
        # UP
        if x-1>=0:
            if grid[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                successors.append(suc)
        
        return successors
    #--------------------------------------------------------------------------    
    # SHOW PATH FOUND IN SEARCH TREE
    #--------------------------------------------------------------------------    
    def show_path(self,node):
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
        # Finish if start equals goal
        if start == goal:
            return [start]
        
        # List for search tree - QUEUE
        queue = deque()
    
        # Include start as root node of search tree
        root = Node(None,start,0,None,None)    # graph
        queue.append(root)
    
        # Mark start as visited
        visited = {start: root}           # graph
        
        while queue:
            # Remove first from QUEUE
            current = queue.popleft()
    
            # Generate successors from graph
            idx = nodes.index(current.state)    # graph
            children = self.successors_graph(idx, graph, 1) # graph
    
            for new in children:
                if new not in visited:   # graph
                    child = Node(current,new,current.depth + 1,None,None)  # graph
                    queue.append(child)
                    visited[new] = child   # graph
                    
                    # Check if found the goal
                    if new == goal:        # graph
                        return self.show_path(child)
        return None
    #--------------------------------------------------------------------------
    # DEPTH-FIRST SEARCH
    #--------------------------------------------------------------------------
    def depth_first_search(self, start, goal, nodes, graph):
        # Finish if start equals goal
        if start == goal:
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
                        return self.show_path(child)
        return None
    #--------------------------------------------------------------------------
    # DEPTH-LIMITED SEARCH
    #--------------------------------------------------------------------------
    def depth_limited_search(self,start,goal,nodes,graph,limit):
        # Finish if start equals goal
        if start == goal:
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
                            return self.show_path(child)
        return None
    #--------------------------------------------------------------------------
    # ITERATIVE DEEPENING SEARCH
    #--------------------------------------------------------------------------
    def iterative_deepening_search(self,start,goal,nodes,graph,max_limit):
        for limit in range(1,max_limit):
            # Finish if start equals goal
            if start == goal:
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
                                return self.show_path(child)
        return None
    #--------------------------------------------------------------------------
    # BIDIRECTIONAL SEARCH
    #--------------------------------------------------------------------------
    def bidirectional_search(self, start, goal, nodes, graph):
        if start == goal:
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
                            return self.show_path_bidirectional(new, visited1, visited2)

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
                            return self.show_path_bidirectional(new, visited1, visited2)

                        # Insert in QUEUE
                        queue2.append(child)
        return None
