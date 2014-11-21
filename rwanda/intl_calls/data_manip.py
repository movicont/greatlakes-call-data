# 2007-12-31 to 2008-03-01

"""SELECT  `country` , SUM(  `duration` ) , COUNT( * ) 
FROM  `world_activity` 
WHERE  `date` =  '2007-12-31'
AND  `time` >=  '23:00:00'
AND  `time` <  '24:00:00'
AND  `country` =  'United States'"""

def pre(num):
	if num < 10:
		return '0' + str(num)
	return str(num)

def times():
	times = []
	for i in range(24):
		times.append((pre(i)+':00:00', pre(i+1)+':00:00'))
	return times

def dates(start, end):
	months = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
	dates = []
	for month in range(start[1], end[1]+1):
		for i in range(months[month]):
			dates.append(str(start[0]) + '-' + pre(month) + '-' + pre(i+1))
	return dates

# 162 countries, 31+28+31 days, 24 hour/day
def generate_hourly():
	f = open('countries_list')
	w = open('sql_gen', 'w')
	for c in f:
		for d in dates((2008,01,01), (2008,03,01)):
			for t in times():
				w.write("INSERT INTO `hourly_world_activity` SELECT  `country`, `date`, `time`, COUNT(*) FROM `world_activity` WHERE `date` = '%s' AND `time` >= '%s' AND  `time` < '%s' AND `country` = '%s';" % (d, t[0], t[1], c.strip()) + "\n")
					
for i in range(1, 25):
	print "INSERT INTO `world_avgs` SELECT  `country`, `date`, `time`, COUNT(*)/92 FROM `world_activity` WHERE `time` >= '%s:00:00' AND  `time` < '%s:00:00' GROUP BY `country`;" % (pre(i), pre(i+1))
