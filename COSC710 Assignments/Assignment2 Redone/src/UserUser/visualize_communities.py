import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import scipy

# Paths to data files
graph_path = 'finalUserUserGraph.txt'
comm_csv = 'community_assignments.csv'


def load_graph(path):
    G = nx.Graph()
    with open(path, 'r') as f:
        for line in f:
            u, v, w = line.strip().split()
            G.add_edge(int(u), int(v), weight=float(w))
    return G


def load_communities(path):
    """
    Load community assignments into a dict node->community
    """
    df = pd.read_csv(path)
    return df.groupby('community')['node'].apply(list).to_dict()


def visualize_community_subgraph(G, nodes, cid, layout='spring'):
    """
    Visualize the subgraph for one community.
    """
    subG = G.subgraph(nodes)
    plt.figure(figsize=(6,6))
    # choose layout
    if layout == 'spring':
        pos = nx.spring_layout(subG, seed=42)
    elif layout == 'spectral':
        pos = nx.spectral_layout(subG)
    else:
        pos = nx.random_layout(subG)

    # draw nodes and edges
    nx.draw_networkx_nodes(subG, pos, node_size=50, alpha=0.8)
    nx.draw_networkx_edges(subG, pos, alpha=0.4)
    plt.title(f'Community {cid} (n={subG.number_of_nodes()})')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def main():
    # Load data
    G = load_graph(graph_path)
    communities = load_communities(comm_csv)

    # Visualize top 5 communities by size
    sorted_comms = sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)
    div = 70
    for cid, nodes in sorted_comms[int(len(sorted_comms)/div): int(len(sorted_comms)/div) + 5]:
        visualize_community_subgraph(G, nodes, cid, layout='spring')

if __name__ == '__main__':
    main()
