"""

Aggregates the time of calls for each region

"""

import csv, collections, pickle, os, time
from datetime import datetime


def process():
	regions = {}
	f = csv.reader(open("../applab_6.csv", 'rb'), delimiter=',')
	i = 0
	uniquect, actual = 0, 0
	for line in f:
		i += 1
		if i % 100000 == 0:
			print "processed", i, "lines"
		#if i == 400000: break
		try:
			sender, receiver, d, ti, duration, cost, location, region = line
			ti = ti.split(':') #datetime.fromtimestamp(time.mktime(time.strptime(ti, "%H:%M:%S")))
			if (location, region) not in regions:
				regions[(location, region)] = collections.defaultdict(int)
			regions[(location, region)][int(ti[0])] += 1
		except: pass
		
	w = open("../output/time_by_tower.csv", 'w')
	w.write("tower,region,time,count\n")
	for reg, times in regions.items():
		for ti, ct in times.items():
			w.write("%s,%s,%s,%s\n" % (reg[0], reg[1], ti, ct))
	w.close()

process()