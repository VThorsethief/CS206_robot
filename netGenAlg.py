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
import sys,os
import peas.peas as peas

sys.path.append(os.path.join(os.path.split("netGenAlg.py")[0], '..', '..'))
from peas.methods.neat import NEATPopulation, NEATGenotype

genotypes = lambda: NEATGenotype(inputs = c.numOfLegs + 4, weight_range = (-50, 50), types = ["tanh"])

pop = NEATPopulation(genotypes, popsize = c.popSize)

pop.epoch(generations = c.numGens, evaluator = pop.Evaluate())
pop.epoch()




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
evolution_metrics = {
	'fitness':[],
	'vertical': [],
	'x rot':[],
	'y rot': [],
	'airtime': [],
	'gen': []
}
for g in range(1,c.numGens):
	start = time.clock()
	generations.append(g)
	starttime = time.clock() - start
	startTimes.append(starttime)
	children = POPULATION(c.popSize)
	children.Fill_From(parents)
	fillTime = time.clock() - starttime
	fillTimes.append(fillTime)
	children.Evaluate(envs, pb = True, pp = False)
	evaluateTime = time.clock() - fillTime
	evalTimes.append(evaluateTime) 
	print(g, end = " ")
	children.Print()
	evolution_metrics['gen'].append(g)
	evolution_metrics["fitness"].append(children.pop[0].fitness)
	evolution_metrics['vertical'].append(children.pop[0].max_z)
	evolution_metrics['x rot'].append(children.pop[0].x_rotation)
	evolution_metrics['y rot'].append(children.pop[0].y_rotation)
	evolution_metrics['airtime'].append(children.pop[0].airtime)
	parents = copy.deepcopy(children)
	copyTime = time.clock() - evaluateTime
	copyTimes.append(copyTime) 


recorder = Recorder(generations, startTimes, evalTimes, copyTimes, fillTimes, evolution_metrics)
# recorder.plotTimes()
recorder.plot_evolution()
best = POPULATION(1)
best.pop[0] = parents.Copy_Best_From(parents)
repeat = 'r'
while repeat == 'r':
	best.Evaluate(envs, pb = False, pp = True)
	recorder.plot_touch_values(best.pop[0])
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





