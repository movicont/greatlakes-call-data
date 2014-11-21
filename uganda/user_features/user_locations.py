import csv, collections, pickle, operator, math

class User:
	# Get the tower latitude/longitudes
	sites_r = csv.reader(open("../../output/mtnugsites.csv"), delimiter=',')
	phone_towers = {}
	cntr = 0
	for line in sites_r:
		if cntr != 0:
			phone_towers[line[1]] = (float(line[2]), float(line[3]))
		cntr += 1
	
	def __init__(self, uid, location, date):
		self.uid = uid
		self.locmap = {}
		self.locmap[date] = [location]


def record_user_locs(userid = '13707895'):
	# Open user location files
	f = csv.reader(open("../../output/users_mobility.csv"), delimiter=',')
	i = 0
	user_locs = {}
	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		user_locs[line[0]] = (line[2], line[3])

	# Process the CDR file
	users = {}
	full_users = set()
	f = csv.reader(open("../../applab_new_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect = 0
	for line in f:
		#print line
		line = map(lambda x: x.strip(), line)
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		#if i == 1000000: break
		try:
			sender, receiver, date = line[0], line[1], line[2]
			#if sender not in full_users:
			if sender not in users and sender == userid:
				if receiver in user_locs:
					uniquect += 1
					#full_users.add(sender)
					#if uniquect % denom - round == 0:
					users[sender] = User(sender, user_locs[receiver], date)
			else:
				if sender in users and sender == userid and receiver in user_locs:
					users[sender].locmap[date].append(user_locs[receiver])
		except: pass
	print users

	# Store all recorded metrics in csv
	w = open("../../output/calls_spider.csv", 'w')
	w.write("uid,date,fromlat,fromlon,tolat,tolon,times\n")
	i = 0
	for uid, user in users.items():
		i += 1
		if i % 100000 == 0: print "processed", i, "users"
		try:
			for date, locs in user.locmap.items():
				for loc in locs:
					w.write("%s,%s,%s,%s,%s,%s\n" % (uid, user_locs[uid][0], user_locs[uid][1], loc[0], loc[1], times))
		except: pass
	w.close()

record_user_locs()