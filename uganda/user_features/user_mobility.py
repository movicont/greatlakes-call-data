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
	sites_r = csv.reader(open("../mtnugsites.csv"), delimiter=',')
	phone_towers = {}
	cntr = 0
	for line in sites_r:
		if cntr != 0:
			phone_towers[line[1]] = (float(line[2]), float(line[3]))
		cntr += 1
	
	def __init__(self, uid, location):
		self.uid = uid
		self.center_of_mass = None
		self.radius_of_gyration = 0.0
		#self.distance_traveled = 0.0
		#self.velocity = 0.0
		self.locmap = collections.defaultdict(int)
		if location != '':
			self.locmap[location] += 1

	def mostfreqloc(self):
		try:
			return max(self.locmap.iteritems(), key=operator.itemgetter(1))[0]
		except:
			return ''
	
	"""
		Stores the center of mass as a tuple (lat, lon)
	"""
	def calc_com(self):
		sumlat, sumlon = 0.0, 0.0
		count = 0
		for loc, ct in self.locmap.items():
			if loc in User.phone_towers:
				count += ct
				sumlat += User.phone_towers[loc][0]*ct
				sumlon += User.phone_towers[loc][1]*ct
		if count != 0:
			self.center_of_mass = (sumlat/count, sumlon/count)
		else:
			self.center_of_mass = None
	
	"""
		Calculates the distance between two lat/lon points
		Uses the haversine formula, which finds the great circle distance
		between two points: http://www.movable-type.co.uk/scripts/latlong.html
	"""
	def get_distance(self, latA, lonA, latB, lonB):
		R = 6371.0
		dLat = math.radians(latB-latA)
		dLon = math.radians(lonB-lonA)
		latA = math.radians(latA)
		latB = math.radians(latB)
		a = math.sin(dLat/2) * math.sin(dLat/2) +\
			math.sin(dLon/2) * math.sin(dLon/2) * math.cos(latA) * math.cos(latB)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		return R * c
	
	"""
		Calculates the radius of gyration:
		rog = sqrt(sum over all distances((dist-com)^2))
	"""
	def calc_rog(self):
		sumdist = 0.0
		count = 0
		if self.center_of_mass != None:
			for loc, ct in self.locmap.items():
				if loc in User.phone_towers:
					count += ct
					dist = self.get_distance(self.center_of_mass[0], self.center_of_mass[1], User.phone_towers[loc][0], User.phone_towers[loc][1])
					sumdist += (dist ** 2)*ct
			if count != 0:
				self.radius_of_gyration = math.sqrt(sumdist/count)
			else:
				self.radius_of_gyration = 0.0
	
	"""
		Calculates the average of the # of times a user is at a given location
		This number should tend to be smaller if the user moves around frequently
		and only goes to new places a few times.
	"""
	def avg_freq_per_loc(self):
		try:
			return sum(self.locmap.values())/len(self.locmap)
		except: return 0

	def total_locs(self):
		return len(self.locmap)
		
	"""
		The highest # of times a person is at a given location.
	"""
	def highest_freq(self):
		try:
			return max(self.locmap.values())
		except: return 0

		

def record_user_locs(denom = 5, round = 0):
	# Process the CDR file
	users = {}
	full_users = set()
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect = 0
	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
		#if i == 1000000: break
		try:
			sender, location, region = line[0], line[6], line[7]
			if sender not in full_users:
				uniquect += 1
				full_users.add(sender)
				if uniquect % denom - round == 0:
					users[sender] = User(sender, location)
			else:
				users[sender].locmap[location] += 1
		except: pass

	# Store all recorded metrics in csv
	w = open("../output/users_mobility_%s.csv" % round, 'w')
	w.write("uid,loc,comlat,comlon,rog,avg_freq,total_locs,highest_freq\n")
	i = 0
	for uid, user in users.items():
		i += 1
		if i % 100000 == 0: print "processed", i, "users"
		user.calc_com()
		user.calc_rog()
		try:
			w.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (uid, user.mostfreqloc(), user.center_of_mass[0], user.center_of_mass[1], user.radius_of_gyration,\
								user.avg_freq_per_loc(), user.total_locs(), user.highest_freq()))
		except: pass
	w.close()

record_user_locs()