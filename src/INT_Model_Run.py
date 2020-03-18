
from INT_Model_Data_Modules import Constructing_and_Loading_Network, get_subsets, Loading_Network_Flows, Loding_Telemetry_Items, Loding_Monitoring_Applications, Spatial_And_Temporal_Dependencies_Requirements, Plot_Device_Items, Plot_Flow_Items
from INT_Model import INT_Model
from Save_OutPut import Save_OutPut_csv, Save_OutPut_txt
from INT_Model_Save_Solution import INT_Save_Solution



# Loading data from external files

number_of_devices = 50
embeded_items = [0,1,2,3,4,5,6,7]
number_of_telemetry_items = 8
size_of_telemetry_items = [2,2,2,2,2,2,2,2]
number_of_monitoring_application = 4
spatial_requirements = [[0,1], [2,3], [4,5], [6,7]]
number_of_flows = 50




# Loading the Network Infrastructure
network_infrastricture_file = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Network_Data/Barabasi_Albert/Barabasi_5_50_3.csv'
#network_infrastricture_file = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Network_Data/Erdos_Renyi/Erdos_50_0.15.csv'

# Loading the networks flows endpoints and capacities
active_network_flows_file = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/Flow_Data/Flow_Data_50_50.csv'


#Constructing_and_Loading_Network(filename, number_of_devices, embeded_items)
(D,G) = Constructing_and_Loading_Network(network_infrastricture_file, number_of_devices, embeded_items)

#Loading_Network_Flows(filename, number_of_flows)
(F, S, E, Kf) = Loading_Network_Flows(active_network_flows_file, number_of_flows)

#Loding_Telemetry_Items(number_of_telemetry_items, size_of_telemetry_items)
(V, Size) = Loding_Telemetry_Items(number_of_telemetry_items, size_of_telemetry_items)

#Loding_Monitoring_Applications(number_of_monitoring_application, spatial_requirements)
(M, R) = Loding_Monitoring_Applications(number_of_monitoring_application, spatial_requirements)

#Spatial_And_Temporal_Dependencies_Requirements
(PR, Rs, idxs_Rs, Rt, idxs_Rt, TT, HH) = Spatial_And_Temporal_Dependencies_Requirements(M,R)

#param = (number_of_flows, D,G, F, S, E, Kf, V, Size, M, R, PR, Rs, idxs_Rs, Rt, idxs_Rt, TT, HH)

(model, s_b, s, y) = INT_Model(number_of_devices, number_of_flows, D,G, F, S, E, Kf, V, Size, M, R, PR, Rs, idxs_Rs, Rt, idxs_Rt, TT, HH)

# solving the model 
model.optimize()


INT_Save_Solution(number_of_devices, number_of_flows, M, D, Rs, V, F, s_b, s, y)
#Plot_Device_Items(file_to_save_collected_items, D, V)
#Plot_Flow_Items(file_to_save_collected_items, F, V)





