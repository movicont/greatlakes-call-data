import sys
import matplotlib.pyplot as plt
import shpUtils
sys.path.append('..')
import base.database as database

def load_world():
	shpRecords = shpUtils.loadShapefile('world_borders/world_borders.shp')['features']
	colors = load_color_map()
	plt.figure(figsize=(16, 9))

	last = ''
	for i in range(0,len(shpRecords)):
		if shpRecords[i]['info']['CNTRY_NAME'] != last:
			print shpRecords[i]['info']['CNTRY_NAME']
			last = shpRecords[i]['info']['CNTRY_NAME']

		# x and y are empty lists to be populated with the coords of each geometry.
		x = []
		y = []
		#print shpRecords[i]
		for j in range(0,len(shpRecords[i]['shape']['parts'][0]['points'])):
			tempx = float(shpRecords[i]['shape']['parts'][0]['points'][j][0])
			tempy = float(shpRecords[i]['shape']['parts'][0]['points'][j][1])
			x.append(tempx)
			y.append(tempy) # Populate the lists  

		# Creates a polygon in matplotlib for each geometry in the shapefile
		if shpRecords[i]['info']['CNTRY_NAME'] in colors:
			if shpRecords[i]['info']['CNTRY_NAME'] == 'Congo' or shpRecords[i]['info']['CNTRY_NAME'] == 'Zaire':
				plt.fill(x,y, facecolor=colors['Democratic Republic of the Congo'])
			plt.fill(x,y, facecolor=colors[shpRecords[i]['info']['CNTRY_NAME']])

	plt.axis('equal')
	plt.savefig('world_calls.png', dpi=100, format='png')
	plt.show()

def load_color_map():
	def generate_color(value, maximum):
		value, maximum = float(value), float(maximum)
		"""if value > 1000000:
			return '#660000'
		elif value > 500000:
			return '#B22222'
		elif value >= 250000:
			return '#CD5555'
		elif value >= 100000:
			return '#C67171'
		elif value >= 10000:
			return '#BC8F8F'
		elif value >= 1000:
			return '#CD9B9B'
		elif value >= 100:
			return '#CDC9C9'
		elif value >= 10:
			return '#EEE9E9'
		else:
			return '#eeeeee'"""
		val = "".join(["%02x"%_interpolate(155, 255, log(value), maximum), "%02x"%_interpolate(0, 0, value, maximum), "%02x"%_interpolate(0, 0, value, maximum)])
		return '#' + val

	def _interpolate(begin, end, step, maximum):
		if begin < end:
		    	return int(((end - begin) * (step / maximum)) + begin)
		else:
			return int(((begin - end) * (1 - (step / maximum))) + end)

	db = database.DBConnection()
	vals = db.query("SELECT * FROM `world_data`")

	disabled = ['Ascension', 'British Virgin Islands', 'Macao']
	#calls_to_pop = filter(lambda x: x[0] not in disabled, map(lambda x: (x[0], (x[2]/float(x[1])*10000 if float(x[1]) != 0.0 else 0) if x[0] != 'Russia' and x[0] != 'Kazakhstan' else x[2]/(141950000.0+15674833)), vals))
	max_ratio = max(map(lambda x: x[2], vals))
	colors = {}

	for (country, pop, count, dur) in vals:
		colors[country] = generate_color(count, max_ratio)
		#print country, ratio
	print max_ratio
	return colors


load_world()
