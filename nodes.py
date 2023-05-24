import networkx as nx
import matplotlib.pyplot as plt
from netmiko import ConnectHandler
import re


cisco_router = {
    'device_type': 'cisco_ios',
    'host': '192.168.21.138',
    'username': 'admin1',
    'password': 'pass1',
    'secret': 'enable',
    'port': 22,
}

ssh = ConnectHandler(**cisco_router)
hostname = ssh.find_prompt()[:-1]

up_interface = ssh.send_command("show interface status | i connected")

if_list = up_interface.splitlines(True)

# declare Graph
G = nx.Graph()

labels = {}

for a in if_list:
 interface = a.split()
 cdp = ssh.send_command(f"show cdp neighbor {interface[0]}")
 cdp = re.findall(".*/.*",cdp)
 if len(cdp) > 0 :
  for b in cdp:
    b = b.split()
    print(f"{interface[0]} - {b[0]}")
    e = G.add_edge(hostname,b[0])
    labels[(hostname,b[0])] = interface[0]


#print(labels) 
#print(G.nodes)
#print(G.edges)


pos = nx.spring_layout(G)
plt.figure()

"""
options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3,
}
"""

#subax1 = plt.subplot(111)
nx.draw(G,pos,  with_labels=True, width=1,linewidths=1,font_weight='bold', node>
#nx.draw(G, with_labels=True, font_weight='bold', node_color='black', edge_colo>
#nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
#    node_size=500, node_color='pink', alpha=0.9,
#    labels={node: node for node in G.nodes()}
#)
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_color='green')

plt.axis('off')
plt.show()
