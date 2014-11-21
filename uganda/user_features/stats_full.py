"""

Calculates basic statistics like user degree (in, out and total), # of calls, and duration.
Stores information about each user in a csv file (users_full_x.csv), with one line per user.

Processes a fraction of total users at a time:
  getstats(denom, round), where
	1/denom = percentage of users to process at a time
	round   = the nth x% of users

"""

import csv, collections, pickle, os

class User:
	def __init__(self, mobnum, startdate):
		self.mobnum = mobnum

		self.startdate = startdate
		self.enddate = None
		self.cost = 0
		self.duration = 0
		self.calls = 0
		self.in_degree = set()
		self.out_degree = set()
		self.degree = set()

def getstats(denom=20, round=8):
	#round = denom
	users = {}
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect, actual = 0, 0
	if os.path.isfile("users.p"):
		users = pickle.load(open("users.p", "rb"))
	else:
		full_users = set()
		for line in f:
			i += 1
			if i % 1000000 == 0:
				print "processed", i, "lines and", uniquect, "users", " and actual users", actual
			#if i == 3000000: break
			try:
				sender, receiver, date, time, duration, cost, location, region = line
				if sender not in full_users:
					uniquect += 1
					full_users.add(sender)
					if uniquect % denom - round == 0:
						actual += 1
						users[sender] = User(sender, date)
				if receiver not in full_users:
					uniquect += 1
					full_users.add(receiver)
					if uniquect % denom - round == 0:
						actual += 1
						users[receiver] = User(receiver, date)
				if sender in users:
					users[sender].degree.add(receiver)
					users[sender].out_degree.add(receiver)
					users[sender].cost += int(cost)
					users[sender].duration += int(duration)
					users[sender].calls += 1
				if receiver in users:
					users[receiver].degree.add(sender)
					users[receiver].in_degree.add(sender)
					users[receiver].cost += int(cost)
					users[receiver].duration += int(duration)
					users[receiver].calls += 1
			except: pass
	print "total users:", len(users.keys()), uniquect
	#pickle.dump(users, open("users_%s.p" % str(round+1), "wb"))
	
	w = open("../output/users_full_%s.csv" % (round+1), 'w')
	w.write("mobile,start,degree,in_degree,out_degree,send_count,receive_count,cost,duration,calls\n")
	i = 0
	for user in users.values():
		if i % 100000 == 0: print "written line", i
		i += 1
		w.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (user.mobnum, user.startdate, len(user.degree),\
		len(user.in_degree), len(user.out_degree), user.cost, user.duration, user.calls))
	w.close()

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

	"""w = open("../output/users_cost_dur.csv", 'w')
	w.write("cost,duration,calls,cost_per_min,cost_per_call,call_len\n")
	for user in users.values():
		try:
			w.write("%s,%s,%s,%s,%s,%s\n" % (user.cost,user.duration,user.calls,\
			float(user.cost)/user.duration,float(user.cost)/user.calls,float(user.duration)/user.calls))
		except: pass
	w.close()"""
	
getstats()
