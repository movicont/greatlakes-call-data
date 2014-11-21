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
					try:
						part.set_facecolor(value)
					except:
						part.set_facecolor('white')
		self.canvas.show()
		if name != '':
			self.figure.savefig(name.replace(' ', '_'), dpi=100, format='png')

	def animate(self, day):
		def add_zero(num):
			if num < 10: return "0%d" % num
			else: return str(num)

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
			for time in range(24):
				avg_res = self.db.query("SELECT `country`,`time`,`count`,`std_dev` FROM  `world_avgs` WHERE `time` = %s" % time)
				for entry in avg_res:
					avgs[(entry[1], entry[0])] = (float(entry[2]), float(entry[3]))
			return avgs

		def dates(start, end):
			months = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
			dates = []
			for month in range(start[1], end[1]+1):
				for i in range(0, months[month]):
					dates.append(str(start[0]) + '-' + add_zero(month) + '-' + add_zero(i+1))
			return dates

		cache = {}
		ind_cache = {}
		max_value = -1
		avgs = get_avg_per_time()
		text = self.figure.text(0.4, 0.95, '')
		
		for d in dates((2008,02,00), (2008,02,15)):
			for time in range(24):
				query = "SELECT `country`, `time`, `count`, `date` FROM `hourly_world_activity_15_15` WHERE `time` = %s AND `date`='%s' GROUP BY `country`" % (time, d)
				res = self.db.query(query)
				print query
				colors = {}
				for entry in res:
					country, time, count, date = entry[0], entry[1], entry[2], entry[3]
					#print count, avgs[(time, country)]
					colors[country] = self.generate_color(count+0.01, avgs[(time, country)][0]+0.01-avgs[(time, country)][1]*3, avgs[(time, country)][0]+0.01+avgs[(time, country)][1]*3)
				n = '__tmp-%s%s.png' % (d, str(add_zero(time)))
				text.set_text('%s %s' % (d, str(add_zero(time))))
				print colors
				self.load_new_color_map(colors, n)

		os.system("mencoder 'mf://__tmp*.png' -mf type=png:fps=10 -ovc xvid -lavcopts vcodec=mpeg4 -xvidencopts bitrate=738556:me_quality=6:pass=1 -oac copy -o animation3.avi")

	def generate_color(self, value, minimum, maximum):
		#value += 0.01
		#minimum += 0.01
		#maximum += 0.01

		def _interpolate(begin, end, step, mini, maxi):
			if step > maxi: return end
			if step < mini: return begin
			v = (step / ((maxi - mini) / (end - begin))) + begin
			if v < 0:
				return begin
			return v

		#value, maximum = math.logf(loat(value)+1.0), math.log(float(maximum+1.0))
		try:
			if value == 0 or minimum == 0 or maximum == 0:
				return '#dddddd'
			#print value, minimum, maximum, _interpolate(0, 255, value, minimum, maximum)
			val = "".join(["%02x"%_interpolate(0, 255, value, minimum, maximum),\
			"%02x"%_interpolate(155, 0, value, minimum, maximum), "%02x"%_interpolate(255, 0, value, minimum, maximum)])
			print val, value, minimum, maximum, _interpolate(155, 0, value, minimum, maximum)
			return '#' + val
		except: return '#dddddd'

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
			colors[country] = self.generate_color(ratio, 0, max_ratio)
			#print country, ratio
		#print max_ratio
		return colors

def main(argv):
	#try:
	w = World()
	w.animate(argv[0])
	#	print "format is python world.py [start-time] [end-time]"

if __name__ == "__main__":
	main(sys.argv[1:])
