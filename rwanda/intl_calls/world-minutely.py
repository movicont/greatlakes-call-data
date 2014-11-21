import sys, math, os, datetime
import Tkinter as Tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.collections import PolyCollection, LineCollection

import shpUtils

sys.path.append('..')
import base.database as database

class World:
	def __init__(self):
		self.db = database.DBConnection()
		colors = self.get_color_map()		

		# Dict mapping country names to polygon coords
		self.nations = {}

		# Matplotlib canvases to draw on
		self.figure = plt.figure(figsize=(16,9))
		self.root = Tk.Tk()
		self.root.title('Int\'l Calls to Rwanda')
		self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
		self.base = self.figure.add_subplot(111)

		# Load countries from shape file into dictionary with self.nations
		xmax, xmin, ymax, ymin = 0, 0, 0, 0
		shpRecords = shpUtils.loadShapefile('world_borders/world_borders.shp')['features']
		for i in range(0,len(shpRecords)):
			# 'verts' is populated with tuples of each border point
			verts = []
			for j in range(0,len(shpRecords[i]['shape']['parts'][0]['points'])):
				tempx = float(shpRecords[i]['shape']['parts'][0]['points'][j][0])
				tempy = float(shpRecords[i]['shape']['parts'][0]['points'][j][1])
				verts.append((tempx, tempy))
				if tempx > xmax: xmax = tempx
				if tempx < xmin: xmin = tempx
				if tempy > ymax: ymax = tempy
				if tempy < ymin: ymin = tempy
 
			cntry_name = shpRecords[i]['info']['CNTRY_NAME']
			if cntry_name in colors:
				if cntry_name.find('Congo') >= 0 or cntry_name.find('Zaire') >= 0:
					if cntry_name in self.nations:
						self.nations[cntry_name].append(PolyCollection([verts], facecolor=colors['Democratic Republic of the Congo']))
					else:
						self.nations[cntry_name] = [PolyCollection([verts], facecolor=colors['Democratic Republic of the Congo'],edgecolor='black')] 
				else:
					if cntry_name in self.nations:
						self.nations[cntry_name].append(PolyCollection([verts], facecolor=colors[shpRecords[i]['info']['CNTRY_NAME']],edgecolor='black'))
					else:
						self.nations[cntry_name] = [PolyCollection([verts], facecolor=colors[shpRecords[i]['info']['CNTRY_NAME']],edgecolor='black')]

		# Add countries loaded into self.nations to the canvas
		for cntry, polys in self.nations.items():
			# Each country can have multiple polygons representing it
			for p in polys:
				if p != []:
					self.base.add_collection(p)
		plt.xlim(xmin, xmax)
		plt.ylim(ymin+20, ymax+20)

		self.canvas.show()
		self.figure.savefig('world', dpi=100, format='png')
		

	def load_new_color_map(self, colors, name):
		for cntry, value in colors.items():
			if cntry in self.nations:
				for part in self.nations[cntry]:
					if value != '#' and value != '':
						part.set_facecolor(value)
					else:
						part.set_facecolor('white')
		self.canvas.show()
		if name != '':
			self.figure.savefig(name.replace(' ', '_'), dpi=100, format='png')

	def animate(self, day):
		def add_zero(num):
			if num < 10: return "0%d" % num
			else: return num

		def generate_times():
			times = []
			for i in range(0, 24):
				#for j in range(0, 60, 5):
				times.append(("%s:00:00" % (add_zero(i)), ("%s:00:00" % (add_zero(i+1)))))
			return times
		
		def round_time(time):
			if time.seconds % 300 != 0:
				return datetime.timedelta(0, time.seconds - time.seconds % 300)
			return time
	
		def get_avg_per_time():
			avgs = {}
			for time in generate_times():
				avg_res = self.db.query("SELECT `country`, `time`, `count` FROM `agg_world_activity` WHERE `time` >='%s' AND `time` < '%s'" % (time[0], time[1]))
				for entry in avg_res:	
					avgs[(round_time(entry[1]), entry[0])] = float(entry[2])/62.0
			return avgs

		def get_max_per_time():
			maxes = {}
			for time in generate_times():
				max_res = self.db.query("SELECT `country`, `time`, `count` FROM `agg_world_activity` WHERE `time` >='%s' AND `time` < '%s'" % (time[0], time[1]))
				for entry in max_res:	
					maxes[(round_time(entry[1]), entry[0])] = float(entry[2])/62.0
			return maxes

		cache = {}
		ind_cache = {}
		max_value = -1
		avgs = get_max_per_time()
		
		for time in generate_times():
			dates = ['2008-02-03']
			for d in dates:
				res = self.db.query("SELECT `country`, `time`, SUM(`count`) FROM `world_activity` WHERE `time` >='%s' AND `time` < '%s' AND `date`='%s' GROUP BY `country`" % (time[0], time[1], d))
				print "SELECT `country`, `time`, SUM(`count`) FROM `world_activity` WHERE `time` >='%s' AND `time` < '%s' AND `date`='%s' GROUP BY `country`" % (time[0], time[1], d)
				for entry in res:
					if (time, d) not in cache:
						cache[(time, d)] = {}
		#			print "enr", entry
					if (round_time(entry[1]), entry[0]) in avgs:
						cache[(time, d)][entry[0]] = [float(entry[2]), float(avgs[(round_time(entry[1]), entry[0])])] #- avgs[(round_time(entry[1]), entry[0])] + 1.0)/(avgs[(round_time(entry[1]), entry[0])]+1.0)
						if cache[(time, d)][entry[0]] < 0:
							cache[time][entry[0]] = 0
						if cache[(time, d)][entry[0]] > max_value:
							max_value = cache[(time, d)][entry[0]]
				mini = min(map(lambda x: x[1][0], cache[(time, d)].items()))
				for country in cache[(time, d)]:
					cache[(time, d)][country][0] -= mini
				#max_value -= mini
		#print cache.items()
		text = self.figure.text(0.4, 0.95, '')
		incr_items = cache.items()
		incr_items.sort(lambda x, y: cmp(x[0][0][0], y[0][0][0]))
		for ((time, date), res) in incr_items:
			text.set_text('%s %s' % (date, ''.join(time)))
			#print res.items()
			colors = {}
			maxe = max(map(lambda x: x[1], res.items()))
			for (country, val) in res.items():
				print "val0", val[0], val[1]
				colors[country] = self.generate_color(val[0], max_value)
			n = '__tmp-%s%s.png' % (date, ''.join(time))
			print n #, colors
			self.load_new_color_map(colors, n)

		os.system("mencoder 'mf://__tmp*.png' -mf type=png:fps=10 -ovc xvid -lavcopts vcodec=mpeg4 -xvidencopts bitrate=738556:me_quality=6:pass=1 -oac copy -o animation3.avi")

	def generate_color(self, value, maximum):
	
		print "valmax", value, maximum
		if type(maximum) == type(0.0):
			maximum = maximum[1]
		def _interpolate(begin, end, step, maximum):
			val, use = 0, 0
			if end < begin: use = end - begin
			else: use = begin - end
			if step < maximum:
				val = int((use * (step / maximum)) + begin)
			else:
				val = int((use * (1 - (step / maximum))) + end)
			if val < 0: return begin
			if val > 255: return end
			return val

		if value < 20:
			return '#eeeeee'
		#	return '#660000'
		"""elif value > 65:
			return '#B22222'
		elif value >= 50:
			return '#CD5555'
		elif value >= 45:
			return '#C67171'
		elif value >= 20:
			return '#BC8F8F'
		elif value >= 10:
			return '#CD9B9B'
		elif value >= 8:
			return '#CDC9C9'
		elif value >= 6:
			return '#EEE9E9'
		else:
			return '#eeeeee'"""
		#value, maximum = math.log(float(value)+1.0), math.log(float(maximum+1.0))
		val = "".join(["%02x"%_interpolate(0, 255, value, maximum), "%02x"%_interpolate(200, 0, value, maximum), "%02x"%_interpolate(255, 0, value, maximum)])
		return '#' + val

	def get_color_map(self, query="SELECT * FROM `world_data`", max_ratio=-1):
		print query
		vals = self.db.query(query)

		disabled = []
		#print vals
		calls_to_pop = filter(lambda x: x[0] not in disabled, map(lambda x: (x[0], x[3]) if x[0].find('Russia') < 0 else ('Russia', x[3]), vals))
		#calls_to_pop = filter(lambda x: x[0] not in disabled, map(lambda x: (x[0], (x[2]/float(x[1])*10000 if float(x[1]) != 0.0 else 0) if x[0] != 'Russia' and x[0] != 'Kazakhstan' else x[2]/(141950000.0+15674833)), vals))
		if max_ratio == -1:
			max_ratio = max(map(lambda x: x[1], calls_to_pop))
		colors = {}

		for (country, ratio) in calls_to_pop:
			colors[country] = self.generate_color(ratio, max_ratio)
			#print country, ratio
		#print max_ratio
		return colors

def main(argv):
	#try:
	w = World()
	w.animate(argv[0])
	#except:
	#	print "format is python world.py [start-time] [end-time]"

if __name__ == "__main__":
	main(sys.argv[1:])
