from netmiko import ConnectHandler
import networkx as nx
import matplotlib.pyplot as plt
import re
import matplotlib.image as mpimg
from PIL import Image
import argparse
import socket

def connect_to_device(ip):
	# Create the argument parser
	#parser = argparse.ArgumentParser(description='Connect to a Cisco device.')

	# Add the required arguments
	#parser.add_argument('host', type=str, help='Device hostname or IP address')
	#parser.add_argument('username', type=str, help='Username for device login')
	#parser.add_argument('password', type=str, help='Password for device login')

	# Optional arguments (can be customized as needed)
	#parser.add_argument('--port', type=int, default=22, help='SSH port (default: 22)')
	#parser.add_argument('--device-type', type=str, default='cisco_ios', help='Device type (default: cisco_ios)')
	#parser.add_argument('depth', type=str, help='Depth of neighbor from inital device')

	# Parse the command-line arguments
	#args = parser.parse_args()

	"""
	# Define device details
	device = {
	    'device_type': 'cisco_ios',
	    'ip': '192.168.21.138',
	    'username': 'admin1',
	    'password': 'pass1',
	}
	"""
	
	#if args.depth != 0 :

	# Prepare the device connection parameters
	device_params = {
   		'device_type': 'cisco_ios',
    		'ip': ip,
    		#'port': args.port,
    		'username': 'admin1',
    		'password': 'pass1',
	}

	# Establish SSH connection to the device
	try:
    		net_connect = ConnectHandler(**device_params)
    		print('Connected to the device:', ip)

	except Exception as e:
    		print('Error occurred while connecting to the device:', str(e))


	# Connect to the device
	#net_connect = ConnectHandler(**device)

	return net_connect

def nslookup(hostname):
    	try:
        	ip_address = socket.gethostbyname(hostname)
        	#print(f'IP Address of {hostname}: {ip_address}')
        	return ip_address

    	except socket.gaierror as e:
        	print(f'Error occurred: {e}')


def get_nodes(all_nodes,nodes_and_ip,ip,edge_dict,edge_colors,dict_edge_width):
	#edge_colors = {}
	#edge_dict = {}
	#dict_edge_width = {}
	#nodes = []
	nodes_depth = {}

	ssh = connect_to_device(ip)

	this_node_hostname = ssh.find_prompt()[:-1]

	#nodes_depth[depth] = this_node_hostname

	#nodes.append(this_node_hostname)

	if this_node_hostname not in all_nodes:
		all_nodes.append(this_node_hostname)

	connected_interface = ssh.send_command("show interface status | i connected")
	for i in connected_interface.splitlines():
		row = i.split("connected")
		interface = row[0].strip()
		neighbors = ssh.send_command(f"show cdp neighbors {interface} detail")
		neighbor_name = re.findall("Device ID:.*",neighbors)
		row = row[1].split()
		vlan = row[0]
		speed = row[2]
		media = row[3]

		have_neighbor = False

		# cdp enabled
		if len(neighbor_name) > 0 :
			neighbor_ip = nslookup(neighbor_name[0][11:])
			neighbor_name = neighbor_name[0][11:].split(".")[0]
			neighbor_port = re.findall("outgoing port.*",neighbors)[0][16:]
			neighbor_port = neighbor_port[:2]+re.findall("[0-9]+/.*",neighbor_port)[0]
			have_neighbor = True
			#print(neighbor_port)

		# try lldp
		else:
			neighbors = ssh.send_command(f"show lldp neighbors {interface} detail")
			neighbor_name = re.findall("System Name:.*",neighbors)
			if len(neighbor_name) > 0 :
				neighbor_ip = nslookup(neighbor_name[0][13:])
				neighbor_name = neighbor_name[0][13:].split(".")[0]
				neighbor_port = re.findall("Port id.*",neighbors)[0][9:]
				have_neighbor = True


		if have_neighbor:
			if neighbor_name not in all_nodes:
				#nodes.append(neighbor_name)
				all_nodes.append(neighbor_name)
				#print(neighbor_ip)
				nodes_and_ip[neighbor_name] = neighbor_ip
			if (this_node_hostname,neighbor_name) in edge_dict:
				if interface not in edge_dict[this_node_hostname,neighbor_name]:
					existing_interface = edge_dict[(this_node_hostname,neighbor_name)]
					edge_dict[(this_node_hostname,neighbor_name)] = existing_interface+"\n"+interface
					dict_edge_width[(this_node_hostname,neighbor_name)] = 3.0
			if(neighbor_name,this_node_hostname) in edge_dict:
				if neighbor_port not in edge_dict[neighbor_name,this_node_hostname]:
					existing_neighbor_port = edge_dict[(neighbor_name,this_node_hostname)]
					edge_dict[(neighbor_name,this_node_hostname)] = existing_neighbor_port+"\n"+neighbor_port
			else:
				edge_dict[(this_node_hostname,neighbor_name)] = interface
				edge_dict[(neighbor_name,this_node_hostname)] = neighbor_port
				dict_edge_width[(this_node_hostname,neighbor_name)] = 1.0
			if speed == "10":
				edge_colors[(this_node_hostname,neighbor_name)] = "red"
			else:
				edge_colors[(this_node_hostname,neighbor_name)] = "black"


	#print(edge_dict)
	#nodes_depth[depth+1] = nodes 

	#print(nodes_depth)
	#print(dict)
	#print(dict_edge_width)
	#print(edge_colors)
	#print(f"before return nodes and ip {nodes_and_ip}")
	return this_node_hostname,edge_dict,edge_colors,dict_edge_width,all_nodes,nodes_and_ip


