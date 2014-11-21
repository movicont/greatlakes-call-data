import csv, pickle

class Tower:
	def __init__(self, sitename, lat, lon):
		self.lat = lat
		self.lon = lon
		self.name = sitename
		#self.regions = set()
		self.in_calls = 0
		self.out_calls = 0
		self.calls_to_self = 0
		self.calls_to_others = 0

class User:
	def __init__(self, loc, reg):
		self.loc = loc
		self.reg = reg
		self.lat = None
		self.lon = None
		
def load_tower_locs():
	towers = {}
	f = csv.reader(open("../mtnugsites.csv", 'rb'), delimiter=',')
	i = 0
	for line in f:
		siteid, sitename, long, lat = line
		towers[sitename] = Tower(sitename, lat, long)
	pickle.dump(towers, open("tower_locations.p", "wb"))
	return towers

def load_user_locs():
	users = {}
	f = csv.reader(open("../output/temp/user_locations.csv", 'rb'), delimiter=',')
	i = 0
	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "users"
		uid, loc, reg = line
		if loc != '' and reg != None:
			users[uid] = User(loc, reg)
	return users
	
def agg_by_region():
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	w = open("../output/regions.csv", 'w')
	i = 0
	towers = load_tower_locs()
	users = load_user_locs()
	#for uid in users.keys():
	#	if users[uid].loc.strip() in towers:
	#		users[uid].lat = towers[users[uid].loc].lat
	#		users[uid].lon = towers[users[uid].loc].lon

	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		try:
			sender, receiver, date, time, duration, cost, location, region = line
			if location in towers:
				towers[location].out_calls += 1
				towers[users[receiver].loc].in_calls += 1
				if users[receiver].loc == location:
					towers[location].calls_to_self += 1
				else:
					towers[location].calls_to_others += 1
		except: pass
		
	w.write("sitename,lat,lon,in_calls,out_calls,calls_to_self,calls_to_others\n")
	i = 0
	for loc, tower in towers.items():
		i += 1
		print "written", i, "lines"
		w.write("%s,%s,%s,%s,%s,%s,%s\n" % (loc, tower.lat, tower.lon, tower.in_calls, tower.out_calls, tower.calls_to_self, tower.calls_to_others))
	w.close()

if __name__ == "__main__":
	agg_by_region()