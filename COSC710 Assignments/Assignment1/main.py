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


    ########### Organize by Centrality ##########
    # calculateCloseness(graph[1], graph)
    centralityList:list = getClosenessList(graph)
    # print([node.name for node in centralityList])


    ########### Organize by Degrees ##########
    degreesList:list = getDegreeList(graph)
    # print([node.name for node in degreesList])

    ########## Organize by Betweeness ########
    betweenessList = getBetweenessList(graph)
    # print ([node.name for  node in betweenessList])










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
