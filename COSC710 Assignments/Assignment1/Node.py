# For all graphs, a node has a connection to other nodes with a weight
# For directed graphs, like 2 -> 3, only  2 has that connect
# For undirected graphs like 2 - 3, both 2 and three has that connection

class Node:
    def __init__(self, name):
        self.connections: list[tuple["Node", int]] = []
        self.name = name

    def addNode(self, node: "Node", weight:int):
        
        self.connections.append([node, weight])

    def __str__(self):
        connectionsRep = ""
        for connection in self.connections:
            connectionsRep += f"{self.name}->{connection[0].name} |{connection[1]}| \t"
        return f"{connectionsRep}"
    
    def __repr__(self):
        return f"{self.name}"