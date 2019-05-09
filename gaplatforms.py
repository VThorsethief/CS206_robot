import pyrosim.pyrosim as pyrosim
import random
from individual import INDIVIDUAL
import copy
import pickle
from population import POPULATION
from platforms import PLATFORMS
import constants as c
import datetime
import time
from recorder import Recorder
import os
import pprint
from archive import Archive
import matplotlib.pyplot as plt


envs = PLATFORMS()

parents = POPULATION(c.popSize)
parents.Initialize()
parents.Evaluate(envs, pb = True, pp = False)
while not parents.pop[0].test_pass:
	print("test failure")
	parents = POPULATION(c.popSize)
	parents.Initialize()
	parents.Evaluate(envs, pb = True, pp = False)
parents.Print()
startTimes = []
copyTimes = []
evalTimes = []
generations = []
fillTimes = []
entire_fill = []

pop_size = c.popSize
print(pop_size)
recorder = Recorder()

children = None
for g in range(1,c.numGens):
	start = time.time()
	# generations.append(g)
	starttime = time.time() - start
	if g > 0:
		del children
	children = POPULATION(pop_size)
	# if g < c.numGens *.25:
	# 	entire_fill_temp = children.Fill_From(parents)	
	# else:
	# pop_fitness, ages = 
	if c.evolution_alg == 'apfo':
		recorder.record_population_fitness(*children.apfo(parents))
	elif c.evolution_alg == 'genetic':
		entire_fill_temp = children.Fill_From(parents)
	fillTime = time.time() - starttime
	# pp.pformat(children.pop[0])
	children.Evaluate(envs, pb = True, pp = False)
	evaluateTime = time.time() - fillTime
	parents = copy.deepcopy(children)
	copyTime = time.time() - evaluateTime
	if g % 2 == 0:
		print(g, end = " ")
		children.Print()
	else: 
		print(g)
	recorder.record_times(g, evaluateTime, copyTime, fillTime, starttime)
	if c.evolution_alg == 'apfo':
		recorder.add_metrics(parents.pop[recorder.evolution_data['pop_fitness'][g - 1]['best_index']], g)
	elif c.evolution_alg == 'genetic':
		recorder.add_metrics(parents.pop[0], g)
	pop_size = len(parents.pop)


# recorder.plotTimes()
recorder.plot_evolution()
best = POPULATION(1)
best.pop[0] = parents.Copy_Best_From(parents)
repeat = 'r'
while repeat == 'r':
	best.Evaluate_Best(envs, pb = False, pp = True, retain_data = True)
	recorder.plot_touch_values(best.pop[0])
	repeat = input("Press 'r' to repeat: ")

recorder.present()
if c.evolution_alg == 'apfo':
	recorder.plot_fitness_values()
saveOption = input("Save File? [y/n]")
if(saveOption =='y'):
	saveBot = True
	saveLabel = input("file name: ")
else:
	print("Not saved")
	saveBot = False


robot_name = "spiderbot" + str(datetime.date.today()) + ".p"
robot_file = os.path.join(c.save_file_folder, robot_name)
f = open(robot_file, "wb")
pickle.dump(best, f)
f.close()

	# if bestBot.fitness < best.pop[0].fitness:
	# 	print("new best spider")
	# 	bestBot = copy.deepcopy(best.pop[0])
if saveBot:
	print("Elected to save")
	manualSave = copy.deepcopy(best.pop[0])
	manualLabel = saveLabel + str(datetime.date.today()) + ".p"
	manSav = open(os.path.join(c.save_file_folder,manualLabel), "wb")
	archive_save = Archive(manualSave.genome, manualSave.cppn.save())
	pickle.dump(archive_save, manSav)
	manSav.close()
save_data = input("Save Data(y/n): ")
if save_data == 'y':	
	recorder.archive_data()

# parents.pop[0].Evaluate(False)
# 	children.Mutate()
# 	children.Evaluate(True)
# 	parents.ReplaceWith(children)
# 	parents.Print()
# parents.Evaluate_Select(False, [3,5,7])