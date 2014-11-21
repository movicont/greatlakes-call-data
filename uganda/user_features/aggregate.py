"""

Aggregates basic stats per day (duration, cost, # calls, inbound, outbound etc)

Easier on the memory since the # of days is much more finite than the # of users (6 million).

"""

import csv, time
from datetime import datetime

class EachDate:
	def __init__(self, d, duration, cost):
		self.date = datetime.fromtimestamp(time.mktime(time.strptime(d, "%d-%b-%y")))
		self.duration = int(duration)
		self.cost = int(cost)
		self.calls = 1

	def addInfo(self, duration, cost):
		self.duration += int(duration)
		self.cost += int(cost)
		self.calls += 1

class HourBlock:
	def __init__(self, d, dur, cost):
		self.duration = int(dur)
		self.cost = int(cost)
		self.calls = 1
	def addInfo(self, dur, cost):
		self.duration += int(dur)
		self.cost += int(cost)
		self.calls += 1

def aggregate_by_date():
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	dates = {}
	i = 0
	uniqdays = 0
	for line in f:
		i+=1
		if i % 10000 == 0: print "processed line", i, "and", uniqdays, "days"
		try:
			sender, receiver, date, time, duration, cost, location, region = line
			if date not in dates:
				uniqdays += 1
				dates[date] = EachDate(date, duration, cost, location, region)
			else:
				dates[date].addInfo(duration, cost)
		except: pass
	
	w = open("../output/agg_by_date.csv", 'w')
	w.write("date,duration,cost,calls,is_weekend\n")
	for key, d in dates.items():
		w.write("%s,%s,%s,%s,%s\n" % (key, d.duration, d.cost, d.calls,\
				d.date.weekday() == 5 or d.date.weekday() == 6))
	w.close()

class User:
	def __init__(self, uid):
		self.uid = uid
		self.duration = 0
		self.cost = 0
		self.calls = 0
		self.inbound = 0
		self.outbound = 0

	def addCall(self, duration, cost, isIn):
		self.duration += int(duration)
		self.cost += int(cost)
		self.calls += 1
		if isIn == True: self.inbound += 1
		else: self.outbound += 1
	
def aggregate_by_user():
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	users = {}
	i = 0
	for line in f:
		i+=1
		if i % 100000 == 0: print "processed line", i
		#if i == 100000: break
		try:
			sender, receiver, date, ti, duration, cost, location, region = line
			if sender not in users:
				users[sender] = User(sender)
			if receiver not in users:
				users[receiver] = User(receiver)
			#users[sender].addCall(duration, cost, False)
			#users[receiver].addCall(duration, cost, True)
		except: pass
	
	w = open("../output/agg_by_user.csv", 'w')
	w.write("uid,duration,cost,mean_duration,mean_cost,inbound,outbound,calls\n")
	for key, user in users.items():
		avg_call_length = user.duration/user.calls
		avg_call_cost = user.cost/user.calls
		w.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (user.uid, user.duration, user.cost, avg_call_length, avg_call_cost, user.inbound, user.outbound, user.calls))
	w.close()
	
aggregate_by_user()