# Generating the network infrastructure and the endpoints of active network flows
from INT_Generating_Data_Modules import  Generating_Flows_Data, INT_Barabasi, INT_Erdos_Renyi, plot_deg_dist


# Seting flow information
number_of_devices = 50
number_of_flows = 200
min_size = 1
max_size = 5

#Generating_Flows_Data(number_of_flows, number_of_devices, min_size, max_size)


# Generating Barabasi graph
init_nodes = 5
final_nodes = 50 
m_parameter = 3

#Barabasi_G = INT_Barabasi(init_nodes, final_nodes, m_parameter)


# Genereting Erdos Renyi Graph
nombre_of_nodes = 50
probability_to_connect = 0.15

#Erdos_G = INT_Erdos_Renyi(nombre_of_nodes, probability_to_connect)


# Degree distribution
file_to_save_barabasi_distribution = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Plots/Degree_Distribution_barabasi_' + str(init_nodes) + '_' + str(final_nodes) + '_' + str(m_parameter) + '.png'

file_to_save_erdos_distribution = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Plots/Degree_Distribution_Erdos_' + str(nombre_of_nodes) + '_' + str(probability_to_connect) + '.png'

#plot_deg_dist(Barabasi_G, file_to_save_barabasi_distribution)
#plot_deg_dist(Erdos_G, file_to_save_erdos_distribution)


