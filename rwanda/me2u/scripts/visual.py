import os, sys, time, math, random as rn, voronoi as v, numpy as np
import Tkinter as Tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
#from mpl_toolkits.basemap import Basemap
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

	def graph(self, data):
		search = map(lambda x: float(x), data)
		maximum = max(search)
		dat_map = {}
		for pt in data:
			dat_map[pt[0]] = pt[1]
		print dat_map
		for i in range(len(self.voronoi)):
			poly = Polygon(self.voronoi[i][1])
			area, centroid = 110*111*poly.area(), poly.centroid()
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
	
	def graph_me2u(self):
		me2u = self.figure.add_subplot(111)
		f = open("../data/locations/22")
		f.readline()
		values = []
		for line in f:
			line = line.split("\t")
			values.append(float(line[3]))
		self.graph(values)
		self.figure.savefig(self.fig_name % '_with_incoming_me2u_amount')
		self.fig_name = self.fig_name % "_with_incoming_me2u_amount%s"
		

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

	def menu(self):
		menubar = Tk.Menu(self.root)
		menubar.add_command(label="Show Areas", command=self.show_areas)
		menubar.add_command(label="Show Map", command=self.draw_map)
		menubar.add_command(label="Show Towers", command=self.draw_towers)
		menubar.add_command(label="Graph Areas", command=self.graph_areas)
		menubar.add_command(label="Graph me2u", command=self.graph_me2u)
		
		self.root.config(menu=menubar)

t = TowerMap()
