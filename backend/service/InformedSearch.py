from collections import deque
from NodeP import NodeP
from math import sqrt

class InformedSearch(object):
#--------------------------------------------------------------------------
# SUCCESSORS FOR GRAPH
#--------------------------------------------------------------------------
    def graph_successors(self,ind,graph,order):
        
        f = []
        for suc in graph[ind][::order]:
            f.append(suc)
        return f
    
#--------------------------------------------------------------------------
# SUCCESSORS FOR GRID
#--------------------------------------------------------------------------
    def grid_successors(self,st,nx,ny,map_grid):
        f = []
        x, y = st[0], st[1]
        # RIGHT
        if y+1<ny and map_grid[x][y+1]==0:
            suc = [x, y+1]
            cost = 5
            f.append([suc, cost])
        # LEFT
        if y-1>=0 and map_grid[x][y-1]==0:
            suc = [x, y-1]
            cost = 7
            f.append([suc, cost])
        # DOWN
        if x+1<nx and map_grid[x+1][y]==0:
            suc = [x+1, y]
            cost = 2
            f.append([suc, cost])
        # UP
        if x-1>=0 and map_grid[x-1][y]==0:
            suc = [x-1, y]
            cost = 3
            f.append([suc, cost])        
        return f
#--------------------------------------------------------------------------    
# INSERT IN LIST KEEPING IT ORDERED
#--------------------------------------------------------------------------    
    def insert_ordered(self,list_nodes, node):
        for i, n in enumerate(list_nodes):
            if node.v1 < n.v1:
                list_nodes.insert(i, node)
                break
        else:
            list_nodes.append(node)
#--------------------------------------------------------------------------    
# DISPLAY THE PATH FOUND IN THE SEARCH TREE
#--------------------------------------------------------------------------    
    def display_path(self,node):
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path
#--------------------------------------------------------------------------    
# GENERATE H RANDOMLY - GRAPH
#--------------------------------------------------------------------------    
    def graph_heuristic(self,nodes,destination,n):
        i_destination = nodes.index(destination)
        i_n = nodes.index(n)
        h = [
             [0,97,59,100,53,71,66,72,91,70,74,58,62,88,70,77,67,50,93,70],
             [70,0,80,70,62,80,97,87,100,64,57,67,72,96,72,86,84,76,54,98],
             [78,92,0,66,50,99,71,99,56,77,52,55,64,96,96,97,72,86,91,95],
             [69,70,99,0,68,82,85,53,60,88,64,79,78,75,96,58,92,58,73,72],
             [83,64,83,100,0,84,99,82,86,98,56,84,83,70,76,57,51,62,95,91],
             [88,96,73,77,83,0,87,95,50,50,78,59,52,97,88,95,84,99,77,90],
             [56,52,73,64,97,70,0,58,69,58,95,94,89,72,53,70,96,89,75,83],
             [51,64,93,67,67,63,88,0,93,52,97,52,100,71,87,78,55,99,69,90],
             [84,75,90,89,62,95,91,81,0,88,60,55,71,70,82,55,90,85,63,100],
             [82,72,69,92,52,98,61,62,100,0,87,68,63,63,73,99,75,93,91,85],
             [94,55,100,57,77,59,62,92,86,98,0,85,67,75,87,75,84,64,79,74],
             [85,69,84,84,55,65,56,92,54,99,98,0,99,90,68,77,86,59,75,98],
             [92,76,77,85,51,76,88,55,75,73,60,92,0,85,80,93,82,96,66,98],
             [92,95,65,57,90,96,73,94,96,66,75,82,50,0,87,52,70,100,61,73],
             [88,95,76,56,72,86,59,100,85,88,58,100,98,74,0,77,91,75,79,89],
             [95,74,96,62,95,93,66,98,70,66,61,59,70,82,92,0,77,67,90,52],
             [63,68,83,99,61,96,81,59,83,76,86,77,94,51,74,100,0,100,85,65],
             [54,60,65,52,68,51,91,66,89,93,87,86,75,63,64,67,82,0,60,55],
             [51,93,100,96,57,83,50,55,59,79,81,71,76,56,93,70,93,78,0,76],
             [83,73,53,51,95,93,93,59,90,78,70,55,71,52,84,92,91,78,88,0]
             ]
        return h[i_destination][i_n]
#--------------------------------------------------------------------------    
# GENERATE H - GRID
#--------------------------------------------------------------------------    
    def grid_heuristic(self,p1,p2):
        if (p2[0]-p1[0])<0:
            c1 = 3
        else:
            c1 = 2
        if (p2[1]-p1[1])<0:
            c2 = 7
        else:
            c2 = 5
        h = sqrt(c1*(p1[0]-p2[0])*(p1[0]-p2[0]) + c2*(p1[1]-p2[1])*(p1[1]-p2[1]))
        return h
