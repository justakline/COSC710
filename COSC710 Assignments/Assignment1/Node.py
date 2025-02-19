# For all graphs, a node has a connection to other nodes with a weight
# For directed graphs, like 2 -> 3, only  2 has that connect
# For undirected graphs like 2 - 3, both 2 and three has that connection

class Node:
    def __init__(self, name):
        self.connections: dict["Node", int] = {}
        self.name = name

    def addNode(self, node: "Node", weight:int):
        self.connections[node] = weight

    def __str__(self):
        connectionsRep = ""
        for node, weight in self.connections.items():
            connectionsRep += f"{self.name}->{node} |{weight}| \t"
        return f"{connectionsRep}"