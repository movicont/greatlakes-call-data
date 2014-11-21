import os, sys, time, math, random as rn, voronoi as v, numpy as np
import Tkinter as Tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from pylab import *
import matplotlib.image as mpimg
import Image
from matplotlib.widgets import Slider

from handle_voronoi_data import Voronoi

sys.path.append('..')
import base.csv as csv
import base.database as database

class Point:
	def __init__(self, x, y):
		self.x, self.y = x, y

	def println(self):
		print "(%d, %d)" % (self.x, self.y)

class Polygon:
	def __init__(self, points):
		self.points = points
	
	def points(self): return self.points
	
	def area(self):
		s = 0
		for i in range(len(self.points)-1):
			s += self.points[i][0]*self.points[i+1][1] - self.points[i+1][0]*self.points[i][1]
		return abs(0.5*s)
	
	def centroid(self):
		ratio = 1.0/(6*self.area())
		x = sum(map(lambda one, two: (one[0]+two[0])*(one[0]*two[1] - two[0]*one[1]), self.points[0:len(self.points)-1], self.points[1:]), 0)
		y = sum(map(lambda one, two: (one[1]+two[1])*(one[0]*two[1] - two[0]*one[1]), self.points[0:len(self.points)-1], self.points[1:]), 0)
		return Point(ratio*x, ratio*y)

