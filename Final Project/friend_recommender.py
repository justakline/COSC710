
import networkx as nx
import pandas as pd

import to_authors
# Make sure the nodes are able to be seen
def ensure_nodes(G: nx.Graph, nodes: list[int]):
    missing = [n for n in nodes if n not in G]
    if missing:
        G.add_nodes_from(missing)
        print(f"Added {len(missing)} isolated nodes to the graph (missing owners).")

# Create this just in case we can't recommend
def popularity_order(G: nx.Graph) -> list[int]:
    return [n for n, _ in sorted(G.degree(weight="weight"), key=lambda t: t[1], reverse=True)]


# Use jaccard to reccomend new friends that are not already friends
def similarity_candidates(G: nx.Graph, node: int, excluded: set[int]):
    other_nodes = (v for v in G if v not in excluded)
    pairs = ((node, v) for v in other_nodes)

    raw = nx.jaccard_coefficient(G, pairs)

    return sorted(((v, score) for _, v, score in raw), key=lambda t: t[1], reverse=True)


def recommend(G: nx.Graph, node: int, pop_iter, k=3):
    neigh = set(G.neighbors(node))
    neigh.add(node)

    # Primary: similarity‑based
    sims = similarity_candidates(G, node, neigh)
    recs = []
    for cand, _ in sims:
        if cand not in recs:
            recs.append(cand)
        if len(recs) == k:
            break

    # Fallback: cycle through global popularity iterator (shared generator)
    while len(recs) < k:
        try:
            cand = next(pop_iter)
        except StopIteration:  # exhausted
            recs.append(-1)
            continue
        if cand in neigh or cand in recs:
            continue
        recs.append(cand)

    return recs


def main():
    G = nx.read_weighted_edgelist("finalUserUserGraph.txt", nodetype=int)
    owners = []
    with open("top_owners_index.txt", "r") as file:
        owners = [int(line.strip()) for line in file.readlines() if line.strip()]
    ensure_nodes(G, owners)

    global_pop = popularity_order(G)
    pop_iter = iter(global_pop)

    out_rows = []
    for owner in owners:
        recs = recommend(G, owner, pop_iter, 3)
        out_rows.append([owner, *recs])

    cols = ["user_index", *[f"rec_{i+1}" for i in range(3)]]
    pd.DataFrame(out_rows, columns=cols).to_csv("friend_recommendations_top500.csv", index=False)
    print(f"Done → {"friend_recommendations_top500.csv"} with {len(out_rows)} rows.")
    to_authors.convert()

if __name__ == "__main__":
    main()
