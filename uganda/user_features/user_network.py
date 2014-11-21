import networkx as nx
import csv
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def process_data(denom=100000, round=0):
	f = csv.reader(open("../applab_new_6.csv", 'rb'), delimiter=',')
	db = nx.DiGraph()
	full_users = set()
	i = 0
	uniquect = 0
	for line in f:
		if i % 100000 == 0 : print "processed", i, "lines"
		if i == 1000: break
		sender, receiver, date, time, duration, cost, location, region = map(lambda x: x.strip(), line)
		if sender not in full_users:
			uniquect += 1
			full_users.add(sender)
			if uniquect <= 2: #% denom - round == 0:
				db.add_node(sender)
				if db.has_node(receiver) == False:
					db.add_node(receiver)
		else:
			if db.has_node(receiver) == False:
				db.add_node(receiver)

		if db.has_edge(sender, receiver):
			db[sender][receiver]['weight'] += int(duration)
		else:
			db.add_edge(sender, receiver, weight=int(duration))
		i+=1
	#pickle.dump(db, open("users_networkx.p" % str(round), "wb"))
	#print "degree assortativity coeff:", nx.degree_assortativity_coefficient(db)
	#print "average degree connectivity:", nx.average_degree_connectivity(db)
	#	print "k nearest neighbors:", nx.k_nearest_neighbors(db)
	print "calculating deg cent"
	deg_cent = nx.degree_centrality(db) #sorted(nx.degree_centrality(db).items(), key=lambda x: x[1])
	print "calculating in deg cent"
	in_deg_cent = nx.in_degree_centrality(db) #sorted(nx.in_degree_centrality(db).items(), key=lambda x: x[1])
	print "calculating out deg cent"
	out_deg_cent = nx.out_degree_centrality(db) #sorted(nx.out_degree_centrality(db).items(), key=lambda x: x[1])
	print "closeness cent"
	closeness_cent = nx.closeness_centrality(db) #sorted(nx.closeness_centrality(db).items(), key=lambda x: x[1])
	#print "betweenness cent"
	#btwn_cent = nx.betweenness_centrality(db) #sorted(nx.betweenness_centrality(db).items(), key=lambda x: x[1])
	print "done"
	w = open("../output/user_network_stats.csv", 'w')
	w.write("uid,deg_cent,in_deg_cent,out_deg_cent,closeness_cent,btwn_cent\n")
	for user in deg_cent.keys():
		try:
			w.write("%s,%s,%s,%s,%s\n" % (user, deg_cent[user], in_deg_cent[user], out_deg_cent[user], closeness_cent[user]))
		except: pass
	w.close()
	print "drawing..."
	nx.draw(db)
	plt.savefig("path.pdf")
	print "done!"
	print "edge betweenness centrality:", nx.edge_betweenness_centrality(db)
	print "communicability:", nx.communicability(db)
	print "communicability centrality:", nx.communicability_centrality(db)
	
process_data()
