import numpy as np
import pandas as pd
from collections import defaultdict
from typing import Set, List
from typing import Tuple
from itertools import product
import networkx as nx
from sys import stdout as out
import sys
from mip import Model, xsum, maximize, BINARY, ConstrsGenerator, CutPool





#reading data from external file

network_data_file = "/home/tbn/Brazil_note/These_Telemetry/Implementation_INT/INT_Python/Small_Example_Nodes.csv"
network_data = pd.read_csv(network_data_file, sep=',', header = None, names = ['ori', 'dst'])

#displaying the first line
network_data.head()
#df = network_data[['ori','dst','cap']]
df = network_data[['ori','dst']]

# saving data in form we know
src_node = df.ori
dst_node = df.dst

S=[0, 4, 6, 3, 6]
E=[9, 5, 8, 6, 9]
Kf = {0:4, 1:6, 2:2, 3:8, 4:4}


## Defining the set
# Set of devices
nb_devices=10
D=[d for d in range(nb_devices)]

# Set of flows
nb_flows=5
F=[f for f in range(nb_flows)]

# Set of telemetry items
nb_telemetry=8
V=[v for v in range(nb_telemetry)]

# size of telemetries
Size = {V[0]: 2, V[1]: 2, V[2]: 2, V[3]: 2, V[4]: 2, V[5]: 2, V[6]: 2, V[7]: 2}

#set of Monitoring Applications
nb_Mon_App=4
M = [m for m in range(nb_Mon_App)]

R = {
M[0]: [0, 1],
M[1]: [2, 3],
M[2]: [4, 5],
M[3]: [6, 7]}



  #####################################################################################

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

  #####################################################################################


PR={}

for m in M :
  PR[m] = get_subsets(set(R[m]))
  del PR[m][0]


#spatial dependency
Rs = {}
for m in M :
 Rs[m] = PR[m]
 print("Rs", Rs)

# index for set Rs
idxs_Rs = {}
for m in M :
 idxs_Rs[m] = list(range(len(Rs[m])))

#temporal dependency
Rt = {}
for m in M :
 Rt[m] = Rs[m]
 print("Rt", Rt)

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





# creating graph

G = nx.Graph()
G.add_nodes_from(D)
no_link = len(src_node)
links = [i for i in range(no_link)]
for i in links :
 G.add_edge(src_node[i], dst_node[i])

G.nodes

"""# adding atribute to the a single node
G.nodes[2]['Items'] = [1,2,3]
# accessing the atributes
G.nodes[2]['Items']"""

#adding same telemetry Items to all nodes
for d in D :
   G.nodes[d]['Items'] = [0,1,2,3,4,5,6,7]


# creating links
links=list()
for i in range(no_link) :
  links.append((src_node[i],dst_node[i]))



# Creating the model
#model = Model(sense=MAXIMIZE, solver_name=Gurobi) # use GRB for Gurobi
model = Model() # it choose automaticaly the model

#defining the variable in correct way
s_b = [[[model.add_var(name='s_b({},{},{})'.format(m,d,P), var_type=BINARY) for P in range(len(Rs[m]))] for d in D] for m in M]

t_b = [[model.add_var(name='t_b({},{})'.format(m,P), var_type=BINARY) for P in range(len(Rt[m]))] for m in M]

# binary variables indicating if arc (i,j) is used on the route or not
#x = {a: model.add_var('x({},{},{})'.format(a[0], a[1],f), var_type=BINARY) for a in G.edges for f in F}

x = [[[model.add_var(name='x({},{},{})'.format(i,j,f), var_type=BINARY) for f in F] for j in D] for i in D]

y = [[[model.add_var(name='y({},{},{})'.format(d,v,f), var_type=BINARY) for f in F] for v in V] for d in D]

s = [[[model.add_var(name='s({},{},{})'.format(m,d,P)) for P in range(len(Rs[m]))] for d in D] for m in M]

t = [[model.add_var(name='t({},{})'.format(m,P)) for P in range(len(Rt[m]))] for m in M]

ttt = [[model.add_var(name='ttt({},{})'.format(i,f)) for f in F] for i in D]


# objective function : maximise spatial and temporal dependencies
model.objective = maximize(xsum(s_b[m][d][P] for m in M for d in D for P in range(len(Rs[m]))) + xsum(t_b[m][P] for m in M for P in range(len(Rt[m]))))


# constraints


#starting of the flow
for f in F :
 model += xsum(x[S[f]][j][f] for j in G.neighbors(S[f])) + xsum(x[j][S[f]][f] for j in G.neighbors(S[f])) == 1

#ending of the flow
for f in F :
 model += xsum(x[i][E[f]][f] for i in G.neighbors(E[f])) + xsum(x[E[f]][i][f] for i in G.neighbors(E[f])) == 1


#flow conservation
for f in F :
 for i in D :
   if (i!= S[f] and i!=E[f]) :
      model += xsum(x[j][i][f] for j in G.neighbors(i)) - xsum(x[i][j][f] for j in G.neighbors(i)) == 0



# single telemetry is collected by a single flow
for d in D :
#for (i,d) in G.edges :
   for v in G.nodes[d]['Items'] :
      for f in F :
         model += y[d][v][f] <= xsum(x[i][d][f] for i in G.neighbors(d))



## variable cycle

for (i, j) in G.edges :
   for f in F :
      model += ttt[j][f] >= ttt[i][f]+1 - len(D)*(1-x[i][j][f])

#removing subtour of size two
for (i,j) in G.edges :
  for f in F :
     model += x[i][j][f] + x[j][i][f] <=1


#exch flow does not excced it capacity
for f in F :
 model += xsum(y[d][v][f]*Size[v] for d in D for v in G.nodes[d]['Items']) <= Kf[f]

# counting the spatial dependency
for m in M :
   for d in D :
      for p in range(len(Rs[m])) :
         model += s[m][d][p] == xsum(y[d][v][f] for v in Rs[m][p] for f in F)
#          print("Rs[m][p] = ", Rs[m][p])

# print("V = ", V)
# sys.exit()

# counting temporal dependency
for m in M :
   for P in range(len(Rt[m])) :
#      print("P", P)
      if HH[P] > TT[P] :
         print("encore")
         model += t[m][P] == xsum(y[d][v][f] for d in D for v in Rt[m][P] for f in F)
#         print("v", Rs[m][idxs_Rs[m][P]])



#spatial dependency
for m in M :
   for d in D :
      for P in range(len(Rs[m])) :
#         for P1 in idxs_Rs[m] :
            model += s_b[m][d][P] <= s[m][d][P]/len(Rs[m][P])
#          model += s_b[m][d][P1] <= s[m][d][P]/len(Rs[m])




#temporal dependency
for m in M :
  for P in range(len(Rt[m])) :
#     for P1 in idxs_Rt[m] :
        model += t_b[m][P] <= t[m][P]/len(Rt[m][P])
#     model += t_b[m][P1] <= t[m][P]/len(Rt[m])



model.write('model3.lp')
#model.lazy_constrs_generator = SubTourLazyGenerator(x)
model.optimize()

# displaying the result of variable in terminal


#display x
print('Path of Flows: ')
for f in F :
   for i in D :
      for j in D :
#     for f in F :
        if x[i][j][f].x >= 0.99:
        #if x[i][j][f]== 1:
          print('({},{},{})'.format(i,j,f))
print('Makespan = {} '.format(model.objective_value))
