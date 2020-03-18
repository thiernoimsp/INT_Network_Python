
from Save_OutPut import Save_OutPut_csv

def INT_Save_Solution(number_of_devices, number_of_flows, M, D, Rs, V, F, s_b, s, y) :
	file_to_save_spatial = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/INT_Model_Solution/Sapatial_dependency_' + str(number_of_devices) + '_' + str(number_of_flows) + '.csv'
	print('spatial Dependencies : ')
	Satisfied_Spatial_Dependencies = list()
	for m in M :
		for d in D :
			for P in range(len(Rs[m])) :
				if s_b[m][d][P].x >= 0.99:
					print('({},{},{})'.format(m,d,P), s_b[m][d][P].x)
					data = [m,d,P]
					Satisfied_Spatial_Dependencies.append(data)
	Save_OutPut_csv(file_to_save_spatial, Satisfied_Spatial_Dependencies)

	#file_to_save_temporal = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Sapatial_dependency' + '_' + str(number_of_flows) + '.csv'

	file_to_save_nb_spatial = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/INT_Model_Solution/Nb_Sapatial_dependency_' + str(number_of_devices) + '_' + str(number_of_flows) + '.csv'
	print('number of spatial : ')
	Nb_Satisfied_Spatial_Dependencies = list()
	for m in M :
		for d in D :
			for P in range(len(Rs[m])) :
				if s[m][d][P].x >= 0.99:
					print('({},{},{})'.format(m,d,P), s[m][d][P].x)
					data = [m,d,P,s[m][d][P].x]
					Nb_Satisfied_Spatial_Dependencies.append(data)
	Save_OutPut_csv(file_to_save_nb_spatial, Nb_Satisfied_Spatial_Dependencies)

	file_to_save_collected_items = '/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/Organazed_Tasks/Generating_Instances/INT_Model_Solution/Collected_Items_' + str(number_of_devices) + '_' + str(number_of_flows) + '.csv'
	print('Collected Items : ')
	Collected_Items = list()
	for d in D :
		for v in V :
			for f in F :
				if y[d][v][f].x >= 0.99:
					print('({},{},{})'.format(d,v,f), y[d][v][f].x)
					data = [d,v,f]
					Collected_Items.append(data)
	Save_OutPut_csv(file_to_save_collected_items, Collected_Items)
