import csv

class User:
	def __init__(self, mobnum, startdate):
		self.mobnum = mobnum
		self.startdate = startdate
		self.enddate = None
		self.cost = 0
		self.duration = 0
		self.calls = 0
		#self.in_degree = set()
		#self.out_degree = set()
		#self.degree = set()

def getstats():
	users = {}
	f = csv.reader(open("../applab_5.txt", 'rb'), delimiter=',')
	#w = open("../output/users_agg_one_percent.csv", 'w')
	i = 0
	uniquect = 0
	for line in f:
		i += 1
		if i % 10000 == 0:
			print "processed", i, "lines and", uniquect, "users"
		try:
			sender, receiver, date, cost, duration = line[0], line[1], line[2], line[3], line[4]
			if sender not in users and i % 7000 == 0:
				users[sender] = User(sender, date)
				uniquect += 1
			if receiver not in users and i % 7000 == 0:
				users[receiver] = User(receiver, date)
				uniquect += 1
			if sender in users:
			#	users[sender].degree.add(receiver)
			#	users[sender].out_degree.add(receiver)
				users[sender].cost += int(cost)
				users[sender].duration += int(duration)
				users[sender].calls += 1
			if receiver in users:
			#	users[receiver].degree.add(sender)
			#	users[receiver].in_degree.add(sender)
				users[receiver].cost += int(cost)
				users[receiver].duration += int(duration)
				users[receiver].calls += 1
		except: pass
	print "total users:", len(users.keys())
	#"""w.write("mobile,start,degree,in_degree,out_degree,send_count,receive_count\n")
	#for user in users.values():
	#	w.write("%s,%s,%s,%s,%s,%s,%s\n" % (user.mobnum, user.startdate, user.degree,\
	#	user.in_degree, user.out_degree, user.send_count, user.receive_count))
	#w.close()"""

	"""w.write("mobile,start,send_count,receive_count\n")
	for user in users.values():
		w.write("%s,%s,%s,%s\n" % (user.mobnum, user.startdate, user.send_count, user.receive_count))
	w.close()
	"""
	"""w.write("mobile,start,degree,in_degree,out_degree\n")
	for user in users.values():
		w.write("%s,%s,%s,%s,%s\n" % (user.mobnum, user.startdate, len(user.degree), \
		len(user.in_degree), len(user.out_degree)))
	w.close()"""

	w = open("../output/users_cost_dur.csv", 'w')
	w.write("cost,duration,calls,cost_per_min,cost_per_call,call_len\n")
	for user in users.values():
		try:
			w.write("%s,%s,%s,%s,%s,%s\n" % (user.cost,user.duration,user.calls,\
			float(user.cost)/user.duration,float(user.cost)/user.calls,float(user.duration)/user.calls))
		except: pass
	w.close()
	
getstats()