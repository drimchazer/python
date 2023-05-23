import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge("switch", "router")

options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3,
}

subax1 = plt.subplot(111)
nx.draw(G, with_labels=True, font_weight='bold', node_color='black', edge_color='blue', node_shape="s",bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.5'))
#nx.draw(G, with_labels=True, font_weight='bold', node_color='black', edge_color='blue', node_shape="s")

plt.show()