def draw_diagram(hostname,nodes,edge_dict,colors,edge_width):
	print("start drawing\n=================")
	print(hostname)
	print(nodes)
	print(edge_dict)
	print(colors)
	print(edge_width)
	# Create an empty graph
	G = nx.Graph()

	# Add nodes
	G.add_nodes_from(nodes)
	#print(nodes)

	#working
	#G.add_node("SW",shape='square')
	#G.add_node("SW-DIST",shape='diamond')
	#G.add_node("R1",shape='circle')

	# Add edges
	edge_labels = {}
	for edge_pair in edge_dict:
		print(edge_pair)
		#print(edge_pair.split(","))
		print(edge_pair[0])
		print(edge_pair[1])
		G.add_edge(edge_pair[0],edge_pair[1])

	print(G.edges())

	#G.add_edges_from(edge_dict)

	# Add labels
	edge_labels = edge_dict

	# Draw the network diagram
	pos = nx.spring_layout(G)
	nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=6, font_weight='bold', edge_color=[colors[edge] for edge in G.edges()], width=[edge_width[edge] for edge in G.edges()])
	#nx.draw_networkx_edges(G, pos, edge_color=[colors[edge] for edge in G.edges()])
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue', label_pos =0.7, font_size=6)
	#nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000, node_shape={"SW":"s"})
	# Draw nodes with custom shapes

	##node_shapes = {'square':'s','diamond':'d','circle':'o'}

	##for node, attrs in G.nodes(data=True):
    	##	shape = attrs['shape']
    	##	nx.draw_networkx_nodes(G, pos, nodelist=[node], node_shape=node_shapes[shape])


	plt.title("Network Diagram")
	plt.axis('off')
	plt.show()


def exec():

	# Create the argument parser
	parser = argparse.ArgumentParser(description='Connect to a Cisco device.')

	# Add the required arguments
	parser.add_argument('host', type=str, help='Device hostname or IP address')
	#parser.add_argument('username', type=str, help='Username for device login')
	#parser.add_argument('password', type=str, help='Password for device login')

	# Optional arguments (can be customized as needed)
	#parser.add_argument('--port', type=int, default=22, help='SSH port (default: 22)')
	#parser.add_argument('--device-type', type=str, default='cisco_ios', help='Device type (default: cisco_ios)')
	parser.add_argument('depth', type=int, help='Depth of neighbor from inital device')

	# Parse the command-line arguments
	args = parser.parse_args()

	#nodes_dictionary = []
	#nodes_dictionary.append({"ip": args.host,"depth":0})

	all_nodes = []
	nodes_and_ip = {"first_device":args.host}
	edge_dict = {}
	edge_colors = {}
	width = {}
	#nodes = [args.host]

	#nodes_and_ip_here = nodes_and_ip

	
	for d in range(args.depth):
		print(d)
		#print(nodes_and_ip)
		copy_nodes_and_ip = nodes_and_ip.copy()
		nodes_and_ip = {}
		print(copy_nodes_and_ip)
		for key in copy_nodes_and_ip:
			hostname,edge_dict,edge_colors,width,all_nodes,nodes_and_ip = get_nodes(all_nodes,nodes_and_ip,copy_nodes_and_ip[key],edge_dict,edge_colors,width)
			#get_nodes(all_nodes,copy_nodes_and_ip[key])
		#print(nodes_and_ip)

	
	print("hostname:"+hostname)
	print("==============\nedge_dict\n===============")
	print(edge_dict)
	print("==============\nedge_colors\n===============")
	print(edge_colors)
	print("==============\nwidth\n===============")
	print(width)
	print("==============\nallnodes\n===============")
	print(all_nodes)
	print("==============\nnodes_and_ip\n===============")
	print(copy_nodes_and_ip)
	

	draw_diagram(hostname,all_nodes,edge_dict,edge_colors,width)


if __name__ == "__main__":
    exec()
