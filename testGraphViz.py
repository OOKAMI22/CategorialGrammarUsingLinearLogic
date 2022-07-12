import networkx as nx
import matplotlib.pyplot as plt

G2 = nx.DiGraph()
G2.add_edges_from(
    [("forAll(x0,_)-", "--o"), ("--o", "np(0,1)+"), ("--o", "s(0,2)-"), ("s(0,2)+", None), ("np(0,1)-", None)])
G2.add_nodes_from(["s(0,2)+", "np(0,1)-"])
pos = nx.spring_layout(G2)

d = nx.degree(G2)

nx.draw(G2, nodelist=d.keys(), node_size=[v * 100 for v in d.values()])
nx.draw_networkx_nodes(G2, pos, node_size=800)
nx.draw_networkx_edges(G2, pos, edgelist=G2.edges, edge_color="black", width=1)
nx.draw_networkx_labels(G2, pos)
plt.show()

