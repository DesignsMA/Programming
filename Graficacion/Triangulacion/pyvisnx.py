from pyvis.network import Network
import networkx as nx
import random
bounds = [60, 60]
nodes =  16

nx_graph = nx.Graph()
for _ in range(nodes):
    x = random.randint(0,bounds[0])
    y = random.randint(0,bounds[1])
    nx_graph.add_node(_,key=_, size=3, x=x, y=y )

nt = Network("600px", "600px", notebook=False)
nt.from_nx(nx_graph)
nt.show('nx.html', notebook=False)