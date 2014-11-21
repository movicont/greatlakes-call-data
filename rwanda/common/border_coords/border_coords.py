
def get_coords():
	f = open('../../data/rwanda_border_coords')
	coords = []
	for line in f:
		line = line.split('&')[0]
		line = line.split('=')[1]
		line = line.split(',')
		coords.append((line[0], line[1]))
	return coords
for (x, y) in get_coords():
	print x, y
