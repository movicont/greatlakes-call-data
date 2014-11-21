import csv, pickle, collections

class Tower:
	def __init__(self, sitename, lat, lon):
		self.lat = lat
		self.lon = lon
		self.name = sitename
		self.in_calls = collections.defaultdict(int)
		self.out_calls = collections.defaultdict(int)
		self.calls_to_self = collections.defaultdict(int)
		self.calls_to_others = collections.defaultdict(int)

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
	
	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		try:
			sender, receiver, date, time, duration, cost, location, region = line
			if location in towers:
				towers[location].out_calls[date] += 1
				towers[users[receiver].loc].in_calls[date] += 1
				if users[receiver].loc == location:
					towers[location].calls_to_self[date] += 1
				else:
					towers[location].calls_to_others[date] += 1
		except: pass
		
	w.write("date,sitename,lat,lon,in_calls,out_calls,calls_to_self,calls_to_others\n")
	i = 0
	for loc, tower in towers.items():
		i += 1
		print "written", i, "lines"
		for d in tower.out_calls.keys():
			w.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (d, loc, tower.lat, tower.lon, tower.in_calls[d], tower.out_calls[d], tower.calls_to_self[d], tower.calls_to_others[d]))
	w.close()

if __name__ == "__main__":
	agg_by_region()