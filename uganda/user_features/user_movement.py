"""

Calculates various user mobility metrics, including:
- center of mass: this is the average of all the latitude and longitudes of the user's locations, weighted by frequency
- radius of gyration: how far the user deviates from the center of mass
- distance travelled: total distance covered by the user
- velocity: how quickly the user travels

"""

from datetime import datetime
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
	
	def __init__(self, uid, date, tower):
		self.uid = uid
		self.locmap = {}
		if tower != '':
			self.locmap[date] = [tower]
		self.coms = {}
			
	"""
		Stores the center of mass as a tuple (lat, lon)
	"""
	def calc_com(self):
		for date, locs in self.locmap.items():
			sumlat, sumlon = 0.0, 0.0
			count = 0
			for loc in locs:
				if loc in User.phone_towers:
					count += 1
					sumlat += User.phone_towers[loc][0]
					sumlon += User.phone_towers[loc][1]
			if count != 0:
				self.coms[date] = (sumlat/count, sumlon/count)

			
def record_user_locs(denom = 100000, round = 0):
	# Process the CDR file
	users = {}
	full_users = set()
	f = csv.reader(open("../../applab_new_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect = 0
	for line in f:
		line = map(lambda x: x.strip(), line)
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		if i == 10000000: break
		try:
			sender, date, tower = line[0], line[2], line[6]
			if sender not in full_users:
				uniquect += 1
				full_users.add(sender)
				if uniquect % denom - round == 0:
					users[sender] = User(sender, date, tower)
			else:
				if sender in users:
					if date in users[sender].locmap:
						users[sender].locmap[date].append(tower)
					else:
						users[sender].locmap[date] = [tower]
		except: pass		
	print users

	# Store all recorded metrics in csv
	w = open("../../output/users_movement_%s.csv" % round, 'w')
	w.write("uid,date,lat,lon\n")
	i = 0
	for uid, user in users.items():
		i += 1
		if i % 100000 == 0: print "processed", i, "users"
		try:
			user.calc_com()
			dates = sorted(user.coms.items(), key=lambda x: int(x[0].split('-')[0]))
			print dates
			for date, tower in dates:
				w.write("%s,%s,%s,%s\n" % (uid, date, tower[0], tower[1]))
		except: pass
	w.close()

def get_user_locs(userid='13707895'):
	# Process the CDR file
	users = {}
	#full_users = set()
	f = csv.reader(open("../../applab_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect = 0
	for line in f:
		#line = map(lambda x: x.strip(), line)
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		#if i == 10000000: break
		try:
			sender, date, tower = line[0], line[2], line[6]
			if sender == userid and userid not in users:
			#	uniquect += 1
			#	full_users.add(sender)
			#	if uniquect % denom - round == 0:
				users[sender] = User(sender, date, tower)
			else:
				if sender in users:
					if date in users[sender].locmap:
						users[sender].locmap[date].append(tower)
					else:
						users[sender].locmap[date] = [tower]
		except: pass		
	print users

	# Store all recorded metrics in csv
	w = open("../../output/users_movement_.csv", 'w')
	w.write("uid,date,lat,lon\n")
	i = 0
	for uid, user in users.items():
		i += 1
		if i % 100000 == 0: print "processed", i, "users"
		try:
			user.calc_com()
			dates = sorted(user.coms.items(), key=lambda x: int(x[0].split('-')[0]))
			print dates
			for date, tower in dates:
				w.write("%s,%s,%s,%s\n" % (uid, date, tower[0], tower[1]))
		except: pass
	w.close()

	
get_user_locs()