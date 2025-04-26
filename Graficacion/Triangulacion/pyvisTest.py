from pyvis.network import Network
import random
bounds = [60, 60]
nodes =  16
net = Network("600px", "600px", bgcolor="#161616") # crear red

for _ in range(nodes):
    x = random.randint(0,bounds[0])
    y = random.randint(0,bounds[1])
    net.add_node(n_id=_,shape="dot", color="#ff5353", borderWidth=0, x=x, y=y, size=1, physics=False)

net.set_options('''
{
  "interaction": {
    "dragNodes": false
  }
}
''')

net.write_html('nx.html', notebook=False)