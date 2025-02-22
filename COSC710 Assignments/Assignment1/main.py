from Node import Node
from Calculations import *


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
    # printGraph(graph)

    ########### Organize by Degrees ##########
    degreesList:list = getDegreeList(graph)
    # print([node.name for node in degreesList])

    ########## Organize by Betweeness ########
    betweenessList = getBetweenessList(graph)
    # print ([node.name for  node in betweenessList])


    ########### Organize by Closeness ##########
    # calculateCloseness(graph[1], graph)
    closenessList:list = getClosenessList(graph)
    # print([node.name for node in closenessList])

     ########## Organize by Clustering Coeff ########
    clusteringList = closenessList.copy()
    # clusteringList = getClusteringList(graph)
    # print ([node.name for  node in betweenessList])
    k = 0
    validInput = False
    while(not validInput):
        try:
            k = int(input("Please enter k nodes to remove: ")) 
            if( k > len(graph) or k < 0):
                raise  Exception(f"You can only remove 0 - {len(graph)} nodes") 
            validInput = True
        except Exception as e:
            print(e)
            print("Please type in a number\n")

    degreesList = degreesList[k:]
    betweenessList = betweenessList[k:]
    closenessList = closenessList[k:]
    clusteringList = clusteringList[k:]


    allLists: list[tuple[list[Node], str]] = [(degreesList, "degreesList"), (betweenessList, "betweenessList"), (closenessList, "closenessList"), (clusteringList, "clusteringList")]

    # Create a file for each list
    for l, name in allLists:
        graphCopy:list[Node]  = removeNodesFromGraph(graph.copy(), l)
        print(graphCopy)
        with open(f"{name}.txt", "w") as file:
            file.write(f"{len(l)} {graphType}\n")
            # Write dowm each of the nodes and their connections
            nodePairs: list[set] = [] 
            for node in graphCopy:
                connections = node.connections
                for n, weight in connections.items():
                    pair = {node.name,n.name}
                    # Check for the pair because
                    if(graphType == 0 and pair not in nodePairs):
                        file.write(f"{node.name} {n.name} {weight}\n")
                        nodePairs.append(pair)
                    if(graphType == 1):
                        file.write(f"{node.name} {n.name} {weight}\n")


        






def removeNodesFromGraph(graph: list[Node], nodeList: list[Node]) -> list[Node]:
    graphCopy = graph.copy()

    for node in graph:
        if(node not in nodeList):
            graphCopy.remove(node)
    return graphCopy







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
        graph[a].addNode(graph[b], weight)

        if(graphType == 0):
            graph[b].addNode(graph[a], weight)



def printGraph(graph: list[Node]):
    for node in graph:
        print(node)



if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
