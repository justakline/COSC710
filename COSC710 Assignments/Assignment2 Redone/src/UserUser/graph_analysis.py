import networkx as nx
import pandas as pd


def load_graph(path):
    """
    Load a user-user graph from a text file into a NetworkX Graph.
    Each line should be: node1 node2 weight
    """
    G = nx.Graph()
    with open(path, 'r') as f:
        for line in f:
            u, v, w = line.strip().split()
            G.add_edge(int(u), int(v), weight=float(w))
    return G


def compute_statistics(G):
    """
    Compute basic network statistics.
    Returns: num_nodes, num_edges, avg_degree, avg_clustering
    """
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = sum(dict(G.degree()).values()) / num_nodes
    avg_clustering = nx.average_clustering(G, weight='weight')
    return num_nodes, num_edges, avg_degree, avg_clustering


def detect_communities_louvain(G):
    """
    Detect communities using NetworkX's built-in Louvain method.
    Returns a dict mapping node -> community_id.
    """
    communities = nx.community.louvain_communities(G, weight='weight')
    # Map each node to its community index
    comm_dict = {node: cid for cid, comm in enumerate(communities) for node in comm}
    return comm_dict


def compute_centrality(G):
    """
    Compute degree and betweenness centrality for each node.
    Returns two dicts: degree_centrality, betweenness_centrality
    """
    deg_cent = nx.degree_centrality(G)
    bet_cent = nx.betweenness_centrality(G,
                                         k=60,
                                         weight='weight',
                                         normalized=True,
                                         seed=42)
    return deg_cent, bet_cent


def main():
    # Path to user-user graph file
    path = 'finalUserUserGraph.txt'
    G = load_graph(path)

    # Compute and display basic stats
    n_nodes, n_edges, avg_deg, avg_clust = compute_statistics(G)
    print(f'Nodes: {n_nodes}, Edges: {n_edges}, Avg degree: {avg_deg:.2f}, '
          f'Avg clustering: {avg_clust:.4f}')

    # Fast community detection
    comm_dict = detect_communities_louvain(G)
    comm_df = pd.DataFrame(list(comm_dict.items()), columns=['node', 'community'])
    print('\nCommunity sizes:')
    print(comm_df['community'].value_counts().sort_index())

    # # Centrality measures
    deg_cent, bet_cent = compute_centrality(G)
    cent_df = pd.DataFrame({
        'node': list(deg_cent.keys()),
        'degree_centrality': list(deg_cent.values()),
        'betweenness_centrality': [bet_cent[n] for n in deg_cent.keys()],
        'community': [comm_dict[n] for n in deg_cent.keys()]
    })
    print('\nTop 10 by degree centrality:')
    print(cent_df.nlargest(10, 'degree_centrality')[['node', 'degree_centrality']].to_string(index=False) )
    print('\nTop 10 by betweenness centrality:')
    print(cent_df.nlargest(10, 'betweenness_centrality')[['node', 'betweenness_centrality']].to_string(index=False) )

    # Save detailed results
    comm_df.to_csv('community_assignments.csv', index=False)
    cent_df.to_csv('centrality_measures.csv', index=False)


if __name__ == '__main__':
    main()
