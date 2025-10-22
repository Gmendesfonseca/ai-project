from backend.service.base.UninformedSearch import UninformedSearch
import numpy as np  
import random as rd

# Constants for repeated strings
PATH_MSG = "Path: "
COST_MSG = "Cost..: "
NOT_FOUND_MSG = "PATH NOT FOUND"
DEPTH_LIMITED_MSG = "*****DEPTH LIMITED*****"

#-----------------------------------------------------------------------------
# IMPORT GRAPH FROM TEXT FILE
#-----------------------------------------------------------------------------
def generate_graph_problem(file_path):
    f = open(file_path,"r")
    
    nodes = []
    graph = []
    for str1 in f:
        str1 = str1.strip("\n")
        str1 = str1.split(",")
        nodes.append(str1[0])
        graph.append(str1[1:])
    
    return nodes, graph
#-----------------------------------------------------------------------------
# MAIN PROGRAM
#-----------------------------------------------------------------------------
# Execute Graph
file_path = "Romenia_Sem_Pesos.txt"
nodes, graph = generate_graph_problem(file_path)
print("======== Node List ========\n",nodes)

origin  = input("\nOrigin......: ").upper()
destination = input("Destination.....: ").upper()

flag_origin  = origin in nodes
flag_destination = destination in nodes
flag = flag_origin and flag_destination

if flag:
    sol = UninformedSearch()
    path = []
    path = sol.breadth_first(origin,destination,nodes,graph)
    if path!=None:
        print("\n" + DEPTH_LIMITED_MSG)
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)
  
    path = sol.depth_first(origin,destination,nodes,graph)
    print("\n" + DEPTH_LIMITED_MSG)
    if path!=None:
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)

    limit = 2
    path = sol.depth_limited(origin,destination,nodes,graph,limit)
    print("\n" + DEPTH_LIMITED_MSG)
    if path!=None:
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)
    
    limit = 3
    path = sol.depth_limited(origin,destination,nodes,graph,limit)
    print("\n" + DEPTH_LIMITED_MSG)
    if path!=None:
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)
    
    limit = 4
    path = sol.depth_limited(origin,destination,nodes,graph,limit)
    print("\n" + DEPTH_LIMITED_MSG)
    if path!=None:
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)

    max_limit = len(nodes)
    path = sol.iterative_deepening(origin,destination,nodes,graph,max_limit)
    if path!=None:
        print("\n*****ITERATIVE DEEPENING*****")
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)
        
    path = sol.bidirectional(origin,destination,nodes,graph)
    if path!=None:
        print("\n*****BIDIRECTIONAL*****")
        print(PATH_MSG,path)
        print(COST_MSG,len(path)-1)
    else:
        print(NOT_FOUND_MSG)
else:
    print("Invalid initial/final state")
