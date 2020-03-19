# Orchestrating In-Band Network Telemetry Data Plane
Python version of the INT

## Requirements
* Python3+
* Python-MIP (Install using : pip install mip)
* Solver (Cbc, Glpk, Gurobi, Cplex ... etc)

## Organization
The project is organized as follow :
1) instances : contains the generated instance for testing the model(i.e. the network infrastructure and the flows information : endpoints and capacities).
2) out : contains the outputs of the model in text files and figures(i.e. Spatial Requirements Satisfied, Collected Telemetry Items)
3) src : contains the source code.


## Description of the source code files
1) INT_Generating_data_Modules.py : contains python functions for generation random network infrastructures following Barabasi Albert model or Erdos Renyi model and the endpoints for each active network flow and it corresponding capacity.
2) INT_Generating_data_Run.py : is the main file for running the INT_Generating_data_Modules.py file.
3) INT_Model.py : contains the Implementation of the mathematical model.
4) INT_Model_Data_Modules.py : contains python functions for loading the data used for running the model(i.e network infrastructure, active network flows, Monitoring Applications, telemetry items ... etc).
5) INT_Model_Run : is the main file for running the model.
