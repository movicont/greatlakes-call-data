import operator, csv, collections, pickle

class User:
	def __init__(self, location, region):
		self.locmap = collections.defaultdict(int)
		if location != '':
			self.locmap[location] += 1
		self.regionmap = collections.defaultdict(int)
		if region != '':
			self.regionmap[region] += 1
		
	def mostfreqloc(self):
		try:
			return max(self.locmap.iteritems(), key=operator.itemgetter(1))[0]
		except:
			return ''
	
	def mostfreqregion(self):
		try:
			return max(self.regionmap.iteritems(), key=operator.itemgetter(1))[0]
		except:
			return ''

def record_user_locs(denom = 5, round = 0):
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
					users[sender] = User(location, region)
		except: pass
	
	w = open("../output/user_locations_%s.csv" % round, 'w')
	w.write("uid,loc,region\n")
	for uid, user in users.items():
		w.write("%s,%s,%s\n" % (uid, user.mostfreqloc(), user.mostfreqregion()))

#record_user_locs(5, 4)

"""
break it down by regions:
- percentage of calls that are out of region
- percent that stay in region

% of users who move out of their region once:
	% of Kampala/Central users who leave their region
	% of ... users who leave their region at least once

% of Kampala users who make at least one call out of their region
% of ... users who make at least one call out of their region
"""

class Region:
	def __init__(self):
		self.outgoing_calls = collections.defaultdict(int)
		self.incoming_calls = collections.defaultdict(int)
		#self.at_least_one_out = set()
		#self.all_in = set()

	def mostfreqin(self):
		try:
			return sorted(self.incoming_calls.items(), key=lambda x: x[1], reverse=True)[0:5]
		except:
			return ''
	
	def mostfreqout(self):
		try:
			return sorted(self.outgoing_calls.items(), key=lambda x: x[1], reverse=True)[0:5]
		except:
			return ''
	
def load_user_locs():
	users = {}
	f = csv.reader(open("../output/user_locations.csv", 'rb'), delimiter=',')
	for line in f:
		uid, location, region = line
		if location != '' and region != '':
			users[uid] = (location, region)
	return users
	
def get_percentages(useRegion=False, denom = 10, round = 0):
	regions = {}
	users = load_user_locs()
	full_users = {}
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect = 0
	for line in f:
		i += 1
		if i % 1000000 == 0:
			print "processed", i, "lines"
			#print regions
		#if i == 1000000: break
		try:
			sender, receiver, location, region = line[0], line[1], line[6], line[7]
			if useRegion == True:
				if region not in regions:
					regions[region] = Region()
				regions[region].outgoing_calls[users[receiver][1]] += 1
				regions[users[receiver][1]].incoming_calls[region] += 1
			else:
				if (location, region) not in regions:
					regions[(location, region)] = Region()
				#regions[(location, region)].outgoing_calls[users[receiver]] += 1
				regions[users[receiver]].incoming_calls[(location, region)] += 1
				
		except: pass

	try:
		pickle.dump(regions, open("regions_use.p", "wb"))
	except: pass
		
	w = open("../output/regions_transfers.csv", 'w')
	w.write("loc1,reg1,loc2,reg2,calls,percent\n")
	#for uid, user in regions.items():
	#	w.write("%s,%s,%s\n" % (uid, user.mostfreqloc(), user.mostfreqregion()))
	for r, region in regions.items():
		insum = float(sum(region.incoming_calls.values()))
		outsum = float(sum(region.outgoing_calls.values()))
		for r2, r2val in region.mostfreqin():
			w.write("%s,%s,%s,%s,%s,%s\n" % (r[0], r[1], r2[0], r2[1], r2val, r2val/insum))
		for r2, r2val in region.mostfreqout():
			w.write("%s,%s,%s,%s,%s,%s\n" % (r[0], r[1], r2[0], r2[1], r2val, r2val/outsum))

get_percentages()