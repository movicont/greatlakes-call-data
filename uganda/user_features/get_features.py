"""

Collect basic features about the user that can be used to predict attributes.
  features collected: # of incoming/outgoing, workday/nonworkday, weekend/weekday calls
Stores features in a csv file with the user id + features

"""

import csv, collections, pickle, os, time
from datetime import datetime

class User:
	def __init__(self, mobnum):
		self.mobnum = mobnum
		#self.incoming_cost = 0
		#self.outgoing_cost = 0
		#self.incoming_dur = 0
		#self.outgoing_dur = 0
		self.incoming = 0
		self.outgoing = 0
		self.workday = 0
		self.nonworkday = 0
		self.weekend = 0
		self.weekday = 0
		
	def addData(self, inc, out, dur, cost, date, t):
		if int(inc) == 1:
			self.incoming += int(inc)
			#self.incoming_cost += int(cost)
			#self.incoming_dur += int(dur)
		if int(out) == 1:
			self.outgoing += int(out)
			#self.outgoing_cost += int(cost)
			#self.outgoing_dur += int(dur)
		t = t.split(':')
		if int(t[0]) >= 9 and int(t[0]) <= 18 and date.weekday() < 5:
			self.workday += 1
		else:
			self.nonworkday += 1
		if date.weekday() < 5:
			self.weekday += 1
		else:
			self.weekend += 1

def getstats(denom=20, round=1):
	users = {}
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect, actual = 0, 0
	wf = open("temp", 'w', 0)
	if os.path.isfile("users.p"):
		users = pickle.load(open("users.p", "rb"))
	else:
		full_users = set()
		for line in f:
			i += 1
			if i % 100000 == 0:
				wf.write("processed " + str(i) + " lines and " + str(uniquect) + " users\n")
				#print "processed", i, "lines"
			#if i == 20000000: break
			try:
				sender, receiver, date, ti, duration, cost, location, region = line
				date = datetime.fromtimestamp(time.mktime(time.strptime(date, "%d-%b-%y")))
				if sender not in full_users:
					uniquect += 1
					full_users.add(sender)
					#if uniquect % denom - round == 0:
					users[sender] = User(sender)
				if receiver not in full_users:
					uniquect += 1
					full_users.add(receiver)
					#if uniquect % denom - round == 0:
					users[receiver] = User(receiver)
				if sender in users:
					users[sender].addData(0, 1, duration, cost, date, ti)
				if receiver in users:
					users[receiver].addData(1, 0, duration, cost, date, ti)
			except:
				print line
	#wf.write("total users:" len(users.keys()), uniquect
	wf.close()
	#pickle.dump(users, open("users_%s.p" % str(round), "wb"))
	
	w = open("../output/users_features_%s.csv" % round, 'w')
	w.write("mobile,incoming,outgoing,workday,nonworkday,weekday,weekend\n")
	i = 0
	for user in users.values():
		if i % 100000 == 0: print "written line", i
		i += 1 #user.incoming_cost,user.incoming_dur,\
		#user.outgoing_cost,user.outgoing_dur,\
		w.write("%s,%s,%s,%s,%s,%s,%s\n" % (user.mobnum, user.incoming,\
											user.outgoing,\
											user.workday, user.nonworkday, user.weekday, user.weekend))
	w.close()

getstats()