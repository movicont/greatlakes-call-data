from datetime import datetime
import csv

class User:
	def __init__(self, uid, date, t, loc, region):
		self.uid = uid
		self.workday = 0.0
		self.other = 0.0
		self.calls = 0.0
		self.addTime(date, t, loc, region)
		self.location = ""
	
	def addTime(self, date, t, loc, region):
		t = t.split(':')
		self.calls += 1
		if int(t[0]) >= 9 and int(t[0]) <= 18 and date.weekday() == True:
			self.workday += 1
		else:
			self.other += 1
		self.location = (loc, region)

def process():
	users = {}
	f = csv.reader(open("../applab_new_6.csv", 'rb'), delimiter=',')
	i = 0
	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		try:
			sender, receiver, date, t, duration, cost, location, region = map(lambda x: x.strip(), line)
			date = datetime.fromtimestamp(time.mktime(time.strptime(d, "%d-%b-%y")))
			if sender not in users: users[sender] = User(sender, date, t, loc, region)
			else: users[sender].addTime(date, t, loc, region)
			if receiver not in users: users[receiver] = User(receiver, date, t, loc, region)
			else: users[receiver].addTime(date, t, loc, region)
		except: pass
	w = open("../output/user_time.csv", 'wb')
	w.write("userid,workday,other,calls,location,region\n")
	for u in users:
		w.write("%s,%s,%s,%s,%s,%s\n" % (u.uid, u.workday, u.other, u.calls, u.location[0], u.location[1]))
	w.close()

process()