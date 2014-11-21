import collections

w = open("../data/user_transfers.csv", 'w')
w1 = open("../data/sorted_by_transfers.csv", 'w')
f = open("../data/me2u.locs.valid.txt")
i = 0
trans_freq = {}
count_freq = collections.Counter()
w.write("user1,user2,type,loc,freq,time\n")
for line in f:
	if i % 50000 == 0:
		print "processed line " + str(i)
	# split the line and match the columns to variables
	line = line.split(',')
	person1, person2, date, time, amount = line[0:5]
	loc1, loc2 = line[5], line[8]
	count_freq[person1] += 1
	"""if person1 not in trans_freq:
		trans_freq[person1] = {}
		trans_freq[person1][person2] = 1
		w.write(person1 + ',' + person2 + ',join+transfer,' + str(trans_freq[person1][person2]) + "\n")
	elif person1 in trans_freq:
		if person2 in trans_freq[person1]:
			trans_freq[person1][person2] += 1
		else:
			trans_freq[person1][person2] = 1
		w.write(person1 + ',' + person2 + ',transfer,' + str(trans_freq[person1][person2]) + "\n")"""
	i+=1
print count_freq.most_common(20)