# -----------------------------------------------------------------------------
# UNIFORM COST
# -----------------------------------------------------------------------------
    def uniform_cost(self,start,end,map_grid,nx,ny): # grid
        # Origin equals destination
        if start == end:
            return [start]
        
        # Priority queue based on deque + ordered insertion
        node_list = deque()
        t_start = tuple(start)   # grid
        root = NodeP(None, t_start,0, None, None, 0)  # grid
        node_list.append(root)
    
        # Control of visited nodes
        visited = {tuple(start): root}    # grid
        
        # search loop
        while node_list:
            # remove first node
            current = node_list.popleft()
            current_value = current.v2
    
            # Reached the goal
            if current.state == end:
                path = self.display_path(current)
                return path, current.v2
    
            # Generate successors - grid
            children = self.grid_successors(current.state,nx,ny,map_grid) # grid
    
            for new in children: # grid
                # accumulated cost to successor
                v2 = current_value + new[1]
                v1 = v2 
    
                # Not visited or better cost
                t_new = tuple(new[0])       # grid
                if (t_new not in visited) or (v2<visited[t_new].v2): # grid
                    child = NodeP(current,t_new, v1, None, None, v2) # grid
                    visited[t_new] = child # grid
                    self.insert_ordered(node_list, child)
        return None
# -----------------------------------------------------------------------------
# GREEDY
# -----------------------------------------------------------------------------
    def greedy(self,start,end,map_grid,nx,ny): # grid
        # Origin equals destination
        if start == end:
            return [start]
        
        # Priority queue based on deque + ordered insertion
        node_list = deque()
        t_start = tuple(start)   # grid
        root = NodeP(None, t_start,0, None, None, 0)  # grid
        node_list.append(root)
    
        # Control of visited nodes
        visited = {tuple(start): root}    # grid
        
        # search loop
        while node_list:
            # remove first node
            current = node_list.popleft()
            current_value = current.v2
    
            # Reached the goal
            if current.state == end:
                path = self.display_path(current)
                return path, current.v2
    
            # Generate successors - grid
            children = self.grid_successors(current.state,nx,ny,map_grid) # grid
    
            for new in children: # grid
                # accumulated cost to successor
                v2 = current_value + new[1]
                v1 = self.grid_heuristic(new[0],end)  
    
                # Not visited or better cost
                t_new = tuple(new[0])       # grid
                if (t_new not in visited) or (v2<visited[t_new].v2): # grid
                    child = NodeP(current,t_new, v1, None, None, v2) # grid
                    visited[t_new] = child # grid
                    self.insert_ordered(node_list, child)
        return None
# -----------------------------------------------------------------------------
# A STAR
# -----------------------------------------------------------------------------
    def a_star(self,start,end,map_grid,nx,ny): # grid
        # Origin equals destination
        if start == end:
            return [start]
        
        # Priority queue based on deque + ordered insertion
        node_list = deque()
        t_start = tuple(start)   # grid
        root = NodeP(None, t_start,0, None, None, 0)  # grid
        node_list.append(root)
    
        # Control of visited nodes
        visited = {tuple(start): root}    # grid
        
        # search loop
        while node_list:
            # remove first node
            current = node_list.popleft()
            current_value = current.v2
    
            # Reached the goal
            if current.state == end:
                path = self.display_path(current)
                return path, current.v2
    
            # Generate successors - grid
            children = self.grid_successors(current.state,nx,ny,map_grid) # grid
    
            for new in children: # grid
                # accumulated cost to successor
                v2 = current_value + new[1]
                v1 = v2 + self.grid_heuristic(new[0],end)  
    
                # Not visited or better cost
                t_new = tuple(new[0])       # grid
                if (t_new not in visited) or (v2<visited[t_new].v2): # grid
                    child = NodeP(current,t_new, v1, None, None, v2) # grid
                    visited[t_new] = child # grid
                    self.insert_ordered(node_list, child)
        return None
# -----------------------------------------------------------------------------
# IDA STAR
# -----------------------------------------------------------------------------       
    def ida_star(self,start,end,map_grid,nx,ny): # grid
        # Origin equals destination
        if start == end:
            return [start]
        
        limit = self.grid_heuristic(start,end)
        
        # Priority queue based on deque + ordered insertion
        node_list = deque()
        
        # Iterative search
        while True:
            above_limit = []
            
            t_start = tuple(start)   # grid
            root = NodeP(None, t_start,0, None, None, 0)  # grid
            node_list.append(root)
        
            # Control of visited nodes
            visited = {tuple(start): root}    # grid
            
            # search loop
            while node_list:
                # remove first node
                current = node_list.popleft()
                current_value = current.v2
        
                # Reached the goal
                if current.state == end:
                    path = self.display_path(current)
                    return path, current.v2
        
                # Generate successors - grid
                children = self.grid_successors(current.state,nx,ny,map_grid) # grid
        
                for new in children: # grid
                    # accumulated cost to successor
                    v2 = current_value + new[1]
                    v1 = v2 + self.grid_heuristic(new[0],end)  
                
                    # Check if within limit
                    if v1<=limit:
                        # Not visited or better cost
                        t_new = tuple(new[0])       # grid
                        if (t_new not in visited) or (v2<visited[t_new].v2): # grid
                            child = NodeP(current,t_new, v1, None, None, v2) # grid
                            visited[t_new] = child # grid
                            self.insert_ordered(node_list, child)
                    else:
                        above_limit.append(v1)
            
            if not above_limit:
                return None
            limit = min(above_limit)
            node_list.clear()
            visited.clear()
                        
        return None