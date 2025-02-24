from Node import Node




# returns a list of each node in the graph. organized by desc degree score
def getDegreeList(graph: list[Node]):
    # (Node, centrality score)
    degrees = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        degrees[i] = (node, len(node.connections))
    
    print(f"Degree: {degrees}\n")
    tup = sortTupleInList(degrees.copy())
    return tup

# returns a list of each node in the graph. organized by desc betweeness score
def getBetweenessList(graph: list[Node]):
    # (Node, betweeness score)
    betweeness = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        # print(f"{i} {node}")
        betweeness[i] = (node, calculateBetweeness(node, graph))

    print(f"betweeness: {betweeness}\n")
    tup = sortTupleInList(betweeness.copy())
    return tup

# returns a list of each node in the graph. organized by desc closeness score
def getClosenessList(graph: list[Node]):
    # (Node, centrality score)
    closeness = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        closeness[i] = (node, calculateCloseness(node, graph))
    
    print(f"Closeness: {closeness}\n")
    tup = sortTupleInList(closeness.copy())
    return tup

def getClusteringList(graph: list[Node], isDirected:bool):
    # (Node, centrality score)
    clustering = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        clustering[i] = (node, calculateClustering(node, graph, isDirected))
    
    print(f"Clustering: {clustering}\n")
    tup = sortTupleInList(clustering.copy())
    return tup

def calculateClustering(node: Node, graph: list[int], isDirected: bool):
    graphCopy: list[Node] = graph.copy()
    # Outbound neighbors... if undirected then thats all the neighbors
    neighbors = set(node.connections.keys())
    # Count the inbound neighbors
    if isDirected:
        for n in graphCopy:
            if(node in n.connections):
                neighbors.add(n)

    k = len(neighbors) 
    if k < 2:
        return 0.0  
    
    T = count_triangles(graphCopy, node, isDirected)
    print(f"{T=} {k=}")
    denominator = k * (k - 1) if isDirected else (k * (k - 1)) / 2
    return T / denominator

def count_triangles(graphCopy: list[Node], node: Node, isDirected: bool) -> int:
    neighbors = set(node.connections.keys())  # Outgoing neighbors
    if isDirected:
        # Incoming neighbors
        for n in graphCopy:
            if(node in n.connections):
                neighbors.add(n)

    # triangle_count = sum(1 for v in neighbors for w in neighbors if v != w and w in v.connections)

    triangleCount = 0
    print(f"{neighbors=}")
    for v in neighbors:
        for w in neighbors:
            # since v and w are already neigbors, lets check if there is a connection between the 2, then we know that there is a triangle
            if(v != w and (w in v.connections or v in w.connections)):
                triangleCount += 1

    
    return triangleCount if isDirected else triangleCount / 2  # Avoid double counting in undirected graphs

# Closeness = numberOfReachableNodes/sum(minumumpaths)
def calculateCloseness(node, graph):
    allPaths = [bfs(node, n) for n in graph if n is not node]
    # print(node.name)
    # print(allPaths)
     # go through each pair of nodes, (node, u) and finds the min cost, path is all of the paths from node to any other u
    total = 0
    count = len(graph)-1
    for i, path in enumerate(allPaths):
        # print(path)
        # If we can't get to one of the nodes wew must remove it from the total nodes
        if(not path):
            count -= 1
            continue
        # p is every path from node to u, so we get them
        minCost = float('inf')
        for p in path:
            minCost = min(minCost, calculateCost(p))
        
        total += minCost if minCost != float('inf') else 0
    closeness = (count)/total if total != 0 else 0
    # print(closeness)
    return closeness


def calculateBetweeness(node, graph):
    # print(allPaths[0])
    allPaths = getAllPathsThroughNode(node, graph)
    # go through each pair of nodes and finds the min cost
    betweenness = 0
    for i in range(len(allPaths)):
        costs = []
        # Calculates the cost of each path from i, j... We do not really know what i and j are haha
        for path in allPaths[i]:
            costs.append(calculateCost(path))
        
        # print(f"{costs=}")
        # Keep all the minimum paths
        minCost = min(costs) if costs else 0
        for j in range(len(allPaths[i])- 1, -1, -1):  
            if(costs[j] != minCost):
                allPaths[i].pop(j)
                costs.pop(j)

        numberOfPaths = len(allPaths[i])
        numberOfPathsThroughNode = 0
        for path in allPaths[i]:
            if(node in path):
                numberOfPathsThroughNode += 1
        betweenness += numberOfPathsThroughNode/numberOfPaths if numberOfPaths != 0 else 0
    return betweenness

def getAllPathsThroughNode(node:Node, graph: list[Node]):
    allNodesToCheck = list(graph)
    allNodesToCheck.remove(node)
    allPaths = []



    # Gets all paths between i and j
    for i in range(len(allNodesToCheck)):
        for j in range(i+1, len(allNodesToCheck)):
            path = bfs(allNodesToCheck[i], allNodesToCheck[j])
            if(path):
                allPaths.append(path)

    return allPaths
    
    # print(numberOfPathsThroughNode)
    # print(numberOfPaths)
    # print(f"Betweeness={betweenness}")
    # print(costs)
    # for path in allPaths:
    #     print(path)
        # for p in path:
        #     print([n.name for n in p])
        # print([n.name for n in path])
    
def calculateCost( path: list[Node]):
    cost = 0
    for i in range(len(path)-1):
        connectionCost = path[i].connections[path[i+1]]
        cost += connectionCost
    return cost

def bfs( start: Node, goal: Node,):
    queue = [[start]]  
    validPaths = []  # List of all valid paths to the goal

    while queue:
        currentPath = queue.pop(0)  # Get the first path in the queue
        lastNode = currentPath[-1]  # Get the last node in the current path

        # If we reached the goal, store the path
        if lastNode == goal:
            validPaths.append(currentPath)
            continue  # Continue exploring other paths

        # Add neighbors to queue if not already in currentPath
        for neighbor in lastNode.connections.keys():
            if neighbor not in currentPath:
                newPath = currentPath + [neighbor]  # Create a new path
                queue.append(newPath)  # Add new path to queue

    return validPaths  # Return all paths found

def sortTupleInList(tup: tuple[Node, int]):
    tup.sort(key=lambda x: x[1], reverse=True)

    # Makes a list of only the nodes
    tup = [val[0] for val in tup]
    return tup