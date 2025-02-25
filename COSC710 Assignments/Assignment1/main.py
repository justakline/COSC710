from Node import Node
from Calculations import *
import sys

def start():
    graph: list[Node] = []
    connections:list[list[int]] = []
    isDirected: bool
    numberOfNodes: int

    validPath: bool = False
    while(not validPath):
        try:
            pathName: str = input("Please provide the path to the file with the graph information: ")
            if(pathName == "q"):
                sys.exit()
            # Getting the paramaeters of the graph
            with open(pathName, "r") as file:
                firstLine = file.readline()
                firstLine = firstLine.strip().split(" ")

                if(len(firstLine) != 2 or not isValidHeaderNum(firstLine[0]) or not isValidHeaderNum(firstLine[1]) ):
                    raise Exception("The First line in your file needs exactly 2 positive ints and nothing else")
                numberOfNodes = int(firstLine[0])
                directedNumber = int(firstLine[1])
                if(numberOfNodes <= 0):
                    raise Exception("The number of nodes needs to be bigger than 0")
                if(directedNumber != 0 and directedNumber != 1):
                    raise Exception("Wrong number for your direction, should be either 0 or 1")
                isDirected = True if directedNumber == 1 else False

            # get the connections
            with open(pathName, "r") as file:
                # Skip first line
                file.readline()
                for line in file:
                    lineArray: list[str] = line.strip().split(" ")
                    if(len(lineArray) != 3 or not isValidNum(lineArray[0],numberOfNodes) or not isValidNum(lineArray[1], numberOfNodes) or not isValidNum(lineArray[2],numberOfNodes, False)):
                        raise Exception("After the first line in your file, every line afterwards must contain exactly 3 ints (first 2 must be positive) and nothing else.\nAlso if the number of nodes you provide=n then nodes in the graph will be 0, 1,...,n-1,\nso if you reference a connection from or to node n or above, that is incorrect formatting")
                    connections.append([int(num) for num in line.strip().split(" ") if num])
            graph = initializeGraph(numberOfNodes)
            createConnectionsInGraph(graph, connections, isDirected)
            validPath = True
        except SystemExit:
            raise 
        except Exception as e:
            print(f"\n{e}\n")
            # print("There was an error, either your provided the wrong path\nor the file was not formatted correctly.\n")
        

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
    clusteringList = getClusteringList(graph, isDirected )
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
            print("Please type in an int \n")

    degreesList = degreesList[k:]
    betweenessList = betweenessList[k:]
    closenessList = closenessList[k:]
    clusteringList = clusteringList[k:]


    allLists: list[tuple[list[Node], str]] = [(degreesList, "degreesList"), (betweenessList, "betweenessList"), (closenessList, "closenessList"), (clusteringList, "clusteringList")]

    # Create a file for each list
    for l, name in allLists:
        print(f"{name}:\t{l}")

        graphCopy:list[Node]  = removeNodesFromGraph(graph.copy(), l)
        # printGraph(graphCopy)
        # print(graphCopy)
        with open(f"{name}.txt", "w") as file:
            graphType = 1 if isDirected else 0
            file.write(f"{len(l)} {graphType}\n")
            # Write dowm each of the nodes and their connections
            nodePairs: list[set] = [] 
            for node in graphCopy:
                connections = node.connections
                for tup in connections:
                    pair = {node.name,tup[0].name}
                    # Check for the pair because
                    if(graphType == 0 and pair not in nodePairs):
                        file.write(f"{node.name} {tup[0].name} {tup[1]}\n")
                        nodePairs.append(pair)
                    if(graphType == 1):
                        file.write(f"{node.name} {tup[0].name} {tup[1]}\n")
    print(f"\n4 files were created that show the graph without the top k nodes, please reference each. \nIf you would like to see what the values are, please go into Calculations.py, and in the top 4 functions, there is a commented print statement. \nUncomment them and you will see the values of each set up in a list[ (Node, val) ] \n")

def isValidHeaderNum(num:str):
    try:
        newNum = int(num)
        if(newNum < 0) :
            return False
        return True
    except:
        return False

def isValidNum(num:str, numberOfNodes:int, checkIfNeg:bool=True):
    try:
        newNum = int(num)
        if((checkIfNeg and newNum < 0) or newNum >= numberOfNodes):
            return False
        return True
    except:
        return False

def removeNodesFromGraph(graph: list[Node], nodeList: list[Node], ) -> list[Node]:
    graphCopy = []
    graphCopy = createGraphDeepCopy(graph)
    nodeListCopy = []
    
    for node in nodeList:
        for n in graphCopy:
            if node.name == n.name:
                nodeListCopy.append(n)
    removed = []

    # printGraph(graphCopy)    
    # Remove the nodes from the graph
    for node in graphCopy:
        if(node not in nodeListCopy):
            removed.append(node)
            graphCopy.remove(node)
    # printGraph(graphCopy)
    # Remove the edges associated with the removed nodes
    for node in graphCopy:
        newNodeConnections = []
        for tup in node.connections:
            if(tup[0] not in removed):
                newNodeConnections.append(tup)
        node.connections = newNodeConnections
    # printGraph(graphCopy)
    return graphCopy


def createGraphDeepCopy(graph: list[Node]):
    newGraph = initializeGraph(len(graph))
    connections = []
    for i, node in enumerate(graph):
        connections = node.connections
        for node, edge in connections:
            newGraph[i].connections.append((newGraph[node.name],edge))
            
    return newGraph
        




def initializeGraph(numberOfNodes):
    graph: list[Node] = []
    for i in range(numberOfNodes):
        graph.append(Node(i))
    return graph


# Graph type 0, means undireected, so both nodes have a connection to each other
def createConnectionsInGraph(graph:list[Node], connections:list[list[int]], isDirected:bool):
    for connect in connections:
        a = connect[0]
        b = connect[1]
        weight = connect[2]
        graph[a].addNode(graph[b], weight)

        if(not isDirected):
            graph[b].addNode(graph[a], weight)



def printGraph(graph: list[Node]):
    for node in graph:
        print(node)



if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
