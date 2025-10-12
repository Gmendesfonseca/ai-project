from backend.service.base.InformedSearch import InformedSearch   
        
#--------------------------------------------------------------------------
# IMPORT DATA FROM FILE
#--------------------------------------------------------------------------
def generate_graph_problem(file_path):
    graph = []
    nodes = []
    with open(file_path,"r") as f:
        for data in f:
            data = data.strip()
            data = data.split(",")
            nodes.append(data[0])
            aux1 = []
            for i in range (1,len(data),2):
                aux=[]
                aux.append(data[i])
                aux.append(int(data[i+1]))
                aux1.append(aux)
            graph.append(aux1)
        
    return nodes, graph

#--------------------------------------------------------------------------
# MAIN MODULE
#--------------------------------------------------------------------------
# Execution - Graph
nodes, graph = generate_graph_problem("Romenia_Com_Pesos.txt")
start = "arad"
end  = "bucharest"
start = start.upper()
end  = end.upper()

origin  = tuple(map(int, input("Enter origin (x y): ").split()))
destination = tuple(map(int, input("Enter destination (x y): ").split()))

# Execute searches
sol = InformedSearch()
path = []
PATH_MSG = "Path: "
COST_MSG = "Cost: "
NOT_FOUND_MSG = "Path not found"

path, cost = sol.uniform_cost(origin,destination,nodes,graph)
print("\n===> Uniform Cost")
if path!=None:
    print(PATH_MSG,path)
    print(COST_MSG,cost)
else:
    print(NOT_FOUND_MSG)

path, cost = sol.greedy(origin,destination,nodes,graph)
print("\n===> Greedy")
if path!=None:
    print(PATH_MSG,path[::-1])
    print(COST_MSG,cost)
else:
    print(NOT_FOUND_MSG)

path, cost = sol.a_star(origin,destination,nodes,graph)
print("\n===> A Star")
if path!=None:
    print(PATH_MSG,path[::-1])
    print(COST_MSG,cost)
else:
    print(NOT_FOUND_MSG)

path, cost = sol.ida_star(origin,destination,nodes,graph)
print("\n===> IDA Star")
if path!=None:
    print(PATH_MSG,path[::-1])
    print(COST_MSG,cost)
else:
    print(NOT_FOUND_MSG)