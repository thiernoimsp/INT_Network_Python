import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from Save_OutPut import Save_OutPut_csv, Save_OutPut_txt



def Generating_Flows_Data(number_of_flows, number_of_devices, min_size, max_size) :
	list_save = list()
	i = 0
	while (i<number_of_flows) :
		a = random.randint(0, number_of_devices - 1)
		b = random.randint(0, number_of_devices - 1)
		if a!=b :
			data = [a,b,random.randint(min_size,max_size)]
			list_save.append(data)
			i = i + 1

	#return list_save
	
	filename_csv = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Flow_Data/Flow_Data_' + str(number_of_devices) + '_' + str(number_of_flows) +'.csv'
	filename_txt = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Flow_Data/Flow_Data_' + str(number_of_devices) + '_' + str(number_of_flows) +'.txt'
	Save_OutPut_csv(filename_csv, list_save)
	Save_OutPut_txt(filename_txt, list_save)


def INT_Barabasi(init_nodes, final_nodes, m_parameter) : 
	#G = nx.complete_graph(init_nodes)
	G = nx.path_graph(init_nodes)
	#G = nx.DiGraph()
	#G.add_nodes_from([i for i in range(init_nodes)])
	def rand_prob_node():
		nodes_probs = []
		for node in G.nodes():
			node_degr = G.degree(node)
			#print(node_degr)
			node_proba = node_degr / (2 * len(G.edges()))
			#print("Node proba is: {}".format(node_proba))
			nodes_probs.append(node_proba)
			#print("Nodes probablities: {}".format(nodes_probs))
		random_proba_node = np.random.choice(G.nodes(),p=nodes_probs)
		#print("Randomly selected node is: {}".format(random_proba_node))
		return random_proba_node

	def add_edge():
		if len(G.edges()) == 0:
		    random_proba_node = 0
		else:
		    random_proba_node = rand_prob_node()
		new_edge = (random_proba_node, new_node)
		if new_edge in G.edges():
		    add_edge()
		else:
			if new_node != random_proba_node :
			    G.add_edge(new_node, random_proba_node)
			    

	count = 0
	new_node = init_nodes

	for f in range(final_nodes - init_nodes):
		G.add_node(init_nodes + count)
		count += 1
		for e in range(0, m_parameter):
			add_edge()
		new_node += 1

	H = nx.DiGraph(G)
	nx.write_edgelist(H,'/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Network_Data/Barabasi_Albert/Barabasi_' + str(init_nodes) + '_' + str(final_nodes) + '_' + str(m_parameter) +'.csv',delimiter=',',data=False,encoding='utf-8')
	nx.write_edgelist(G,'/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Network_Data/Barabasi_Albert/Barabasi_' + str(init_nodes) + '_' + str(final_nodes) + '_' + str(m_parameter) +'.txt', comments='#',delimiter=' ',data=False,encoding='utf-8')

	return G


# Genereting Erdos Renyi Graph

def INT_Erdos_Renyi(nombre_of_nodes, probability_to_connect):
	G = nx.Graph()
	G.add_nodes_from([i for i in range(nombre_of_nodes)])

	for i in G.nodes():
		for j in G.nodes():
			if i != j:
				r = random.random()
				if r <= probability_to_connect:
					G.add_edge(i,j)
					
	H = nx.DiGraph(G)
	nx.write_edgelist(H,'/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Network_Data/Erdos_Renyi/Erdos_' + str(nombre_of_nodes) + '_' + str(probability_to_connect) +'.csv',delimiter=',',data=False,encoding='utf-8')
	nx.write_edgelist(H,'/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Network_Data/Erdos_Renyi/Erdos_' + str(nombre_of_nodes) + '_' + str(probability_to_connect) +'.txt', comments='#',delimiter=' ',data=False,encoding='utf-8')
	
	return G
	

# Degree distribution

def plot_deg_dist(graph, filename):
    plt.close()
    num_nodes = graph.number_of_nodes()
    max_degree = 0
    # Calculate the maximum degree to know the range of x-axis
    for n in graph.nodes():
        if graph.degree(n) > max_degree:
            max_degree = graph.degree(n)
    # X-axis and y-axis values
    x = []
    y_tmp = []
    # loop for all degrees until the maximum to compute the portion of nodes for that degree
    for i in range(max_degree+1):
        x.append(i)
        y_tmp.append(0)
        for n in graph.nodes():
            if graph.degree(n) == i:
                y_tmp[i] += 1
        y = [i/num_nodes for i in y_tmp]

    plt.plot(x, y,label='Degree distribution')
    plt.xlabel('Degrees')
    plt.ylabel('Number of nodes')
    plt.title('Degree Distribution')
    #plt.show()
    plt.savefig(filename, format="PNG")
    #plt.close()
