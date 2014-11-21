
""" Voronoi data handler - reads in data from voronoi_towers 
and places them in database. """

import sys
sys.path.append('..')
import base.csv as csv
import numpy as np
import matplotlib.nxutils as nx

import base.database as database


class Voronoi:
	def __init__(self):
		self.voronoi = []
		self.db = database.DBConnection()
		self.handle_data()
		self.get_useful_points()
		self.generate_voronoi()
	
	def handle_data(self):
		df = csv.DelimitedFile('../data/towers.csv', ',')
		points = []
		site_id = map(lambda x: float(x), df.array[df.rfields['SITEID']])
		longitude = map(lambda x: float(x), df.array[df.rfields['LONG']])
		latitude = map(lambda x: float(x), df.array[df.rfields['LAT']])
		self.points = map(lambda sid, lat, lon: (sid, lon, lat), site_id, latitude, longitude)

	def generate_voronoi(self):
		self.voronoi = []
		f = open("voronoi_towers")
		i = 0
		xmax,ymax,xmin,ymin = -100,-100,100,100
		for line in f:
			line = line.replace("\n", "")
			polygon = line.split(",")
			ps = map(lambda x: float(x), polygon[0].split(" "))
			polygon = polygon[1:len(polygon)]
			poly = []
			for edge in polygon:
				edge = edge.split(" ")
				poly.append([float(edge[0]), float(edge[1])])
				if float(edge[0]) > xmax: xmax = float(edge[0])
				if float(edge[0]) < xmin: xmin = float(edge[0])
				if float(edge[1]) > ymax: ymax = float(edge[1])
				if float(edge[1]) < ymin: ymin = float(edge[1])
			verts = np.array(poly, float)
			self.voronoi.append((self.__find(verts), poly))
			i+=1
		voronoi = []
		for x in self.voronoi:
			if x[0] != None:
				voronoi.append(x)
				print x[1]
		self.voronoi = voronoi
		f = open("record", "w")
		for d in self.voronoi:
			f.write(str(d[0]) + str(d[1]) + "\n")
		return self.voronoi, xmax, ymax, xmin, ymin

	def point_in_poly(self, vertx, verty, x):
		i, j, c = False, len(vertx) - 1, 0
		while (i < len(vertx)):
			if (verty[i] > self.points[x][2]) != (verty[j] > self.points[x][2]) and (self.points[x][1] < ((vertx[j] - vertx[i]) * (self.points[x][2] - verty[i]) / (verty[j] - verty[i] + vertx[i]))):
				c = not(c)
			j = i
			i += 1
		return c

	def __find(self, verts):
		ps = np.array(map(lambda x: [x[1], x[2]], self.points), float)
		points_in = nx.points_inside_poly(ps, verts)
		for i in range(len(points_in)):
			if points_in[i] == True:
				 return self.points[i]
		return None

	""" Due to the fact that some points have no data and others no coords,
	    exclude those points and ouput those that are useful.
	"""
	def get_useful_points(self):
		data = self.db.query("SELECT `tower_id`, SUM(`calls_in`) FROM `minute_tower_activity` GROUP BY `tower_id`")
		tower_ids = []
		for (tower_id, calls_in) in data:
			if calls_in > 0:
				tower_ids.append(tower_id)
		useful_points = []
		for p in self.points:
			if p[0] in tower_ids:
				useful_points.append(p)
		self.points = useful_points
		print map(lambda x: x[1], self.points)
		print map(lambda x: x[2], self.points)
		print map(lambda x: x[0], self.points)

if __name__ == '__main__':
	v = Voronoi()
	v.get_useful_points()
		
