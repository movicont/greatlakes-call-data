import csv, collections

def load_tower_times():
	f = csv.reader(open("../output/time_by_tower.csv", 'rb'), delimiter=',')
	towers = {}
	for line in f:
		tower,region,time,count = line
		if tower not in towers:
			towers[tower] = {}
		towers[tower][time] = count
	return towers
	
def load_tower_stats():
	f = csv.reader(open("../output/towers_with_stats.csv", 'rb'), delimiter='|')
	towers = {}
	i = 0
	for line in f:
		if i != 0:
			sitename, lat, lon, urban = line[1], line[2], line[3], line[21]
			towers[sitename] = (lat, lon, int(urban))
		i += 1
	return towers
	
towers_stats = load_tower_stats()
towers_times = load_tower_times()
urban = {}
rural = {}

for tower, val in towers_stats.items():
	try:
		if val[2] == 1: 	# tower is urban
			urban[tower] = towers_times[tower]
		else:
			rural[tower] = towers_times[tower]
	except: pass
		
wurban = open("../output/urban_times.csv", 'w')
wurban.write("tower,time,count\n")
alltimes = collections.defaultdict(int)
for tower, values in urban.items():
	for t, ct in values.items():
		alltimes[t] += int(ct)
		wurban.write("%s,%s,%s\n" % (tower, t, ct))
for t, v in alltimes.items():
	wurban.write("total,%s,%s\n" % (t, v))
wurban.close()

wrural = open("../output/rural_times.csv", 'w')
wrural.write("tower,time,count\n")
alltimes = collections.defaultdict(int)
for tower, values in rural.items():
	for t, ct in values.items():
		alltimes[t] += int(ct)
		wrural.write("%s,%s,%s\n" % (tower, t, ct))
for t, v in alltimes.items():
	wrural.write("total,%s,%s\n" % (t, v))
wrural.close()