class TowerMap:
	def __init__(self):
		self.db = database.DBConnection()
		self.year, self.month, self.day, self.minute, self.hour = '2005', '01', '01', 0,0
		v = Voronoi()
		self.points = v.points
		self.xmin, self.xmax, self.ymin, self.ymax = 0,0,0,0
		
		self.fig_name = "rwanda%s.png"
		
		self.root = Tk.Tk()
		self.root.title('Rwanda Phone Towers')
		
		self.canvas, self.voronoi, self.base, self.figure = None, v.voronoi, None, None
		self.init_figure()
		
		self.menu()
		self.canvas.show()
		self.canvas.get_tk_widget().pack()
		
		self.root.mainloop()
	
	def init_figure(self):
		self.figure = plt.figure(figsize=(8, 6))
		self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
		self.base = self.figure.add_subplot(111)
		
		self.xmax,self.xmin,self.ymax,self.ymin = 31.2,28.5,-1.0,-3.0
		plt.xlim(28.5, 31.2)
		plt.ylim(-3.0, -1.0)
		self.polys = {}
		for i in range(len(self.voronoi)):
			if self.voronoi[i][1] != []:
				self.polys[self.voronoi[i][0][0]] = PolyCollection([self.voronoi[i][1]],facecolors='#ffffff')
			else:
				self.polys[self.voronoi[i][0][0]] = []
		for key, poly in self.polys.items():
			if poly != []:
				self.base.add_collection(poly)
		self.total()
		self.draw_map()

	def generate_csv(self):
		#tower_id, area_covered, n_users, user_density
		areas = self.__get_areas()
		densities = self.__get_densities()
		f = open('tower_densities.csv', 'w')
		f.write("tower_id|area|density|users\n")
		i = 0
		for area in areas:
			f.write(str(int(area[0][0])) + '|' + str(area[1]) + '|' + str(densities[i][1]) + '|' + str(densities[i][2]) + "\n")
			i+=1
		print areas
	
	def generate_color(self, value, maximum):
		value, maximum = float(value), float(maximum)
		if maximum == 0: maximum = 1.0
		#val = ((self.interpolate(0, 255, value, maximum) << 8) | self.interpolate(155, 0, value, maximum)) << 8 | self.interpolate(255, 0, value, maximum)
		val = "".join(["%02x"%self.__interpolate(0, 255, value, maximum), "%02x"%self.__interpolate(155, 0, value, maximum), "%02x"%self.__interpolate(255, 0, value, maximum)])
		print val, value, maximum, self.__interpolate(0, 255, value, maximum)
		return '#' + val

	def __interpolate(self, begin, end, step, maximum):
		if begin < end:
		    	return int(((end - begin) * (step / maximum)) + begin)
		else:
			return int(((begin - end) * (1 - (step / maximum))) + end)

	def next(self, move=1, minute=False):
		days_in_month = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
		if minute == False:
			if (int(self.day) + move) > days_in_month[int(self.month)]:
				self.day = '01'
				if (int(self.month) + 1) > 12:
					self.year = str(int(self.year) + 1)
					self.month = '01'
				else:
					self.month = self.date_prepend(int(self.month)+1)
			else: self.day = self.date_prepend(int(self.day)+move)
			calls = self.db.query("SELECT `tower_id`,`calls_in` FROM `daily_tower_activity` WHERE `date`='"+self.year + '-' + self.month + '-' + self.day+"'")
		else:
			if (self.minute + 1) > 60:
				self.minute = 0
				self.hour += 1
			else:
				self.minute += 1
			calls = self.db.query("SELECT `tower_id`,`calls_in` FROM `minute_tower_activity` WHERE `date`='"+self.year + '-' + self.month + '-' + self.day+"' AND `hour`='" + str(self.hour) + "' AND `minute`='" + str(self.minute) + "'")
		hold(False)
		#print self.year, self.month, self.day, self.minute, self.hour
		self.graph(map(lambda x: x[1], calls))
	
		return map(lambda x: x[0], calls)

	def total(self):
		calls = self.db.query("SELECT `tower_id`, SUM(`calls_in`) FROM `hourly_tower_activity` GROUP BY `tower_id`")
		self.graph(calls)

	def graph(self, data):
		search = map(lambda x: float(x[1]), data)
		#search = map(lambda x: x - min(search), search)
		maximum = max(search)
		#print maximum
		dat_map = {}
		for pt in data:
			dat_map[pt[0]] = pt[1]
		print dat_map
		#print 'unctouche list'
		for i in range(len(self.voronoi)):
			poly = Polygon(self.voronoi[i][1])
			area, centroid = 110*111*poly.area(), poly.centroid()
			#self.base.text(self.voronoi[i][0][1], self.voronoi[i][0][2], str(self.voronoi[i][0][0]) +":"+str(calls_in[0][0]), size=10)
			#if int(self.voronoi[i][0][0]) in dat_map.keys():
				#self.polys[int(self.voronoi[i][0][0])].set_facecolor(self.generate_color(float(dat_map[int(self.voronoi[i][0][0])]), maximum))
				#self.polys[int(self.voronoi[i][0][0])].set_edgecolor(self.generate_color(float(dat_map[int(self.voronoi[i][0][0])]), maximum))
			#else:
				#self.polys[int(self.voronoi[i][0][0])].set_facecolor('#eeeeee')
				#self.polys[int(self.voronoi[i][0][0])].set_edgecolor('#eeeeee')
				#print self.voronoi[i][0][0]
		self.canvas.show()
		
	def draw_map(self):
		coords = self.get_coords()
		mod_coords = self.get_mod_coords()
		self.base.add_collection(PolyCollection([coords],facecolors='#ffffff',edgecolors='#ffffff'))
		self.base.add_collection(LineCollection(mod_coords,colors='#000000'))
		self.canvas.show()
		self.figure.savefig(self.fig_name % '_with_areas')

	def get_coords(self):
		f = open('../data/rwanda_border_coords')
		coords = []
		for line in f:
			line = line.split('&')[0]

			line = line.split('=')[1]
			line = line.split(',')
			coords.append([float(line[1]), float(line[0])])
		return coords

	def get_mod_coords(self):
		f = open('border_coords/processed_border_coords')
		coords, mod_coords = [], []
		for line in f:
			line = line.split(' ')
			coords.append([float(line[1]), float(line[0])])
		for i in range(len(coords)-1):
			mod_coords.append((coords[i], coords[i+1]))
		return mod_coords
	
	def __transform_for_drawing(self, points, plot='polygons',xmax=0,ymax=0,xmin=0,ymin=0):
		if xmax == 0 and ymax == 0 and xmin == 0 and ymin == 0 and plot == 'polygons':
			xmax, ymax, xmin, ymin = self.__min_maxes(points)
		transformed = []
		for i in range(len(points)):
			if plot == 'points':
				transformed.append(((points[i][0]-xmin)*320, (points[i][1]+abs(ymin))*290))
			else:
				transformed.append(map(lambda v: ((v[0]-xmin)*320, (v[1]+abs(ymin))*290), points[i]))
		return transformed
	
	def __min_maxes(self, points):
		xmax,ymax,xmin,ymin = -100,-100,100,100
		for polygon in points:
			for edge in polygon:
				if float(edge[0]) > xmax: xmax = float(edge[0])
				if float(edge[0]) < xmin: xmin = float(edge[0])
				if float(edge[1]) > ymax: ymax = float(edge[1])
				if float(edge[1]) < ymin: ymin = float(edge[1])
		return xmax, ymax, xmin, ymin
	
	def show_areas(self):
		for i in range(len(self.voronoi)):
			#poly = self.__lambert(v[i])
			area_poly = Polygon(self.voronoi[i][1])
			area, centroid = 110*111*area_poly.area(), area_poly.centroid()
			if area > 100:
				self.base.text(centroid.x, centroid.y, str(round(area, 1)), size=int(math.log(area)+3))
			print area, centroid.x, centroid.y
		self.canvas.show()
		self.figure.savefig(self.fig_name % '_with_areas')
		self.fig_name = self.fig_name % "_with_areas%s"

	def __get_areas(self):
		areas = []
		for i in range(len(self.voronoi)):
			area = 110*111*Polygon(self.voronoi[i][1]).area()
			areas.append((self.voronoi[i][0], area))
		return areas

	def graph_areas(self):
		areas = self.figure.add_subplot(111)
		data = map(lambda x: x[1], self.__get_areas())
		n, bins, patches = areas.hist(data, 200, facecolor='green', alpha=0.75)
		bincenters = 0.5*(bins[1:]+bins[:-1])
		areas.set_xlim(0, 1000)
		areas.set_ylim(0, 120)
		areas.set_xlabel('Density')
		areas.set_ylabel('Frequency')
		self.canvas.show()
		#self.figure.savefig(self.fig_name % '_graph_areas')
		self.fig_name = self.fig_name % "_graph_areas%s"

	def draw_towers(self):
		xs, ys, ids = map(lambda x: x[0][1], self.voronoi), map(lambda x: x[0][2], self.voronoi), map(lambda x: x[0][0], self.voronoi)
		
		self.base.scatter(xs, ys, c="white")
		self.base.set_xlim(self.xmin, self.xmax)
		self.base.set_ylim(self.ymin, self.ymax)
		
		self.figure.savefig(self.fig_name % '_with_towers')
		self.fig_name = self.fig_name % "_with_towers%s"
		self.canvas.show()
		return xs, ys, ids

	def get_towers(self):
		xs, ys, ids = map(lambda x: x[0][1], self.voronoi), map(lambda x: x[0][2], self.voronoi), map(lambda x: x[0][0], self.voronoi)
		return xs, ys, ids

	def __lambert(self, points):
		pi = 3.141592654
		projection = []
		for i in range(len(points)):
			lat, lon = points[i][1], points[i][0]
			k = (2.0/(1.0+math.cos(lat)*math.cos(lon)))**0.5
			projection.append(110*(k*math.cos(lat)*math.sin(lon), 111*k*math.sin(lat)))
		return projection
	
	def __get_densities(self):
		df = csv.DelimitedFile('../data/user_locations.4years.anon.txt', '|')
		primary_towers = map(lambda x: int(x), df.array[df.rfields['primary_tower']])
		towers = {}
		for tower in primary_towers:
			if tower in towers: towers[tower] += 1
			else: towers[tower] = 1
		areas = self.__get_areas()
		densities = []
		for item in areas:
			tower_id,area = int(item[0][0]), item[1]
			value = (towers[tower_id] if tower_id in towers else 0)/float(area)
			if value > 700: value = 700
			densities.append((tower_id,value,(towers[tower_id] if tower_id in towers else 0)))
		return densities

	def show_densities(self):
		densities = self.__get_densities()
		#print densities
		self.graph(map(lambda x: x[1], densities))
		self.figure.savefig(self.fig_name % '_with_densities')
		self.fig_name = self.fig_name % "_with_densities%s"

	def date_prepend(self, n):
		if n < 10: n = '0' + str(n)
		return str(n)

	""" Animates minutes between current times (self) and new times"""
	def between(self, new_year, new_month, new_day):
		query = "SELECT `tower_id`,`hour`,`minute`,`calls_in` FROM `minute_tower_activity` WHERE "
		query += "`date`='" + new_year + '-' + new_month + '-' + new_day + "'"
		data = self.db.query(query)
		new_data = {}
		for datum in data:
			if (datum[1], datum[2]) in new_data:
				new_data[(datum[1], datum[2])].append([datum[0], datum[3]])
			else:
				new_data[(datum[1], datum[2])] = [[datum[0], datum[3]]]
		return new_data

	""" Calculates the percent increase between the previous day's values.
		possible other things to try:
		- percent increase against average of N days
		- normalized against 
	"""
	def percent_increase(self, data, normal):
		#data = map(lambda x: x[1], data)
		#normal = map(lambda x: x[3], normal)
		# data is [[time interval: [calls in for every tower on that interval]]
		#normal = map(lambda x: float(x[1]), normal)
		for hour in range(24):
			for minute in range(60):
				for tower in data[(hour, minute)]:
					tower[1] = (float(tower[1]) - float(normal[(hour, minute, int(tower[0]))])+1.0) / \
					(float(normal[(hour, minute, int(tower[0]))])+1.0)
				mini = min(map(lambda x: x[1], data[(hour, minute)]))
				for tower in data[(hour, minute)]:
					tower[1] = tower[1] - mini
				#print float(data[i][1][j][1]+1), float(normal[data[i][0]][1]+1), perinc
		return data

	def animate(self):
		self.year, self.month, self.day, self.minute, self.hour = '2008', '02', '03', 0, 0
		data = self.between('2008','02','03')
		# this finds the average calls in per tower per minute
		avgs = list(self.db.query("SELECT `tower_id` , `hour` , `minute` , AVG( `calls_in` ) FROM `minute_tower_activity` GROUP BY `hour` , `minute` , `tower_id`"))
		#data.sort(lambda x, y: cmp(int(x[0][0])*60+int(x[0][1]), int(y[0][0])*60+int(y[0][1])))
		
		text = self.figure.text(0.4, 0.95, self.year + '-' + self.month + '-' + self.day + ' ' + self.date_prepend(self.hour) + ':' + self.date_prepend(self.minute))
		#dates = map(lambda x: self.date_prepend(x[0][0])+self.date_prepend(x[0][1]), data.items())
		new_avgs = {}
		for x in avgs:
			new_avgs[(x[1],x[2],int(x[0]))] = x[3]
		normalized = self.percent_increase(data, new_avgs)
		
		#minimum = min(map(lambda x: min(map(lambda y: y[1], x)), normalized))
		#for i in range(len(normalized)):
		#	normalized[i] = map(lambda x: (x[0], x[1] + abs(minimum)), normalized[i])
		#minimum = min(map(lambda x: min(x), normalized))
		#for i in range(len(normalized)):
		#	normalized[i] = map(lambda x: (x[0], x[1] - min(map(lambda x: x[1], normalized[i]))), normalized[i])
		#maximum = max(map(lambda x: max(map(lambda y: y[1], x)), normalized))
		
		i = 0
		#self.draw_towers()
		for hour in range(24):
			for minute in range(60):
				self.graph(data[(hour, minute)])
				#print data[(hour, minute)]
				#self.draw_map()
				text.set_text(self.year + '-' + self.month + '-' + self.day + ' ' + self.date_prepend(hour) + ':' + self.date_prepend(minute))
				self.canvas.show()
				self.figure.savefig('__tmp' + self.date_prepend(hour) + self.date_prepend(minute) + str(i) + '.png')
				i+=1
		os.system("mencoder 'mf://__tmp*.png' -mf type=png:fps=24 -ovc xvid -lavcopts vcodec=mpeg4 -xvidencopts bitrate=738556:me_quality=6:pass=1 -oac copy -o animation.avi")
		
	def menu(self):
		menubar = Tk.Menu(self.root)
		menubar.add_command(label="<- Prev", command=lambda:self.next(None,None,None,-1))
		menubar.add_command(label="Next ->", command=self.next)
		menubar.add_command(label="All", command=self.total)
		
		yearmenu = Tk.Menu(menubar, tearoff=0)
		for k in range(2005, 2009):
			monthmenu = Tk.Menu(yearmenu, tearoff=0)
			for j in range(1, 13):
				daymenu = Tk.Menu(monthmenu, tearoff=0)
				for i in range(1, 32):
					#print self.date_prepend(k), self.date_prepend(j), self.date_prepend(i)
					daymenu.add_command(label=str(i), command=lambda:self.next(self.date_prepend(k), self.date_prepend(j), self.date_prepend(i)))
				monthmenu.add_cascade(label=str(j), menu=daymenu)
			
			yearmenu.add_cascade(label=str(k), menu=monthmenu)
		
		menubar.add_cascade(label="Year", menu=yearmenu)
		
		menubar.add_command(label="Show Areas", command=self.show_areas)
		menubar.add_command(label="Show Map", command=self.draw_map)
		menubar.add_command(label="Show Towers", command=self.draw_towers)
		menubar.add_command(label="Graph Areas", command=self.graph_areas)
		menubar.add_command(label="Show Densities", command=self.show_densities)
		menubar.add_command(label="Animate", command=self.animate)
		menubar.add_command(label="Gen CSV", command=self.generate_csv)
		
		self.root.config(menu=menubar)

t = TowerMap()
