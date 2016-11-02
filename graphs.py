#######################################################
#
# Author: Christopher Cummings
# Graph objects.
#
#######################################################

import plotly
import plotly.graph_objs as go


class LineGraph(object):

	def __init__(self, ped_info, car_info, time):
		self.time = time
		self.car_info = car_info
		self.ped_info = ped_info
		self.ped_pos = list()
		self.car_pos = list()
		self.ped_speed = list()
		self.car_speed = list()
		self.get_info()
		self.display()

	def get_info(self):
		for info in self.car_info:
			self.car_pos.append((info[0].x, info[0].y))
			self.car_speed.append(info[1])
		for info in self.ped_info:
			self.ped_pos.append((info[0].x, info[0].y))
			self.ped_speed.append(info[1])

	def display(self):
		"""
		Display the info in graphs.
		"""
		self.make_pos_graph()
		self.make_speed_graph()

	def make_speed_graph(self):
		"""
		Speed graph.
		"""
		time = [i for i in range(self.time)]
			
		trace0 = go.Scatter(
			x = time,
			y = self.car_speed,
			name = 'Car Speed',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		trace1 = go.Scatter(
			x = time,
			y = self.ped_speed,
			name = 'Pedestrian Speed',
			line = dict(
				color = ('rgb(0, 200, 5)'),
				width = 4)
		)

		data = [trace0, trace1]

		layout = dict(title = 'Speed Graph for Car vs Pedestrian',
			xaxis = dict(title = 'Time (ms)'),
			yaxis = dict(title = 'Speed (m/s)'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='speed-graph.html')

	def make_pos_graph(self):
		"""
		Positional graph.
		"""
		car_x = [i[0] for i in self.car_pos]
		car_y = [i[1] for i in self.car_pos]

		ped_x = [i[0] for i in self.ped_pos]
		ped_y = [i[1] for i in self.ped_pos]

		trace0 = go.Scatter(
			x = car_x,
			y = car_y,
			name = 'Car Position',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		trace1 = go.Scatter(
			x = ped_x,
			y = ped_y,
			name = 'Pedestrian Position',
			line = dict(
				color = ('rgb(0, 200, 5)'),
				width = 4)
		)

		data = [trace0, trace1]

		layout = dict(title = 'Positional Graph for Car vs Pedestrian',
			xaxis = dict(title = 'X Coordinate'),
			yaxis = dict(title = 'Y Coordinate'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='positional-graph.html')