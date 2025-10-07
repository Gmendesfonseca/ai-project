from backend.service.UninformedSearch import UninformedSearch
import numpy as np  
import random as rd

# Constants for repeated strings
PATH_MSG = "Path: "
COST_MSG = "Cost..: "
NOT_FOUND_MSG = "PATH NOT FOUND"

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
# GERA GRID ALEATÓRIO
#-----------------------------------------------------------------------------
def generate_random_grid_problem(nx,ny,qty):
    mapa = np.zeros((nx,ny),int)
    
    k = 0
    while k<qty:
        i = rd.randrange(0,nx)
        j = rd.randrange(0,ny)
        if mapa[i][j]==0:
            mapa[i][j] = 9
            k+=1
    return mapa,nx,ny
#-----------------------------------------------------------------------------
# GERA O GRID DE ARQUIVO TEXTO
#-----------------------------------------------------------------------------
def generate_fixed_grid_problem(file_path):
    file = open(file_path)
    mapa = []
    for line in file:
        aux_str = line.strip("\n")
        aux_str = aux_str.split(",")
        aux_int = [int(x) for x in aux_str]
        mapa.append(aux_int)
    nx = len(mapa)
    ny = len(mapa[0])
    return mapa,nx,ny
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
        print("\n*****BREADTH FIRST*****")
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")
  
    path = sol.depth_first(origin,destination,nodes,graph)
    print("\n*****DEPTH FIRST*****")
    if path!=None:
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")

    limit = 2
    path = sol.depth_limited(origin,destination,nodes,graph,limit)
    print("\n*****DEPTH LIMITED*****")
    if path!=None:
        print("\n*****DEPTH LIMITED*****")
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")
    
    limit = 3
    path = sol.depth_limited(origin,destination,nodes,graph,limit)
    print("\n*****DEPTH LIMITED*****")
    if path!=None:
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")
    
    limit = 4
    path = sol.depth_limited(origin,destination,nodes,graph,limit)
    print("\n*****DEPTH LIMITED*****")
    if path!=None:
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")

    max_limit = len(nodes)
    path = sol.iterative_deepening(origin,destination,nodes,graph,max_limit)
    if path!=None:
        print("\n*****ITERATIVE DEEPENING*****")
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")
        
    path = sol.bidirectional(origin,destination,nodes,graph)
    if path!=None:
        print("\n*****BIDIRECTIONAL*****")
        print("Path: ",path)
        print("Cost..: ",len(path)-1)
    else:
        print("PATH NOT FOUND")
else:
    print("Invalid initial/final state")
