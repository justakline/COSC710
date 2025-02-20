from Node import Node


# returns a list of each node in the graph. organized by desc degree score
def getDegreeList(graph: list[Node]):
    # (Node, centrality score)
    degrees = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        degrees[i] = (node, len(node.connections))

    # Sort the tuples by the score
    degrees.sort(key=lambda x: x[1], reverse=True)

    
    # Makes a list of only the nodes
    degrees = [val[0] for val in degrees]
    return degrees

# returns a list of each node in the graph. organized by desc betweeness score
def getBetweenessList(graph: list[Node]):
    # (Node, betweeness score)
    betweeness = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        betweeness[i] = (node, calculateBetweeness(node, graph))

    # Sort the tuples by the score
    betweeness.sort(key=lambda x: x[1], reverse=True)


    # Makes a list of only the nodes
    betweeness = [val[0] for val in betweeness]
    return betweeness

# returns a list of each node in the graph. organized by desc closeness score
def getClosenessList(graph: list[Node]):
    # (Node, centrality score)
    closeness = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        closeness[i] = (node, calculateCloseness(node, graph))

    # Sort the tuples by the score
    closeness.sort(key=lambda x: x[1], reverse=True)

    # for node, val in closeness:
    #     print(f"{node.name}: has score {val}")

    # Makes a list of only the nodes
    closeness = [val[0] for val in closeness]
    return closeness

# Closeness = sum(minumumpaths)/numberOfNodes-1
def calculateCloseness(node, graph):
    allPaths = [bfs(node, n) for n in graph if n is not node]
     # go through each pair of nodes and finds the min cost
    total = 0
    for i, path in enumerate(allPaths):
        costs = []

        # Calculates the cost of each path from i, j... We do not really know what i and j are haha
        for p in path:
            costs.append(calculateCost(p))


        minCost = min(costs)
        total += minCost
        
    
    
    closeness = total/(len(graph)-1)
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
        
        # Keep all the minimum paths
        minCost = min(costs)
        for j in range(len(allPaths[i])- 1, -1, -1):  
            if(costs[j] != minCost):
                allPaths[i].pop(j)
                costs.pop(j)

        numberOfPaths = len(allPaths[i])
        numberOfPathsThroughNode = 0
        for path in allPaths[i]:
            if(node in path):
                numberOfPathsThroughNode += 1
        betweenness += numberOfPathsThroughNode/numberOfPaths
    return betweenness

def getAllPathsThroughNode(node:Node, graph: list[Node]):
    allNodesToCheck = list(graph)
    allNodesToCheck.remove(node)
    allPaths = []

    # Gets all paths between i and j
    for i in range(len(allNodesToCheck)):
        for j in range(i+1, len(allNodesToCheck)):
            allPaths.append(bfs(allNodesToCheck[i], allNodesToCheck[j]))
    return allPaths
    
    print(numberOfPathsThroughNode)
    print(numberOfPaths)
    print(f"Betweeness={betweenness}")
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


