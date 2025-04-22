from afinn import Afinn
import networkx as nx

# 2) Load your author→ID mapping (if you already have one), else assign on the fly

author_to_id = {}
with open('authorToIndex.txt') as f:
    for line in f:
        name, idx = line.strip().split()
        author_to_id[name] = int(idx)
af = Afinn()
G  = nx.DiGraph()

with open("commenter_author_text.txt", "r") as f:
     for line in f.readlines():
          words = line.split(" ", maxsplit = 2)
          commenter, sugg_author, text = [words[0] ,words[1], words[2]]
          # text = text.replace("\n", "")

          # look up numeric IDs (skip if missing)
          u = author_to_id.get(commenter)
          v = author_to_id.get(sugg_author)
          if u is None or v is None:
               continue

          # 4) compute sentiment (positive = >0, negative <0)
          score = af.score(text)

          # 5) add (or accumulate) the edge
          if G.has_edge(u, v):
               G[u][v]['weight'] += score
          else:
               G.add_edge(u, v, weight=score)

# # 6) write out your edge list
with open('suggestion_user_graph.txt', 'w') as out:
    for u, v, data in G.edges(data=True):
        out.write(f"{u} {v} {data['weight']:.3f}\n")
