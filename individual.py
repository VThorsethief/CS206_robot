import random
import pyrosim.pyrosim as pyro
from spiderbot import Spiderbot
import math
import numpy
import constants as c
from simpleSpiderBot import SimpleSpiderBot
from cppn.CPPN.cppn import CPPN
class INDIVIDUAL:
	def __init__(self, id):
		self.input_num = c.numOfLegs + 9
		self.output_num = c.numOfLegs * 2
		self.hidden_num = c.num_of_hidden
		# self.genome = numpy.random.random_sample((self.input_num,(self.output_num))) * 2 - 1
		self.genome = [numpy.zeros((16, self.hidden_num)), \
			numpy.zeros((self.hidden_num, self.hidden_num)),\
				numpy.zeros((self.hidden_num, c.numOfLegs, 2))]
		self.cppn = CPPN() # Need to change the initialization to match the robot weights up the new genome archeteture
		self.genome = self.cppn.paint_weights(self.genome)
		self.fitness = 0
		self.ID = id
		self.complete_data = None
		self.current_env = 0

	def Start_Evaluation(self, env, pb, pp):
		self.sim = pyro.Simulator(eval_steps = c.evalTime, play_blind=pb, play_paused=pp, draw_joints= True)
		# self.robot = Spiderbot(self.sim, self.genome)
		self.robot = SimpleSpiderBot(self.sim, self.genome)
		target = env.Send_To(self.sim)
		self.robot.assign_target(self.sim, target, self.genome)
		self.sim.assign_collision("env", "light")
		self.sim.assign_collision("env", "robot")
		self.sim.assign_collision("env", "body")
		self.sim.assign_collision("env", "env")
		self.sim.assign_collision("robot", "robot")
		self.sim.set_camera(
			xyz= c.cameraLocation,
			hpr = c.cameraDirection
		)
		self.sim.start()
		self.current_env = env.ID

	def Complete_Fitness(self, retain_data = False):
		self.sim.wait_to_finish()
		# exit()
		
		
		sensor_values = []
		self.sensor_data = []
		final_values = []
		self.ray_data = []
		
		
		# The summation of the sum vectors, adding all the touch values for the robot. then dividing by the length of the vector times the number of legs
		# Summation of the final touch values of the sensors at the end of the simulation, indicates the number of legs touching ground. 
		# touch_at_peak = sum(sensor_values)
		self.light_data = self.sim.get_sensor_data(sensor_id = self.robot.target_sensor)
		# NEeed to remove the body touching the ground. 
		# if inflight:r
		if self.light_data is not None:
			self.original_fitness()
			self.determine_rotation()
			self.airtime = self.determine_flight()
			self.light_dist = self.light_data[len(self.light_data) - 1]
			# self.fitness += (1/self.light_dist) * ((c.evalTime - sum(self.body_touch_data))/c.evalTime) * self.airtime
			self.fitness += (self.max_z/self.robot.z_origin) * (self.light_dist**2) * (self.airtime/c.evalTime) * (1/(1+abs(self.x_rotation)))\
				* (1/(1+abs(self.y_rotation)))
		else:
			print("Simulation Failure")
			self.fitness = 0
		
		if not retain_data:
			try:
				del self.sensor_position_data
				del self.sensor_data
				del self.body_touch_data
				del self.light_data
				del self.z_origin
				del self.complete_data
				self.complete_data = None
				del self.x_rotation_data
				del self.y_rotation_data
				# del self.max_z
				# del self.light_dist
			except AttributeError:
				pass
		else:
			if self.complete_data is None:
				self.complete_data = {
					"TouchValues" : [],
					"LightDist" : [],
					"VerticalDist" : [],
					"XPos" : [],
					"YPos" : [],
					'Ray Contact':[],
					'Body Touch': []
				}	
			self.complete_data['TouchValues'].append(self.sensor_data)
			self.complete_data['Ray Contact'].append(self.ray_data)
			self.complete_data['LightDist'].append(self.light_data)
			self.complete_data['VerticalDist'].append(self.sensor_position_data)
			self.complete_data['XPos'].append(self.sim.get_sensor_data(sensor_id=self.robot.x_position_sensor))
			self.complete_data['YPos'].append(self.sim.get_sensor_data(sensor_id=self.robot.y_position_sensor))
			self.complete_data["Body Touch"].append(self.sim.get_sensor_data(sensor_id = self.robot.body_touch))
		del self.sim
		del self.robot

		
		# del self.sensor_data

	def original_fitness(self):
		# All Data
		self.sensor_position_data = self.sim.get_sensor_data(sensor_id = self.robot.position)
		for s in self.robot.touchSensors:
			# The touch values of all the leg sensors at the time that the robot was at it's highest point
			# final_values.append(self.sim.get_sensor_data(sensor_id = self.robot.touchSensors[s])[-1])
			# All sensor data for that sensor
			self.sensor_data.append(self.sim.get_sensor_data(sensor_id = self.robot.touchSensors[s]))
			# Vector addition of the touch sensor data to the summation vector. The first iteration will be adding to a vector of zeros, while subsequent iterations
			# will be added on.
		for r in self.robot.ray_sensors:
			self.ray_data.append(self.sim.get_sensor_data(sensor_id = self.robot.ray_sensors[r]))
		self.body_touch_data = self.sim.get_sensor_data(sensor_id=self.robot.body_touch)

	def determine_flight(self):
		self.z_origin = self.robot.z_origin
		max_airtime = 0
		airtime = 0
		inflight = False
		initialize_free_fall = True
		num_of_steps = len(self.sensor_data[0])
		self.max_z = 0
		self.light_dist = 0
		# print(len(self.sensor_data))
		for x in range(5, num_of_steps):
			iteration_sum = []
			for l in range(len(self.sensor_data)):
				iteration_sum.append(self.sensor_data[l][x])
			if sum(iteration_sum) == 0 and self.body_touch_data[x] == 0:
				if inflight and not initialize_free_fall:
					airtime += 1
					if airtime > c.jump_limit:
						self.max_z = self.sensor_position_data[x] if self.sensor_position_data[x] > self.max_z and self.sensor_position_data[x] > self.z_origin else self.max_z
						self.light_dist = self.light_data[x] if self.light_data[x] > self.light_dist else self.light_dist
				else: 
					initialize_free_fall = False

					# print("Inflight: ", airtime)
				# else:
				# 	print("First flight")
				inflight = True		
			else:
				inflight = False
				airtime = 0
			if airtime > max_airtime:
				max_airtime = airtime
			del iteration_sum
		return max_airtime


			
	def determine_rotation(self):
		self.x_rotation_data = self.sim.get_sensor_data(sensor_id=self.robot.x_rotation_sensor)
		self.y_rotation_data = self.sim.get_sensor_data(sensor_id=self.robot.y_rotation_sensor)
		try:
			endpoint = len(self.x_rotation_data) - 1
			self.x_rotation = self.x_rotation_data[endpoint] - self.x_rotation_data[0]
			self.y_rotation = self.y_rotation_data[endpoint] - self.y_rotation_data[0]
		except TypeError:
			print("Simulation Failure")
			pass
		# self.x_rotation = sum(self.x_rotation_data)
		# self.y_rotation = sum(self.y_rotation_data)



	def Evaluate(self, env, pb, pp, retain_data = False):
		self.Start_Evaluation(env, pb, pp)
		self.Complete_Fitness(retain_data)
	

	def Mutate(self):
		# row_geneToMutate = random.randint(0,self.input_num - 1)
		# col_geneToMutate = random.randint(0,self.output_num - 1)
		# mutatedValue = random.gauss(self.genome[row_geneToMutate][col_geneToMutate], 
		# math.fabs(self.genome[row_geneToMutate][col_geneToMutate]))
		# if mutatedValue > 1:
		# 	mutatedValue = 1
		# elif mutatedValue < -1:
		# 	mutatedValue = -1
		# self.genome[row_geneToMutate][col_geneToMutate] = mutatedValue
		self.cppn.mutate()
		self.genome = self.cppn.paint_weights(self.genome)

	def Print(self):
		# print('[',self.ID, format(self.fitness, ".2f"), ":",format(self.max_z, ".2f"), end = "]")
		print('[', self.ID, '{:.2f}'.format(self.fitness), ":",\
		'{:.2f}'.format(self.airtime),  end = "]")
	
		
		
