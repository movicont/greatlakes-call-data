import sys, voronoi as v
from Tkinter import *
import time, random as rn
import math

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
			s += self.points[i].x*self.points[i+1].y - self.points[i+1].x*self.points[i].y
		return abs(0.5*s)
	
	def centroid(self):
		ratio = 1.0/(6*self.area())
		x = sum(map(lambda one, two: (one.x+two.x)*(one.x*two.y - two.x*one.y), self.points[0:len(self.points)-1], self.points[1:]), 0)
		y = sum(map(lambda one, two: (one.y+two.y)*(one.x*two.y - two.x*one.y), self.points[0:len(self.points)-1], self.points[1:]), 0)
		return Point(ratio*abs(x), ratio*abs(y))

class TowerMap:
	def __init__(self):
		self.db = database.DBConnection()
		self.year, self.month, self.day = '2005', '01', '01'
		dat = self.handle_data()
		self.points, self.width, self.height = dat[0], dat[1], dat[2]
		self.voronoi = []
		
		self.root = Tk()
		self.root.title('Rwanda Phone Towers')
		self.canvas = Canvas(self.root, width=self.width+150, height=self.height+110)
		self.total()
		self.menu()
		self.canvas.pack()
		
		self.e = Entry(self.root)
		self.e.pack()
		self.e.delete(0, END)
		self.e.insert(0, "All")
		
		self.root.mainloop()
		
	def generate_color(self, value, maximum):
		value, maximum = float(int(value)), float(int(maximum))
		return '#' + "".join(["%02x"%(255-(value/maximum)*255), "%02x"%255, "%02x"%255])

	def handle_data(self):
		df = csv.DelimitedFile('../data/towers.csv', ',')
		points = []
		site_id = map(lambda x: float(x), df.array[df.rfields['SITEID']])
		longitude = map(lambda x: float(x), df.array[df.rfields['LONG']])
		latitude = map(lambda x: float(x), df.array[df.rfields['LAT']])
		latitude = map(lambda x: x+abs(min(latitude)), latitude)
		longitude = map(lambda x: x-abs(min(longitude)), longitude)

		WIDTH, HEIGHT = max(longitude)*300, max(latitude)*300

		points = map(lambda lat, lon: Point(lon, lat), latitude, longitude)
		points = map(lambda p: Point(p.x*(WIDTH/(max(longitude) - min(longitude))), p.y*(HEIGHT/(max(latitude) - min(latitude)))), points)
		return points, WIDTH, HEIGHT

	def next(self, year=None, month=None, day=None):
		if year == None or month == None or day == None:
			self.day = self.date_prepend(int(self.day) + 1)
		else:
			self.year, self.month, self.day = year, month, day
		print self.year, self.month, self.day
		calls = self.db.query("SELECT SUM(`calls_in`) FROM `hourly_tower_activity` WHERE `date`='"+self.year + '-' + self.month + '-' + self.day+"' GROUP BY `tower_id`")
		self.graph(map(lambda x: x[0], calls))

		self.e.delete(0, END)
		self.e.insert(0, self.year + '-' + self.month + '-' + self.day)
		
		return map(lambda x: x[0], calls)

	def total(self):
		calls = self.db.query("SELECT `tower_id`, SUM(`calls_in`) FROM `hourly_tower_activity` GROUP BY `tower_id`")
		self.graph(map(lambda x: x[1], calls))
		return map(lambda x: x[1], calls)

	def graph(self, data):
		self.generate_voronoi()
		i = 0
		for point, polygon in self.voronoi:
			color = self.generate_color(data[i], max(data))
			self.canvas.create_polygon(*map(lambda pt: (pt.x, pt.y), polygon.points), fill=color, outline="black",activefill="darkgray")
			i+=1
		print max(data)
			
	def show_areas(self):
		for point, polygon in self.voronoi.items():
			for i in range(len(polygon.points)):
				if polygon.points[i].x < 0: polygon.points[i].x = 0
				if polygon.points[i].y < 0: polygon.points[i].y = 0
				if polygon.points[i].x > self.width + 150: polygon.points[i].x = self.width + 150
				if polygon.points[i].y > self.height + 110: polygon.points[i].y = self.height + 110
			area, centroid = polygon.area(), polygon.centroid()
			if area > 150:
				#if centroid.x < 20: centroid.x += 20
				#if centroid.x > self.width + 150: centroid.x = self.height - 20
				#if centroid.y < 20: centroid.y += 20
				#if centroid.y > self.height + 110: centroid.y = self.width - 20
				print centroid.x, centroid.y, str(round(area, 1)), polygon.points
				self.canvas.create_text(centroid.x, centroid.y, text=str(round(area, 1)), font=("Helvetica", int(math.log(area))))			

	def generate_voronoi(self):
		f = open("voronoi_towers")
		i = 1
		for line in f:
			line = line.replace("\n", "")
			polygon = line.split(",")
			poly = []
			for edge in polygon:
				edge = edge.split(" ")
				#print float(edge[0]), float(edge[1])
				poly.append(Point(float(edge[0]), self.width-float(edge[1])))
			self.voronoi.append((self.points[i], Polygon(poly)))
			i += 1
		return self.voronoi
		
	#def draw_points(self):
	#	for p in self.points:
	#		self.canvas.create_oval(p.x, self.width-p.y, p.x+2, self.width-p.y+2, fill="black")
	
	def date_prepend(self, n):
		if n < 10: n = '0' + str(n)
		return str(n)
	
	def menu(self):
		menubar = Menu(self.root)
		menubar.add_command(label="<- Prev", command=None)
		menubar.add_command(label="Next ->", command=self.next)
		menubar.add_command(label="All", command=self.total)
		
		yearmenu = Menu(menubar, tearoff=0)
		for k in range(2005, 2009):
			monthmenu = Menu(yearmenu, tearoff=0)
			for j in range(1, 13):
				daymenu = Menu(monthmenu, tearoff=0)
				for i in range(1, 32):
					#print self.date_prepend(k), self.date_prepend(j), self.date_prepend(i)
					daymenu.add_command(label=str(i), command=lambda:self.next(self.date_prepend(k), self.date_prepend(j), self.date_prepend(i)))
				monthmenu.add_cascade(label=str(j), menu=daymenu)
			
			yearmenu.add_cascade(label=str(k), menu=monthmenu)
		
		menubar.add_cascade(label="Year", menu=yearmenu)
		menubar.add_command(label="Show Areas", command=self.show_areas)
		self.root.config(menu=menubar)

t = TowerMap()

"""
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

m = Basemap(llcrnrlon=1, \
            llcrnrlat=40.6, \
            urcrnrlon=8.8, \
            urcrnrlat = 49.6, \
            resolution = 'l', \
            projection = 'tmerc', \
            lon_0 = 4.9, \
            lat_0 = 45.1)
            
fig = plt.Figure()
m.ax = fig.add_axes([0, 0, 1, 1])
fig.set_figsize_inches((8/m.aspect, 8.))

m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.fillcontinents(color='beige')
"""
