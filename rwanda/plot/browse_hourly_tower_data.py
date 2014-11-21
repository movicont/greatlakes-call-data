import numpy as np, datetime, time, os, sys
from pylab import figure, show

sys.path.append("../base")
#from text import Text
from database import DBConnection

class DelimitedFile:
	def __init__(self, file_path, delimiter = '|'):
		self.f = open(file_path, "r")
		self.delimiter = delimiter
		self.fields = self.f.readline().split(delimiter)
		#self.svg = SVG("test.svg", 1200, 600, '.line {fill:none; stroke-width:1;}\n.axis {stroke:grey; fill:none; stroke-width:2; stroke-linecap:square;}\n.labels {font-family:Arial,sans-serif; font-size:14px;}\n')
			
	def read_array(self, dtype):
		""" Read a file with an arbitrary number of columns.
			The type of data in each column is arbitrary
			It will be cast to the given dtype at runtime
		"""
		cast = np.cast
		data = [[] for dummy in xrange(len(dtype))]
		for line in self.f:
			fields = line.strip().split(self.delimiter)
			for i, number in enumerate(fields):
				data[i].append(number)
		for i in xrange(len(dtype)):
			data[i] = cast[dtype[i]](data[i])
		return np.rec.array(data, dtype=dtype)

class DailyDistrict(DelimitedFile):
	def __init__(self, file_path, delimiter = '|'):
		DelimitedFile.__init__(self, file_path, delimiter)
		self.time = []
		self.calls_out = []
		self.calls_in = []

	def read(self):
		data = self.read_array(np.dtype([('district', 'int32'), ('date', 'int32'), ('shock', str), ('shocktype', str), ('calls_out', 'int32'), ('calls_in', 'int32'), ('dur_out', 'int32'), ('dur_in', 'int32'), ('me2u_out', 'int32'), ('me2u_in', 'int32'), ('me2u_val_out', 'int32'), ('me2u_val_in', 'int32'), ('intl_calls_out', 'int32'), ('intl_calls_in', 'int32'), ('intl_dur_out', 'int32'), ('intl_dur_in', 'int32')]))
		np.save('test.npy', data)
		#data = np.load('test.npy')
		xs = map(lambda x: time.mktime(datetime.date(int('200'+str(x)[0:1]), int(str(x)[1:3]), int(str(x)[3:5])).timetuple()), data.date)
		f = FigureBrowse(xs, data.calls_out)

class FigureBrowse:
	"""
	Click on a point to select and highlight it -- the data that
	generated the point will be shown in the lower axes.  Use the 'n'
	and 'p' keys to browse through the next and pervious points
	"""
	def __init__(self, xs, ys):
		self.X = np.random.rand(100, 200)
		self.xs = xs
		self.Xs = []
		for i in xs:
			self.Xs.append(datetime.date.fromtimestamp(i))
	
		self.ys = ys

		self.fig = figure()
		self.fig.canvas.mpl_connect('pick_event', self.onpick)
		self.fig.canvas.mpl_connect('key_press_event', self.onpress)

		self.ax = self.fig.add_subplot(211)
		self.ax.set_title('tower usage')
	
		self.line, = self.ax.plot(self.xs, self.ys, 'o', picker=2)  # 5 points tolerance
	
		self.ax2 = self.fig.add_subplot(223)
		self.ax3 = self.fig.add_subplot(224)
		self.lastind = 0

		self.text = self.ax.text(0.05, 0.95, 'selected: none',
							transform=self.ax.transAxes, va='top')
		self.selected,  = self.ax.plot([self.xs[0]], [self.ys[0]], 'o', ms=25, alpha=0.4,
									  color='red', visible=False)

		show()
	
	def onpress(self, event):
		if self.lastind is None: return
		if event.key not in ('n', 'p'): return
		if event.key=='n': inc = 1
		else:  inc = -1
		self.lastind += inc
		self.lastind = np.clip(self.lastind, 0, len(self.xs)-1)
		self.update()

	def onpick(self, event):

	   if event.artist!=self.line: return True

	   N = len(event.ind)
	   if not N: return True

	   x = event.mouseevent.xdata
	   y = event.mouseevent.ydata

	   distances = np.hypot(x-self.xs[event.ind], y-self.ys[event.ind])
	   indmin = distances.argmin()
	   dataind = event.ind[indmin]

	   self.lastind = dataind
	   self.update()

	def update(self):
		if self.lastind is None: return
		dataind = self.lastind

		self.ax2.cla()
		self.ax3.cla()
		dt = datetime.date.fromtimestamp(self.xs[dataind])
		
		db = DBConnection()
		match = db.query("SELECT `date`, sum(`calls_in`), sum(`dur_in`) FROM `hourly_tower_activity` WHERE `date`='"+str(dt.year) + ('0'+str(dt.month) if dt.month < 10 else str(dt.month)) + ('0'+str(dt.day) if dt.day < 10 else str(dt.day))+"' GROUP BY `hour`")

		clean, clean2 = [], []
		for entry in match:
			#print entry
			clean.append(int(entry[1]))
			clean2.append(int(entry[2]))
		#self.ax2.plot(range(0, 24), clean, '-')
		self.ax2.bar(range(0, 24), clean)
		self.ax3.bar(range(0, 24), clean2)

		self.ax2.text(0.05, 0.9, str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day),
				 transform=self.ax2.transAxes, va='top')
		
		self.selected.set_visible(True)
		self.selected.set_data(self.xs[dataind], self.ys[dataind])

		self.text.set_text('selected: %d'%dataind)
		self.fig.canvas.draw()
		show()

dd = DailyDistrict('../data/tower1.txt')
dd.read()
