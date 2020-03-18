

from mip import Model, xsum, maximize, BINARY, ConstrsGenerator, CutPool

def INT_Model(number_of_devices, number_of_flows, D,G, F, S, E, Kf, V, Size, M, R, PR, Rs, idxs_Rs, Rt, idxs_Rt, TT, HH) :
	# Creating the model
	model = Model() # it choose automaticaly the model

	# Defining spatial and temporal dependencies variables
	s_b = [[[model.add_var(name='s_b({},{},{})'.format(m,d,P), var_type=BINARY) for P in range(len(Rs[m]))] for d in D] for m in M]
	t_b = [[model.add_var(name='t_b({},{})'.format(m,P), var_type=BINARY) for P in range(len(Rt[m]))] for m in M]

	# binary variables indicating if arc (i,j) is used on the route or not
	#x = {a: model.add_var('x({},{},{})'.format(a[0], a[1],f), var_type=BINARY) for a in G.edges for f in F}
	x = [[[model.add_var(name='x({},{},{})'.format(i,j,f), var_type=BINARY) for f in F] for j in D] for i in D]

	# variable for collected items
	y = [[[model.add_var(name='y({},{},{})'.format(d,v,f), var_type=BINARY) for f in F] for v in V] for d in D]

	# variable for counting spatial and temporal dependencies
	s = [[[model.add_var(name='s({},{},{})'.format(m,d,P)) for P in range(len(Rs[m]))] for d in D] for m in M]
	t = [[model.add_var(name='t({},{})'.format(m,P)) for P in range(len(Rt[m]))] for m in M]

	# polynomial variable for eleminating cycles
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

	# collected items must belong to the path of the network flow f
	for d in D : #ori
		for v in G.nodes[d]['Items'] :
			for f in F :
				model += y[d][v][f] <= xsum(x[i][d][f] for i in G.neighbors(d)) #ori


	# single telemetry is collected by a single flow
	for d in D : #ori
		for v in G.nodes[d]['Items'] :
			model += xsum(y[d][v][f] for f in F) <= 1

	# removing cycles
	for (i, j) in G.edges :
		for f in F :
			model += ttt[j][f] >= ttt[i][f]+1 - len(D)*(1-x[i][j][f])

	#removing subtour of size two
	for (i,j) in G.edges :
		for f in F :
			model += x[i][j][f] + x[j][i][f] <=1

	# each flow does not excced it capacity
	for f in F :
		model += xsum(y[d][v][f]*Size[v] for d in D for v in G.nodes[d]['Items']) <= Kf[f]

	# counting the spatial dependency
	for m in M :
		for d in D :
			for p in range(len(Rs[m])) :
				model += s[m][d][p] == xsum(y[d][v][f] for v in Rs[m][p] for f in F)

	# counting temporal dependency
	for m in M :
		for P in range(len(Rt[m])) :
			if HH[P] > TT[P] :
				print("encore")
				model += t[m][P] == xsum(y[d][v][f] for d in D for v in Rt[m][P] for f in F)

	# satisfied spatial dependency
	for m in M :
		for d in D :
			for P in range(len(Rs[m])) :
				model += s_b[m][d][P] <= s[m][d][P]/len(Rs[m][P])

	# satisfied temporal dependency
	for m in M :
		for P in range(len(Rt[m])) :
			model += t_b[m][P] <= t[m][P]/len(Rt[m][P])


	# saving the model in lp format
	model.write('INT_Model' + '_' + str(number_of_devices) + '_' + str(number_of_flows) + '.lp')
	return (model, s_b, s, y)
