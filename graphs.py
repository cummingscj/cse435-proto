#######################################################
#
# Author: Christopher Cummings
# Graph objects.
#
#######################################################

import plotly
import plotly.graph_objs as go


class LineGraph(object):

	def __init__(self, rate, ped_info, car_info, time, acceleration, distance):
		self.time = time
		self.car_info = car_info
		self.ped_info = ped_info
		self.ped_pos = list()
		self.car_pos = list()
		self.ped_speed = list()
		self.car_speed = list()
		self.rates = rate
		self.acceleration = [i*1000 for i in acceleration]
		self.distance = distance
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
		self.make_dist_to_ped_graph()
		self.make_speed_graph()
		self.make_rate_graph()
		self.make_acceleration_graph()

	def make_acceleration_graph(self):
		time = [i for i in range(self.time)]
			
		trace0 = go.Scatter(
			x = time,
			y = self.acceleration,
			name = 'Acceleration of the Car',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		data = [trace0]

		layout = dict(title = 'Magnitude of Acceleration vs Time of the Car',
			xaxis = dict(title = 'Time (s * 10)'),
			yaxis = dict(title = '|Acceleration| (m/s^2)'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='acceleration-graph.html')

	def make_rate_graph(self):
		time = [i for i in range(self.time)]
			
		trace0 = go.Scatter(
			x = time,
			y = self.rates,
			name = 'Rate of Approach',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		data = [trace0]

		layout = dict(title = 'Rate at which the car approaches the pedestrian',
			xaxis = dict(title = 'Time (s * 10)'),
			yaxis = dict(title = 'Rate (m/s)'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='rate-graph.html')

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
			yaxis = dict(title = 'Speed (m/s) -- |V|'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='speed-graph.html')

	def make_dist_to_ped_graph(self):
		"""
		The distance between the car and the ped over time.
		"""
		time = [i for i in range(self.time)]

		trace0 = go.Scatter(
			x = time,
			y = self.distance,
			name = 'Distance',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		data = [trace0]

		layout = dict(title = 'Distance Between the Car and Pedestrian Over Time',
			xaxis = dict(title = 'Time (ms)'),
			yaxis = dict(title = 'Distance (m)'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='distance-graph.html')

	def make_pos_graph(self):
		"""
		Positional graph.
		"""
		time = [i for i in range(self.time)]

		car_x = [i[0] for i in self.car_pos]
		car_y = [i[1] for i in self.car_pos]

		ped_x = [i[0] for i in self.ped_pos]
		ped_y = [i[1] for i in self.ped_pos]

		trace0 = go.Scatter(
			x = time,
			y = car_x,
			name = 'Car X Position',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		trace1 = go.Scatter(
			x = time,
			y = ped_x,
			name = 'Pedestrian X Position',
			line = dict(
				color = ('rgb(0, 200, 5)'),
				width = 4)
		)

		data = [trace0, trace1]

		layout = dict(title = 'X Position of the Car and Pedestrian Over Time',
			xaxis = dict(title = 'Time (ms)'),
			yaxis = dict(title = 'X Coordinates'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='x-positional-graph.html')

		trace0 = go.Scatter(
			x = time,
			y = car_y,
			name = 'Car Y Position',
			line = dict(
				color = ('rgb(0, 20, 200)'),
				width = 4)
		)

		trace1 = go.Scatter(
			x = time,
			y = ped_y,
			name = 'Pedestrian Y Position',
			line = dict(
				color = ('rgb(0, 200, 5)'),
				width = 4)
		)

		data = [trace0, trace1]

		layout = dict(title = 'Y Position of the Car and Pedestrian Over Time',
			xaxis = dict(title = 'Time (ms)'),
			yaxis = dict(title = 'Y Coordinates'),
			)

		fig = dict(data=data, layout=layout)
		plotly.offline.plot(fig, filename='y-positional-graph.html')