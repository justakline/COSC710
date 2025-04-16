import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Paths to data files
GRAPH_PATH = 'finalUserUserGraph.txt'
COMM_CSV = 'community_assignments.csv'


def load_graph(path):
    G = nx.Graph()
    with open(path, 'r') as f:
        for line in f:
            u, v, w = line.strip().split()
            G.add_edge(int(u), int(v), weight=float(w))
    return G


def analyze_communities(G, comm_df):
    """
    For each community, compute:
      - number of nodes
      - number of internal edges
      - density
      - average clustering coefficient
      - average degree
    Returns a DataFrame of stats.
    """
    records = []
    for cid, group in comm_df.groupby('community'):
        nodes = list(group['node'])
        subG = G.subgraph(nodes)
        n_nodes = subG.number_of_nodes()
        n_edges = subG.number_of_edges()
        density = nx.density(subG)
        avg_clust = nx.average_clustering(subG, weight='weight')
        avg_deg = sum(dict(subG.degree()).values()) / n_nodes if n_nodes else 0
        records.append({
            'community': cid,
            'nodes': n_nodes,
            'edges': n_edges,
            'density': density,
            'avg_clustering': avg_clust,
            'avg_degree': avg_deg
        })
    return pd.DataFrame(records)


def visualize_summary(summary_df):
    """
    Create and display two visualizations:
      1. Bar chart of top 10 communities by size
      2. Scatter plot of density vs average degree for all communities
    """
    # Top 10 by node count
    top10 = summary_df.nlargest(10, 'nodes')
    plt.figure()
    plt.bar(top10['community'].astype(str), top10['nodes'])
    plt.xlabel('Community ID')
    plt.ylabel('Number of Nodes')
    plt.title('Top 10 Communities by Size')
    plt.tight_layout()
    plt.show()

    # Density vs Avg Degree scatter
    plt.figure()
    plt.scatter(summary_df['density'], summary_df['avg_degree'])
    plt.xlabel('Density')
    plt.ylabel('Average Degree')
    plt.title('Community Density vs Average Degree')
    plt.tight_layout()
    plt.show()


def main():
    # Load graph and community assignments
    G = load_graph(GRAPH_PATH)
    comm_df = pd.read_csv(COMM_CSV)

    # Analyze communities and save summary
    summary_df = analyze_communities(G, comm_df)
    summary_df.to_csv('community_summary.csv', index=False)
    print('Saved community_summary.csv')

    # Print overview of top communities
    print('\nTop 10 communities by size:')
    print(summary_df.nlargest(10, 'nodes')[['community', 'nodes']].to_string(index=False))

    # Visualize results
    visualize_summary(summary_df)


if __name__ == '__main__':
    main()
