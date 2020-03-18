# My principal Module
import numpy as np
import pandas as pd
import networkx as nx
import csv
import collections
import pylab as plt

#plt.style.use("fivethirtyeight")
def Constructing_and_Loading_Network(filename, number_of_devices, embeded_items) : 
	data = pd.read_csv(filename, sep=',', header = None, names = ['ori', 'dst'])
        # Creating a DataFrame from data
	df = data[['ori', 'dst']]
	src_node = df.ori
	dst_node = df.dst


	# Set of devices
	D=[d for d in range(number_of_devices)]

	#constructing the graph
	G = nx.Graph()
	G.add_nodes_from(D)
	no_link = len(src_node)
	edges_links = [i for i in range(no_link)]
	for i in edges_links :
		G.add_edge(src_node[i], dst_node[i])

	#adding same telemetry Items to all nodes
	for d in D :
		G.nodes[d]['Items'] = embeded_items

	return (D, G)


# Functional for loading origin, destination and capacities of flows
def Loading_Network_Flows(filename, number_of_flows) : 
	data2 = pd.read_csv(filename, sep=',', header = None, names = ['ori_flow', 'dst_flow', 'cap_flow'])
	df2 = data2[['ori_flow', 'dst_flow', 'cap_flow']]
	S = df2.ori_flow #Starting node of the flow
	E = df2.dst_flow # Ending node of the flow
	cap = df2.cap_flow # capacity of the flow

	# Set of flows
	F=[f for f in range(number_of_flows)]
	Kf=dict(zip(range(number_of_flows), cap))

	return (F, S, E, Kf)


# Functional for telemetry items
def Loding_Telemetry_Items(number_of_telemetry_items, size_of_telemetry_items) :
	# Set of telemetry items
	V = [v for v in range(number_of_telemetry_items)]
	Size = dict(zip(range(number_of_telemetry_items),size_of_telemetry_items))

	return (V, Size)

# Functional for monitoring application
def Loding_Monitoring_Applications(number_of_monitoring_application, spatial_requirements) :
	#set of Monitoring Applications
	M = [m for m in range(number_of_monitoring_application)]
	R = dict(zip(range(number_of_monitoring_application),spatial_requirements))

	return (M, R)



# Functional for the subset of a set
def get_subsets(fullset):
   listrep = list(fullset)
   subsets = []
   for i in range(2**len(listrep)):
      subset = []
      for k in range(len(listrep)):
         if i & 1<<k:
           subset.append(listrep[k])
      subsets.append(subset)
   return subsets



def Spatial_And_Temporal_Dependencies_Requirements(M,R) :
	PR={}

	for m in M :
		PR[m] = get_subsets(set(R[m]))
		del PR[m][0]

	#spatial dependency
	Rs = {}
	for m in M :
		Rs[m] = PR[m]

	# index for set Rs
	idxs_Rs = {}
	for m in M :
		idxs_Rs[m] = list(range(len(Rs[m])))

	#temporal dependency
	Rt = {}
	for m in M :
		Rt[m] = Rs[m]

	# index for set Rt
	idxs_Rt = {}
	for m in M :
		idxs_Rt[m] = list(range(len(Rt[m])))

	#function of the required deadline time
	TT={}
	c=1
	for m in M :
		for P in range(len(Rs[m])) :
			c += 1
			TT[P] = c

	#function of the last time unit
	HH={}
	c=0
	for m in M :
		for P in range(len(Rt[m])) :
			c += 1
			HH[P] = c

	return (PR, Rs, idxs_Rs, Rt, idxs_Rt, TT, HH)


def Plot_Device_Items(filename, nb_devices, nb_items) : 
	data = pd.read_csv(filename, sep=',', header = None, names = ['Device', 'Item', 'Flow'])
        # Creating a DataFrame from data
	df = data[['Device', 'Item', 'Flow']]
	device = df.Device
	item = df.Item
	flow = df.Flow

	#Grouping the number of collected items from devices
	Collected_Item_Device = sorted([d for d in device], reverse=True)  # degree sequence
	Items_Count_Device = collections.Counter(Collected_Item_Device)
	V_Device, C_Items = zip(*Items_Count_Device.items())

	xindexs = nb_items
	#yindexs = nb_devices
	#Item_Index = np.arange(len(xindexs))

	#plt.barh(V_Device, C_Items)
	plt.plot(V_Device, C_Items)
	plt.xticks(ticks=xindexs, labels=xindexs)
	#plt.yticks(ticks=yindexs, labels=yindexs)

	plt.title("Collected Telemetry Items")
	plt.xlabel("Number of collected Ttems")
	plt.ylabel("Forwarding Devices")
	plt.tight_layout()

	#saving the graph
	plt.savefig('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Collected_Items_Device.png', format="PNG")
	plt.close()


def Plot_Flow_Items(filename, nb_flows, nb_items) : 
	data = pd.read_csv(filename, sep=',', header = None, names = ['Device', 'Item', 'Flow'])
        # Creating a DataFrame from data
	df = data[['Device', 'Item', 'Flow']]
	device = df.Device
	item = df.Item
	flow = df.Flow

	#Grouping the number of collected items by each flow
	Collected_Item_Flow = sorted([f for f in flow], reverse=True)  # degree sequence
	Items_Count_Flow = collections.Counter(Collected_Item_Flow)
	U_Flow, C_Items = zip(*Items_Count_Flow.items())

	xindexs = nb_items
	#yindexs = nb_flows
	#Item_Index = np.arange(len(U_Flow))

	plt.barh(U_Flow, C_Items)
	plt.xticks(ticks=xindexs, labels=xindexs)
	#plt.yticks(ticks=yindexs, labels=yindexs)

	plt.title("Collected Telemetry Items")
	plt.xlabel("Number of collected Ttems")
	plt.ylabel("Active Network flows")
	plt.tight_layout()

	#saving the graph
	plt.savefig('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Collected_Items_Flow.png', format="PNG")
	plt.close()


def Plot_Bar_Flow_Items(nb_used_flows, nb_collected_item) : 

	x_axe = nb_used_flows
	y_axe = nb_collected_item

	plt.bar(x_axe, y_axe)

	plt.title("Collected Telemetry Items")
	plt.xlabel("Number of collected Ttems")
	plt.ylabel("Active Network flows")
	plt.tight_layout()

	#saving the graph
	plt.savefig('/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Collected_Items_Grouped_Flow.png', format="PNG")
	plt.close()


