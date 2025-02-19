from Node import Node




def start():
    graph: list[Node] = []
    connections:list[list[int]] = []
    graphType: int
    numberOfNodes: int

    # Getting the paramaeters of the graph
    with open("graph.txt", "r") as file:
        firstLine = file.readline()
        firstLine = firstLine.split(" ")
        numberOfNodes = int(firstLine[0])
        graphType = int(firstLine[1])

    # get the connections
    with open("graph.txt", "r") as file:
        # Skip first line
        file.readline()
        for line in file:
            connections.append([int(num) for num in line.strip().split(" ") if num])

    graph = initializeGraph(numberOfNodes)

    createConnectionsInGraph(graph, connections, graphType)
    print(calculateCentrality(graph))
    printGraph(graph)


# returns a list of each node in the graph. organized by desc centrality score
def calculateCentrality(graph: list[Node]):
    # (Node, centrality score)
    centralites = [(None, 0) for i in range(len(graph))]
    for i, node in enumerate(graph):
        centralites[i] = (node, len(node.connections))

    # Sort the tuples by the score
    centralites.sort(key=lambda x: x[1], reverse=True)

    # Makes a list of only the nodes
    centralites = [val[0] for val in centralites]
    return centralites




def initializeGraph(numberOfNodes):
    graph: list[Node] = []
    for i in range(numberOfNodes):
        graph.append(Node(i))
    return graph


# Graph type 0, means undireected, so both nodes have a connection to each other
def createConnectionsInGraph(graph:list[Node], connections:list[list[int]], graphType:int):
    for connect in connections:
        a = connect[0]
        b = connect[1]
        weight = connect[2]
        graph[a].addNode(b, weight)

        if(graphType == 0):
            graph[b].addNode(a, weight)



def printGraph(graph: list[Node]):
    for node in graph:
        print(node)



if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
