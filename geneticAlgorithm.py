import pyrosim.pyrosim as pyrosim
import random
from individual import INDIVIDUAL
import copy
import pickle
from population import POPULATION
from environments import ENVIORNMENTS
import constants as c
import datetime
import time
from recorder import Recorder
import os
import pprint


envs = ENVIORNMENTS()

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


pp = pprint.PrettyPrinter(indent = 4)
children = None
for g in range(1,c.numGens):
	start = time.time()
	process_timees['generations'].append(g)
	# generations.append(g)
	starttime = time.time() - start
	if g > 0:
		del children
	children = POPULATION(c.popSize)
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
	evalTimes.append(evaluateTime) 
	copyTimes.append(copyTime) 
	fillTimes.append(fillTime)
	startTimes.append(starttime)
	entire_fill.append(entire_fill_temp)


recorder = Recorder(generations, evolution_metrics)
recorder.plotTimes(startTimes, evalTimes, copyTimes, fillTimes, entire_fill_temp)
recorder.plot_evolution()
best = POPULATION(1)
best.pop[0] = parents.Copy_Best_From(parents)
repeat = 'r'
while repeat == 'r':
	best.Evaluate_Best(envs, pb = False, pp = True, retain_data = True)
	recorder.plot_touch_values(best.pop[0])
	print(best.pop[0].genome)
	repeat = input("Press 'r' to repeat: ")

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
try:
	bb = open(os.path.join(c.save_file_folder, "bestbot.p"), "rb")
	bestBot = pickle.load(bb)
	bb.close()
	# if bestBot.fitness < best.pop[0].fitness:
	# 	print("new best spider")
	# 	bestBot = copy.deepcopy(best.pop[0])
	if saveBot:
		print("Elected to save")
		manualSave = copy.deepcopy(best.pop[0])
		manualLabel = saveLabel + str(datetime.date.today()) + ".p"
		manSav = open(os.path.join(c.save_file_folder,manualLabel), "wb")
		pickle.dump(manualSave, manSav)
		manSav.close()

except FileNotFoundError:
	bestBot = copy.deepcopy(best.pop[0])
bb = open(os.path.join(c.save_file_folder,"bestbot.p"), "wb")
pickle.dump(bestBot, bb)
bb.close()
# parents.pop[0].Evaluate(False)
# 	children.Mutate()
# 	children.Evaluate(True)
# 	parents.ReplaceWith(children)
# 	parents.Print()
# parents.Evaluate_Select(False, [3,5,7])





