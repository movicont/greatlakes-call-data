###
## Parse int'l phone data
###

def load_country_codes():
	# Loads all country codes
	c = open("calling_codes")
	name2rest, idd2rest, code2rest = {}, {}, {}
	for line in c:
		name, code, idd = line.split('|')[0].strip(), line.split('|')[1].strip(), line.split('|')[2].strip()
		name2rest[name] = (code, idd)
		code2rest[code] = name
		if idd not in idd2rest:
			idd2rest[idd] = [(name, code)]
		else:
			idd2rest[idd].append((name, code))
	return name2rest, idd2rest, code2rest

name2rest,idd2rest,code2rest = load_country_codes()	

def find_nation(lst, no):
	for name, code in lst:
		if no[0:len(code)] == code:
			return name
	return None

# Gets list of all letters
def get_countries():
	phone = {}
	codes = load_country_codes()[2]
	print codes
	f = open("anon_intl.txt", 'r')
	w = open("parsed_phones", 'w')
	for line in f:
		values = tuple(line.split('|+|'))
		from_no = values[0]
		nation = None
		#print from_no

		# Check for intl prefix
		"""for i in range(5,0,-1):
			if from_no[0:i] in idd2rest:
				nation = find_nation(idd2rest[from_no[0:i]], from_no[i:len(from_no)-1])
				if nation != None:
					w.write(nation + "|" + "|".join(values[2:]))"""

		if nation == None:
			while len(from_no) > 0 and from_no[0] == '0':
				from_no = from_no[1:]

			if len(from_no) >= 1:
				# North American Numbering Plan
				if from_no[0] == '1':
					if from_no[0:4] in codes:
						phone[values] = codes[from_no[0:4]]
					else:
						phone[values] = 'United States'

				# All other countries besides Russia/Kazakhstan have the same 3-digit/2-digit length pattern
				elif from_no[0] != '7':
					if from_no[0:3] in codes:
						phone[values] = codes[from_no[0:3]]
					elif from_no[0:2] in codes:
						phone[values] = codes[from_no[0:2]]
				else:
					phone[values] = 'Russia/Kazakhstan' # We can't distinguish between these two
				if values in phone:
					w.write(phone[values] + "|" + "|".join(values[2:]))
	f.close()
	w.close()
get_countries()
